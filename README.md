# TypeKindly Post Scraper
This is the data preprocessor and web scraper for TypeKindly.

## Prerequisites
0. (Not necessary but highly recommended) Create a dummy Facebook profile.
1. You will to download a copy of a person's profile (with their permission!) on Facebook. View the details [here](https://www.facebook.com/help/212802592074644/). Only get the `Comments and Reactions` and save it as JSON.
2. You will need to figure out the div tags associated with the testing facebook profile. Here are the types of posts that you need to collect the div tags from:
   1. posts
   2. reels
   3. photos
   4. videos
   5. live videos

3. We will be using this [facebook post as example](https://www.facebook.com/NBA.updates4all/posts/pfbid0iZmT8WrcE3xXSCFfEodg5HFH6eKxr7AkeW4UFRsn1HymtsZ4ArvWDiXeJyCLhGaFl?rdid=DWDAYn6lcw4UYWVe):
<p align="center">
    <img src="https://github.com/user-attachments/assets/53abe7d3-3867-4834-947e-7cc9b99f011c" alt="container_tags">
    <br>
    <b>`container_tags`</b>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/b69ec043-5c83-4697-8e82-9fbfbf79b689" alt="post_text_tags">
    <br>
    <b>`post_text_tags`</b>
</p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/de0b56a9-72dc-49e5-8478-46ba521a9e09" alt="see_more_captions_class_tags">
    <br>
    <b>`see_more_captions_class_tags`</b>
</p>

4. Copy those tags and create a `tags.py` file and create lists that are named after the captions of each div tags above.
5. In the same `tags.py file`, create a list named `post_see_more_intersect_tags` which are just the tags that are shared among `post_text_tags` and `see_more_captions_class_tags`.
6. Note that the div tags are very likely to change, so you will want to check these from time to time.
7. Create a google colab using the Jupyter Notebook `\liked_posts_and_comments_scraper\typekindly_sentiment_analysis.ipynb`.
## Usage
1. (please ignore this rn) To install the dependencies, run:
```bash
pip install -r requirements.txt
```
2. Unzip the file from [prerequisites](#prerequisites) and keep on navigating the folder structure until you cannot proceed anymore. Save the `likes_and_reactions.json` file and rename it as `<person_id>-liked-and-reactions.json`
3. In the `liked_posts_and_comments_scraper`, place the `.json` file to the `json_post_reader_input` folder
4. From the root of the repo, run the command:
```bash
python .\liked_posts_and_comments_scraper\json_post_reader.py
```
and for first time use, you will be prompted to place in the details of your Facebook profile. Place in the details of the dummy facebook profile created and exit the Chromium browser. Press enter on the terminal once done.

5. Afterwards, the command will create a `.csv` file in `json_post_reader_output` that will be fed into `main.py`.
6. Once converted, run the command:
```bash
python .\liked_posts_and_comments_scraper\main.py
```
to allow the `.csv` file to undergo necesssary preprocessing for sentiment analysis

7. Once done, the final file to be analyzed will be placed in a directory named `results_to_analyze`.
8. Place the created `.csv` files in the appropriate Google Drive directory and run the google colab from the [prerequisites](#prerequisites)
