# import zipfile
import pymorphy2
import os
from bs4 import BeautifulSoup

# import re
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords

morph = pymorphy2.MorphAnalyzer()
parser = 'html.parser'


def read_index(index_file_path):
    index_dict = {}
    print(os.curdir)
    with open(index_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            items = line.split(": ")
            index_dict[items[0]] = items[1].split()
    return index_dict


DIR_PATH = "infosearch/services"
DB_PATH = "infosearch/services/data"

os.chdir(DIR_PATH)
index = read_index("./inverted_index.txt")


def bool_search(query):
    parts = query.split()
    for i in range(1, len(parts), 2):
        if parts[i].lower() != 'or' and parts[i].lower() != 'and':
            return

    if len(parts) % 2 == 0:
        return

    normal_form = morph.parse(parts[0])[0].normal_form

    if normal_form in index:
        # print(index[normal_form])
        result = set(index[normal_form])
    else:
        result = set()

    for i in range(2, len(parts), 2):
        normal_form = morph.parse(parts[i])[0].normal_form
        if normal_form in index:
            print(index[normal_form])
            if parts[i - 1] == 'and':
                result = result.intersection(index[normal_form])
            else:
                result = result.union(index[normal_form])

    return result


def get_pages(indices: set):
    if not indices: return []

    db = os.listdir("data")
    # files = [db[int(idx)] for idx in indices]
    pages = []

    for idx in indices:
        filename = db[int(idx)]
        with open(f"data/{filename}", "r", encoding="utf-8") as file:
            content = file.read()
            soup = BeautifulSoup(content, parser)
            # TODO: not only og:
            # TODO: process default value
            title = soup.find("meta", property="og:title")['content']
            url = soup.find("meta", property="og:url")['content']
            description = soup.find("meta", property="og:description")['content']
            page_meta = {
                "title": title,
                "description": description,
                "url": url,
            }
        pages.append(page_meta)

    return pages
