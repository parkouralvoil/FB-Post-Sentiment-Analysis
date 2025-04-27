import asyncio
from project_types import PostData
from facebook_post_scraper import main_scraper

# run using 
# python -m tests.test_scraper_tags

if __name__ == "__main__":
    post_url = "https://www.facebook.com/NBA.updates4all/posts/pfbid0iZmT8WrcE3xXSCFfEodg5HFH6eKxr7AkeW4UFRsn1HymtsZ4ArvWDiXeJyCLhGaFl?rdid=DWDAYn6lcw4UYWVe"
    vid_url = "https://www.facebook.com/watch/?v=2037331740103763"

    ## NOTE, facebook is removing live videos, so this URL is no longer necessary V
    live_vid_url = "https://www.facebook.com/watch/live/?ref=watch_permalink&v=1755104001723783&rdid=FlAPpVvhZJKxzB1W"

    photo_url = "https://www.facebook.com/photo/?fbid=1095195892612904&set=pcb.1095199832612510"
    group_url = "https://www.facebook.com/groups/rivalsmarvel/permalink/1340859083998528/"
    reel_url = "https://www.facebook.com/reel/1280461636519020"
    private_url = "https://www.facebook.com/groups/4893749567414182/permalink/8998372426951855/?app=fbl"

    urls = [post_url, vid_url, live_vid_url, photo_url, group_url, reel_url, private_url]

    datas: list[PostData] = []
    for i, url in enumerate(urls):
        #if url == photo_url:
        datas.append(PostData(i, "Like", url, "test", f"{i}"))

    future_results = asyncio.run(main_scraper(datas, headless=False))
    if future_results.done():
        results = future_results.result()
        for i, r in enumerate(results):
            print(f"{i+1}: {r.url_post_type}, content: {r.post_text}, url: {r.url}")
            print()
