
from playwright.async_api import async_playwright, Page, BrowserContext, Locator
from bs4 import BeautifulSoup
#import json
import os
import asyncio
from tags import PostTags, VideoTags, PhotoTags, ReelTags, LiveVideoTags, GroupTags
from project_types import Tags, TypeOfPost, PostData
# from words import filter_text
# from results_translator import get_translation
from security import encrypt_string

directory = os.path.dirname(__file__)
results_directory = os.path.join(directory, 'results', )
storage_path = os.path.join(results_directory, 'fb_session.json')

MAX_CONCURRENCY: int = 2

async def login_to_facebook():
    """Opens the chromium browser and lets you log in to your facebook account. It does not open if you have used this already
    """
    if os.path.exists(storage_path):
        return 
    async with async_playwright() as p:
        # opens the browser
        browser = await p.chromium.launch(headless=False) 
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.facebook.com")
        print("Please log in to Facebook manually.")
        input("Press Enter after you have logged in...")

        # Save cookies and local storage (session)
        await context.storage_state(path=storage_path)
        print("Session saved!")
        
        await browser.close()

async def open_account_page(context: BrowserContext, data: PostData) -> PostData:
    """Opens the given URL to the post

    Parameters
    ----------
    context: BrowserContext
        The browser being used to scrape 
    data: PostData
        The value that stores the data from a post

    Returns
    -------
    PostData
        The data from the post in this page
    """
    page = await context.new_page()
    print(f"Going to page: {data.url}")
    try:
        await page.goto(data.url)
    except:
        print(f"could not load page, skipping {data.url}")
        data.post_text = "__PAGE_NOT_LOADED__"
        await page.close()
        return data
    await asyncio.sleep(3)
    
    soup = BeautifulSoup(await page.content(), 'html.parser')

    not_avail = "This content isn't available right now"
    if not_avail not in soup.text:
        # detail = None
        # if (soup_data := soup.find('meta', {'name': 'description'})) is not None:
        #     detail = soup_data
        match data.url_post_type:
            case TypeOfPost.VIDEO:
                post_texts, post_images, post_videos = await get_post_data_from_page(page, VideoTags)
            case TypeOfPost.PHOTO:
                post_texts, post_images, post_videos = await get_post_data_from_page(page, PhotoTags)
            case TypeOfPost.REEL:
                post_texts, post_images, post_videos = await get_post_data_from_page(page, ReelTags)
            case TypeOfPost.COMMENT: ## this is not supported
                post_texts, post_images, post_videos = "", [], []
            case TypeOfPost.GROUP: ## this is not supported
                post_texts, post_images, post_videos = await get_post_data_from_page(page, GroupTags)
            case _: ## by default, assume its a post
                post_texts, post_images, post_videos = await get_post_data_from_page(page, PostTags)
        # data['detail'] = detail 
        data.post_text = post_texts
        data.post_images = post_images 
        data.post_videos = post_videos 

    print(f"Finished scraping {data.url}")
    await page.close()
    return data

async def press_button(see_more_buttons: Locator):
    """Presses the see more button and waits for some time after to load the content

    Parameters
    ----------
    see_more_buttons: Locator
        locations of all the see more buttons in the page
    """
    button_count = await see_more_buttons.count()
    for i in range(button_count):
        button = see_more_buttons.nth(i)
        visible = await button.is_visible()
        if visible:
            await button.click()
            await asyncio.sleep(1)

async def scrape_post_data(soup: BeautifulSoup, tags: Tags, url: str) -> tuple[str, list[str], list[str]]:
    """Gets the captions of a post

    Parameters
    ----------
    soup: BeautifulSoup
    tags: Tags
        The tags of all the posts to be analyzed based on the account being used
    url: str
        The url of the post that you will be scraping

    Returns
    -------
    tuple[str, list[str], list[str]]
        Tuple containing the captions of the post, list of urls for the images, and the list of urls for the videos
    """
    post_texts = ""
    post_images: list[str] = []
    post_videos: list[str] = []

    container_tags              = tags.container_tags
    see_more_intersect_tags     = tags.see_more_intersect_tags
    text_tags                   = tags.text_tags
    secondary_text_tags         = tags.secondary_text_tags
    see_more_caption_class_tags = tags.see_more_caption_class_tags

    posts = soup.find_all('div', class_=container_tags[0])
    filtered_posts = [post for post in posts if post['class'] == container_tags]

    if len(filtered_posts) == 0:
        print(f"    empty filtered_posts for {url} <----------------------------------- POSSIBLE ERROR")
        return ("_POSSIBLY_WRONG_TAGS_", [], [])
    post = filtered_posts[0]
    find_div_with_caption = post.find_all('div', class_=see_more_intersect_tags[0])
    div_with_caption = [t for t in find_div_with_caption if t['class'] == text_tags or \
                        t['class'] == see_more_caption_class_tags or \
                        t['class'] == secondary_text_tags]
    for div_cap in div_with_caption:
        post_texts += (div_cap.get_text(separator=' ', strip=True) + '\n')
    
    # translated_text = get_translation(post_texts)
    # post_texts = filter_text(translated_text)
    if post_texts != "":
        post_texts = encrypt_string(post_texts)

    images = post.find_all_next('img')
    image_urls = [img['src'] for img in images if img['src'].startswith("https://scontent") and img['src'] not in post_images]
    post_images += image_urls

    return (post_texts, post_images, post_videos)

async def try_determine_if_live_video(page: Page) -> bool:
    """Determines if the page is a live videos

    Parameters
    ----------
    page: Page
        page to be analyzed

    Returns
    -------
    bool
        Returns true if the page is a live video else false
    """
    if "/live/" in page.url:
        print(f" livestream: {page.url}")
        try:
            comment_button = page.locator("div[role='button']", has_text="comments")
            await press_button(comment_button)
            print("pressed comments button")
            return True
        except Exception:
            print("did not find comments button")
            return False
    else:
        print(f" normal vid: {page.url}")
        return False

async def try_press_see_more(page: Page):
    """try except statement to see if a page has a see more button
    Parameters
    ----------
    page: Page
        The page that will be checked
    """
    try:
        see_more_buttons = page.locator("div[role='button']", has_text="See more")
        await press_button(see_more_buttons)
        print("pressed see more button")
    except Exception:
        print("did not find see more button")

async def get_post_data_from_page(page: Page, tags: Tags) -> tuple[str, list[str], list[str]]:
    """Collects the data from the posts of the profile/page
    Returns
    ----------
    tuple
        a tuple of for the post's attached text, images, and videos
    """
    # wait for content to load
    await asyncio.sleep(2)
    # get the page content
    if not tags is PostTags and not tags is GroupTags:
        if tags is VideoTags:
            is_live_video = await try_determine_if_live_video(page)
            await asyncio.sleep(1)
            await try_press_see_more(page)
            soup = BeautifulSoup(await page.content(), 'html.parser')
            if is_live_video:
                output = await scrape_post_data(soup, LiveVideoTags, page.url)
            else:
                output = await scrape_post_data(soup, VideoTags, page.url)
            return output
        else:
            await try_press_see_more(page)
    soup = BeautifulSoup(await page.content(), 'html.parser')
    output = await scrape_post_data(soup, tags, page.url)
    return output


async def open_new_pages(context: BrowserContext, datas: list[PostData]) -> asyncio.Future[list[PostData]]:
    """Opens pages by batches

    Parameters
    ----------
    context: BrowserContext
        The browser being used to scrape
    datas: list[PostData]

    Returns
    -------
    asynctio.Future[list[PostData]]
    """
    batches: list[list[PostData]] = [datas[i : i+MAX_CONCURRENCY] \
                                     for i in range(0, len(datas), MAX_CONCURRENCY)]
    list_of_tasks: list[asyncio.Task[PostData]] = []
    for batch in batches:
        async with asyncio.TaskGroup() as tg:
            for data in batch:
                list_of_tasks.append(
                    tg.create_task(open_account_page(context, data))  
                )
    results: asyncio.Future[list[PostData]] = asyncio.gather(*list_of_tasks)
    return results

async def main_scraper(datas: list[PostData], headless: bool) -> asyncio.Future[list[PostData]]:
    """Scrapes the data and dumps the data to a json file
    
    Parameters
    ----------
    datas: list[PostData]
    headless: bool
        True if you don't want to see the browser as it is scraping
    """
    await login_to_facebook()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(storage_state=storage_path)
        output = await open_new_pages(context, datas)
        ## no need to close browser since all pages close themselves which eventually closes browser
        print("Scraping completed for all URLs.")
        return output
