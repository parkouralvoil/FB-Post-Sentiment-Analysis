from playwright.sync_api import sync_playwright, Locator
from bs4 import BeautifulSoup
import time
import regex as re
from tags import PhotoTags, LiveVideoTags

vid_url = \
    'https://www.facebook.com/DevelUPDiliman/videos/787397013490795/'
photo_url = \
    'https://www.facebook.com/photo.php?fbid=7719231444786817&set=a.141296565913714&type=3'
live_vid_url = \
    'https://www.facebook.com/DevelUPDiliman/videos/787397013490795/'

# run using 
# python -m tests.test_regex

def open_page(url: str):
    page = context.new_page()
    print(f"working on url {url}")
    page.goto(url)
    time.sleep(2)

    soup = BeautifulSoup(page.content(), 'html.parser')

    try:
        see_more_buttons = page.locator("div[role='button']", has_text="See more")
        press_button(see_more_buttons)
        soup = BeautifulSoup(page.content(), 'html.parser')
        print("found see more")
    except Exception as e:
        print("No 'See more' button found or couldn't click it:", e)
    
    container_tags              =  PhotoTags.container_tags
    see_more_intersect_tags =  PhotoTags.see_more_intersect_tags
    text_tags              =  PhotoTags.text_tags
    see_more_caption_class_tags =  PhotoTags.see_more_caption_class_tags
    post_texts = ""
    post_images: list[str] = []

    posts = soup.find_all('div', class_=container_tags[0])
    filtered_posts = [post for post in posts if post['class'] == container_tags]

    post = filtered_posts[0]
    find_div_with_caption = post.find_all('div', class_=see_more_intersect_tags[0])
    div_with_caption = [t for t in find_div_with_caption if t['class'] == text_tags or t['class'] == see_more_caption_class_tags]
    for div_cap in div_with_caption:
        post_texts += (div_cap.get_text(separator=' ', strip=True) + '\n')
    print(post_texts)
    images = post.find_all_next('img')
    image_urls = [img['src'] for img in images if img['src'].startswith("https://scontent") and img['src'] not in post_images]
    post_images += image_urls

def test_live_vid():
    url = live_vid_url
    page = context.new_page()
    print(f"working on url {url}")
    page.goto(url)
    time.sleep(2)

    soup = BeautifulSoup(page.content(), 'html.parser')

    try:
        see_more_buttons = page.locator("div[role='button']", has_text=re.compile(r" comments$"))
        press_button(see_more_buttons)
        soup = BeautifulSoup(page.content(), 'html.parser')
        print("found comments on live vid")
    except Exception as e:
        print("No 'comments' button found or couldn't click it:", e)
        
    time.sleep(1)
    try:
        see_more_buttons = page.locator("div[role='button']", has_text="See more")
        press_button(see_more_buttons)
        soup = BeautifulSoup(page.content(), 'html.parser')
        print("found see more")
    except Exception as e:
        print("No 'See more' button found or couldn't click it:", e)
    
    time.sleep(1)
    container_tags              =  LiveVideoTags.container_tags
    see_more_intersect_tags     =  LiveVideoTags.see_more_intersect_tags
    text_tags                   =  LiveVideoTags.text_tags
    see_more_caption_class_tags =  LiveVideoTags.see_more_caption_class_tags
    post_texts = ""
    post_images: list[str] = []

    posts = soup.find_all('div', class_=container_tags[0])
    filtered_posts = [post for post in posts if post['class'] == container_tags]
    print(posts)
    print()
    print(filtered_posts)
    # post = filtered_posts[0]
    # find_div_with_caption = post.find_all('div', class_=see_more_intersect_tags[0])
    # div_with_caption = [t for t in find_div_with_caption if t['class'] == text_tags or t['class'] == see_more_caption_class_tags]
    # for div_cap in div_with_caption:
    #     post_texts += (div_cap.get_text(separator=' ', strip=True) + '\n')
    # print(post_texts)
    # images = post.find_all_next('img')
    # image_urls = [img['src'] for img in images if img['src'].startswith("https://scontent") and img['src'] not in post_images]
    # post_images += image_urls

def test_commment():
    url = "https://www.facebook.com/updilimanFW/posts/647859034160581?comment_id=855797229182106"
    page = context.new_page()
    print(f"working on url {url}")
    page.goto(url)
    time.sleep(2)

    soup = BeautifulSoup(page.content(), 'html.parser')
    num_like_tag = soup.find('a', string=re.compile('855797229182106'))
    #num_like = num_like_tag.get_text() if num_like_tag else "None"
    print(num_like_tag)
    #print(num_like)

def press_button(see_more_buttons: Locator):
    button_count = see_more_buttons.count()
    for i in range(button_count):
        button = see_more_buttons.nth(i)
        visible = button.is_visible()
        if visible:
            button.click()
            print("pressed")
            time.sleep(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    #open_page(vid_url)
    #open_page(photo_url)
    #test_commment()
    test_live_vid()