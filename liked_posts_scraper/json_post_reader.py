
import json
import os
import glob
import csv
from typing import Any

"""json_post_reader

This script takes in the likes and reactions of a facebook profile that was taken from their profile information (with their information) and 
processes it into a .csv file so that it can be analyzed later. It takes into account when the reaction was done, what reaction was done, 
the URL / URI of the reacted content, the display name of the poster, and the post id of the associated post

"""

LINKS_PER_CSV: int = 200
RAW_DATA_FN_FORMAT: str = "likes_and_reactions"

def convert_likes_and_reaction_jsons_to_csv():
    """
    Converts all the json files found in the directory named 'json_post_reader_input' into .csv files
    """
    directory = os.path.dirname(__file__)
    json_files = glob.glob(os.path.join(directory, 'json_post_reader_input', f'*-{RAW_DATA_FN_FORMAT}.json'))

    for json_output in json_files:
        #data: list[Post] = []
        with open(json_output, 'r', encoding='utf-8') as f: ## open the json file

            person_id = os.path.basename(json_output).split("-")[0]
            all_post_datas = json.load(f)
            segmented_datas: list[list[Any]] = [[]]
            i: int = 0
            for data in all_post_datas:
                if len(segmented_datas[i]) < LINKS_PER_CSV:
                    segmented_datas[i].append(data)
                else:
                    segmented_datas.append([])
                    i += 1
                    segmented_datas[i].append(data)
            
            for j, segment in enumerate(segmented_datas):
                filepath = os.path.join(directory, 'json_post_reader_output', f'{person_id}_{j+1}.csv')
                print(filepath)
                with open(filepath, 'w', newline='', encoding="utf-8") as file: ## create the csv file

                    writer = csv.writer(file)
                    field = ["timestamp", "reaction", "url", "poster", "post_id"]
                    writer.writerow(field)

                    for post_data in segment:

                        reaction = ""
                        url = ""
                        poster = ""
                        timestamp = post_data["timestamp"]
                        label_values = post_data["label_values"]
                        for label in label_values:

                            while "dict" in label:
                                # this is for handling the nested portions (ie those that are under comments)
                                label = label['dict'][0]

                            match label['label']:
                                case "Reaction":
                                    reaction = label['value'] if 'value' in label else ""
                                case "URL":
                                    url = label['value'] 
                                case "URI":
                                    url = label['value'] 
                                case "Name":
                                    poster = label['value'] 
                                case _:
                                    continue
                        
                        post_id = post_data["fbid"]

                        writer.writerow([timestamp, reaction, url, poster, post_id])
                    



if __name__ == "__main__":
    convert_likes_and_reaction_jsons_to_csv()
