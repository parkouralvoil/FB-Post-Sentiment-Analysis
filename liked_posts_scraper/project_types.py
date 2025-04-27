from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Self
from unidecode import unidecode

type JSONformat = dict[str, str | list[str]]

class TypeOfPost(Enum):
    POST = 1
    VIDEO = 2
    PHOTO = 3
    COMMENT = 4
    REEL = 5
    GROUP = 6


class PostData:
    def __init__(self, timestamp: int, reaction: str, url: str, poster: str, post_id: str):
        self.timestamp = timestamp
        self.reaction = reaction
        self.url = url
        self.poster = poster
        self.post_id = post_id

        ## the fields below need to be updated manually by the post scraper
        self.post_text = ""
        self.translated_post_text = ""
        self.post_images: list[str] = []
        self.post_videos: list[str] = []

    def __str__(self):
        return f"""Hello I was done on {datetime.fromtimestamp(self.timestamp)} and it was a {self.reaction} 
reaction done on the URL: {self.url} that was posted by {self.poster}"""

    def __repr__(self) -> str:
        return f"self.url={self.url}"

    def get_json_format(self) -> JSONformat:
        return {
            "timestamp": str(self.timestamp),
            "reaction": self.reaction,
            "url": self.url,
            "poster": self.poster,
            "post_id": self.post_id,
            "post_text": self.post_text,
            "translated_post_text": self.translated_post_text,
            "post_images": self.post_images,
            "post_videos": self.post_videos,
        }

    @classmethod
    def make_postdata_from_json(cls, json_data: JSONformat):
        timestamp: int = int(json_data["timestamp"]) if isinstance(json_data["timestamp"], str) else 0
        reaction        = json_data["reaction"]  if isinstance(json_data["reaction"], str) else ""
        url             = json_data["url"]       if isinstance(json_data["url"], str) else ""
        poster          = json_data["poster"]    if isinstance(json_data["poster"], str) else ""
        post_id         = json_data["post_id"]   if isinstance(json_data["post_id"], str) else ""
        post_text       = json_data["post_text"]
        translated_post_text = json_data["translated_post_text"]
        post_images = json_data["post_images"]
        post_videos = json_data["post_videos"]
        data = cls(timestamp,
                   reaction,
                   url,
                   poster,
                   post_id)
        data.post_text = [unidecode(text) for text in post_text] if type(post_text) == list[str] else unidecode(post_text)
        data.translated_post_text = translated_post_text
        data.post_images = post_images
        data.post_videos = post_videos

        return data

    @property
    def url_post_type(self) -> TypeOfPost:
        if "comment_id" in self.url:
            return TypeOfPost.COMMENT
        elif "photo.php" in self.url or "/photo/" in self.url:
            return TypeOfPost.PHOTO
        elif "/videos/" in self.url or "/watch/" in self.url:
            return TypeOfPost.VIDEO
        elif "/reel/" in self.url:
            return TypeOfPost.REEL
        elif "/groups/" in self.url:
            return TypeOfPost.GROUP
        else:
            return TypeOfPost.POST
    
    @classmethod
    def test_link(cls, url_to_test: str) -> Self:

        return cls(1, "testing", url_to_test, "poster_testing", "post_id_testing")

@dataclass(frozen=True)
class Tags:
    _see_more_caption_class_tags: str
    _text_tags: str
    _secondary_text_tags: str
    _container_tags: str

    @property
    def text_tags(self) -> list[str]:
        return self._text_tags.split(" ")
    
    @property
    def secondary_text_tags(self) -> list[str]:
        return self._secondary_text_tags.split(" ")

    @property
    def see_more_caption_class_tags(self) -> list[str]: ## only gets unique tags
        return [t for t in self._see_more_caption_class_tags.split(" ") \
                if t not in self._text_tags.split(" ")]

    @property
    def see_more_intersect_tags(self) -> list[str]:
        intersect = [t for t in self._see_more_caption_class_tags.split(" ") \
                     if t in self._text_tags.split(" ")]
        return intersect

    @property
    def container_tags(self) -> list[str]:
        return self._container_tags.split(" ")
    