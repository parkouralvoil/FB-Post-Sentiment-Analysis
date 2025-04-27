
import json
import re

class Word():
    def __init__(self, tag: str, lang: str, word: str):
        self._tag = tag
        self._lang = lang
        self._word = word

    @property
    def tag(self):
        return self._tag

    @property
    def lang(self):
        return self._lang

    @property
    def word(self):
        return self._word

    def __str__(self):
        return f"{self._word}: {self._lang} - {self._tag}"

def populate_words_db(word_arr: list[Word]):
    with open('words.json', 'r') as file:
        data = json.load(file)

        for word_data in data:
            word = Word(word_data['tag'], word_data['lang'], word_data['word'])
            word_arr.append(word)

word_db: list[Word] = []
populate_words_db(word_db)
word_db_only_words: list[str] = [word.word for word in word_db]
bad_words_db: list[Word] = [word for word in word_db if word.tag == "Bad"]

def uncensor_word(word: str):
    censored_word = word.lower()
    possible_matches = [
        word.word for word in bad_words_db if len(word.word) == len(censored_word)
    ]
    
    for bad_word in possible_matches:
        match = True
        for i, char in enumerate(censored_word):
            if char != "*" and char != bad_word[i]:
                match = False
                break
        if match:
            return bad_word  # Returns first match found

    return word

def uncensor_text(text: str):    
    words = re.findall(r'\b[\w*]+\b', text)
    uncensored_words = [uncensor_word(word) for word in words]
    return " ".join(uncensored_words) 

def filter_text(text: str):
    uncensored_text = uncensor_text(text)
    only_alphabet_text = re.sub(r'[^a-zA-Z ]', '', uncensored_text).split(" ")
    only_dictionary_words = [word.lower() for word in only_alphabet_text if word.lower() in word_db_only_words]
    return " ".join(only_dictionary_words)

