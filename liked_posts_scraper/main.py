import asyncio
import glob
import os
import json
import csv
from project_types import PostData, JSONformat, TypeOfPost
from json_post_reader import convert_likes_and_reaction_jsons_to_csv
from facebook_post_scraper import main_scraper, results_directory
from results_translator import get_translation
from tqdm.auto import tqdm
from security import encrypt_string, decrypt_string

CSV_ROWS: int = 5
SCRAPE_HEADLESS: bool = True

SCRAPER_FN_FORMAT: str = "scraper_output"
TRANSLATOR_FN_FORMAT: str = "scraper_translated_output"

def scrape_csv_files(csv_files: list[str], skip_photos: bool, skip_videos: bool, skip_reels: bool):
    """Reads the csv files found in `json_post_reader_output` and converts them into the output json file

    Parameters
    ----------
    csv_files: list[str]
    skip_photos: bool
    skip_videos: bool
    skip_reels: bool
    """
    if len(csv_files) == 0:
        print("main.py: No csv files detected. Make sure json_post_reader_input actually has json files! Exiting program")
        exit()
    print(f"JSON to CSV conversion successful. json_post_reader_output has {len(csv_files)} csvs.")

    def create_json_output_file(_person_id: str, _datas: list[PostData]):
        file_path = os.path.join(results_directory, f'{_person_id}-{SCRAPER_FN_FORMAT}.json')
        json_datas: list[JSONformat] = [d.get_json_format() for d in _datas]

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_datas, f, ensure_ascii=False, indent=4)

    for csv_file in csv_files:
        datas: list[PostData] = [] # reset list
        filename = os.path.basename(csv_file)
        person_id = filename.split(".")[0] ## use the name of csv to track output

        with open(csv_file, newline='', encoding='utf-8') as f: ## open the csv file
            reader = csv.reader(f)
            for row in reader:
                if row[0] == "timestamp":
                    continue
                if len(row) != CSV_ROWS or row[2] == "":
                    print(f"invalid formatted data from csv: {csv_file}")
                    continue

                new_data = PostData(timestamp=int(row[0]), 
                                    reaction=row[1], 
                                    url=row[2], 
                                    poster=row[3], 
                                    post_id=row[4])
                if new_data.url_post_type == TypeOfPost.COMMENT:
                    continue ## cannot scrape comments sadly
                if new_data.url_post_type == TypeOfPost.PHOTO and skip_photos:
                    continue
                if new_data.url_post_type == TypeOfPost.VIDEO and skip_videos:
                    continue
                if new_data.url_post_type == TypeOfPost.REEL and skip_reels:
                    continue
                datas.append(new_data)
        user_data = asyncio.run(main_scraper(datas, SCRAPE_HEADLESS))
        if user_data.done():
            create_json_output_file(person_id, user_data.result())

def translate_results():
    directory = os.path.dirname(__file__)
    json_files = glob.glob(os.path.join(directory, 'results', f'*-{SCRAPER_FN_FORMAT}.json'))
    if len(json_files) == 0:
        print("main.py: No json files detected after running main_run()")
        exit()
    #print(json_files)
    #return
    output: list[JSONformat] = []

    with tqdm(total=len(json_files), desc="JSON files to translate") as json_pbar:
        for json_file in json_files:
            fn = os.path.basename(json_file.split("-")[0] + f"-{TRANSLATOR_FN_FORMAT}.json")

            with open(json_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                with tqdm(total=len(loaded_data), desc=f"translated data in {fn}") as data_pbar:
                    for json_data in loaded_data:
                        if isinstance(json_data, str):
                            break
                        post_data = PostData.make_postdata_from_json(json_data)
                        post_data.translated_post_text = encrypt_string(get_translation(decrypt_string(post_data.post_text)))
                        output.append(post_data.get_json_format())
                        data_pbar.update(1)
                        
                output_directory = os.path.join(directory, 'results_with_translation')
                path = os.path.join(output_directory, fn)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(output, f, ensure_ascii=False, indent=4)
            json_pbar.update(1)

def convert_result_json_to_csv():
    """This should be used AFTER the translate_results function is called"""
    directory = os.path.dirname(__file__)
    json_files = glob.glob(os.path.join(directory, 'results_with_translation', f'*-{TRANSLATOR_FN_FORMAT}.json'))
    if len(json_files) == 0:
        print("main.py, convert_result_json_to_csv(): No json files detected after running translate_results()")
        exit()

    with tqdm(total=len(json_files), desc="JSON files to convert") as json_pbar:
        for json_file in json_files:
            # opening the .json file
            with open(json_file, 'r', encoding='utf-8') as f: ## open the json file
                person_id = os.path.basename(json_file).split("-")[0]
                filepath = os.path.join(directory, 'results_to_analyze', f'{person_id}.csv')

                # creating the .csv file
                with open(filepath, 'w', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    field = ["timestamp", "reaction", "url", "poster", "post_id", "post_text", "translated_post_text"]
                    writer.writerow(field)
                    loaded_data = json.load(f)
                    with tqdm(total=len(loaded_data), desc=f"transferring data to {person_id}.csv") as data_pbar:
                        for post_data in loaded_data:
                            timestamp = post_data["timestamp"]
                            reaction = post_data["reaction"]
                            url = post_data["url"]
                            poster = post_data["poster"]
                            post_id = post_data["post_id"]
                            post_text = post_data["post_text"]
                            translated_post_text = post_data["translated_post_text"]
                            writer.writerow([timestamp, reaction, url, poster, post_id, post_text, translated_post_text])
                            data_pbar.update(1)
            json_pbar.update(1)

def run_scraper():
    directory = os.path.dirname(__file__)
    _csv_files = glob.glob(os.path.join(directory, 'json_post_reader_output', '*.csv'))
    scrape_csv_files(csv_files=_csv_files,
                     skip_photos=False,
                     skip_videos=False,
                     skip_reels=False)

if __name__ == "__main__":
    ## comment out specific function if u wanna test a specific part of the program
    ## UNCOMMENT all function if u wanna run it normally (make sure json_post_reader_input is populated)

    convert_likes_and_reaction_jsons_to_csv()
    run_scraper()
    translate_results() 
    convert_result_json_to_csv() 
