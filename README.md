# TypeKindly Post Scraper
This is the data preprocessor and web scraper for TypeKindly.

## Prerequisites
0. (Not necessary but highly recommended) Create a dummy Facebook profile.
1. You will to download a copy of a person's profile (with their permission!) on Facebook. View the details for [mobile](https://docs.google.com/document/d/1gsMSqWto5ekuEguXWkeYYIh3qbhi9WP2cpo0Lt5Oq_w/edit?usp=sharing) and [PC](https://docs.google.com/document/d/1QkwGFD4Cbg8WtoKLJARt4_eys1dwawkZc5wJun1_i0E/edit?usp=sharing). Only get the `Comments and Reactions` and save it as JSON.
2. You will need to figure out the div tags associated with the testing facebook profile. Create a copy of `_tags.py` and rename it to `tags.py`. Here are the types of posts that you need to collect the div tags from:
   1. posts
   2. reels
   3. photos
   4. videos

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

4. The users are expected to know how to use Inspect Element to collect the div tags for each caption and container of each post type as mentioned above.
5. Copy those tags and copy paste them as strings to their corresponding Tags variable in the `tags.py` file that are named after the captions of each div tags above. Do this for each post type listed above.
6. Note that the div tags are very likely to change, so you will want to check these from time to time.
7. Create a google colab using the Jupyter Notebook found in `\liked_posts_scraper\typekindly_sentiment_analysis.ipynb` to setup the Post Analyzer.
8. Generate `key.KEY` that will be used for encryption and decryption of a post using the `key_generator.py` file by running the command `python ./key_generator`
9. Copy the `key.KEY` file into the `liked_post_scraper` directory, ensuring that there still exists a `key.KEY` in the base of the repo
10. Copy paste the content of the `KEY.key` file into the _secrets_ tab of Google Colab and name it `TYPEKINDLY_KEY`.

## Sequencing Inputs for Testing the Facebook Scrpaer and Google Colab Post Analyzer
1. To install the dependencies, run:
```bash
pip install -r requirements.txt
```
2. Unzip the files from [prerequisites](#prerequisites) and keep on navigating the folder structure until you cannot proceed anymore. Save the `likes_and_reactions.json` file and rename it as `<person_id>-liked-and-reactions.json`
3. In the `liked_posts_scraper` folder, place the `.json` file to the `json_post_reader_input` folder
4. From the root of the repo, run the command:
```bash
python .\liked_posts_scraper\main.py
```

If this is the first time you use the scraper, you will be prompted to place in the details of your Facebook profile. Place in the details of the dummy facebook profile created and exit the Chromium browser. Press enter on the terminal once done.

5. Afterwards, the command will create a `.csv` file in `json_post_reader_output` that will be fed into `facebook_post_scraper.py`.
6. Once the scraper finishes, main.py will do the last steps of preprocessing to the resulting data in preparation for sentiment analysis
7. Once done, the final files to be analyzed will be placed in a directory named `results_to_analyze`.
8. Place the created `.csv` files in the appropriate Google Drive directory and run the google colab from the [prerequisites](#prerequisites)

## Verification Procedure
To verify that the Facebook scraper can still retrieve the texts of all types of posts properly, the user may run `test_scraper_tags.py` under the tests subfolder. This will check whether the tags in the code still match the tags in the Facebook website for each type of post.

If the user wishes to manually check the output of each component of the scraper separately, they can run `main.py` with some of the functions commented out.

```python 
if __name__ == "__main__":
    ## comment out specific function if u wanna test a specific part of the program
    ## UNCOMMENT all function if u wanna run it normally (make sure json_post_reader_input is populated)

    convert_likes_and_reaction_jsons_to_csv()
    run_scraper()
    translate_results()
    convert_result_json_to_csv()
```

For example, if the user wants to verify that `json_post_reader.py` creates the correct CSV files, they can comment out all functions in the codeblock except `convert_likes_and_reactions_to_csv()` to run `json_post_reader.py` by itself. This can be useful to check if a module still works after the user makes changes to the code of the module.
