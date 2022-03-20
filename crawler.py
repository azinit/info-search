import os

import requests
import json
import shutil

from lib import Logger

base_url = "https://vc.ru"
dist_dir = "data"
logger = Logger(name="crawler")


def ensure_clean_dist():
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    os.mkdir(dist_dir)


def crawl_website(from_id: int, amount: int):
    logger.log("1/3 CRAWLING".center(30, "="))
    index = {}

    article_id = from_id
    while len(index) < amount:
        # Calc article properties
        article_url = f"{base_url}/{article_id}"
        article_pathname = f"{dist_dir}/{article_id}.html"
        # Download article content
        response = requests.get(article_url)
        # Save article
        if response.status_code == 200:
            with open(article_pathname, "w", encoding="utf-8") as article_file:
                article_file.write(response.text)
            index[article_id] = article_url
        # Iterate
        article_id += 1
        logger.log(f"Progress: article=[{article_id}] index=[{len(index)}/{amount}] // {response.status_code}")
    return index


def save_index(index):
    logger.log("2/3 SAVING INDEX".center(30, "="))
    # Save text
    logger.log("Save index.txt...")
    with open("index.txt", "w", encoding="utf-8") as index_txt:
        content = [f"{key} {index[key]}" for key in index.keys()]
        index_txt.write("\n".join(content))
    # Save json
    logger.log("Save index.json...")
    with open("index.json", "w", encoding="utf-8") as index_json:
        json.dump(index, index_json, indent=4)


def archive_dump():
    logger.log("3/3 MAKING ARCHIVE".center(30, "="))
    shutil.make_archive('выкачка', 'zip', dist_dir)


if __name__ == '__main__':
    ensure_clean_dist()  # Commentable
    index = crawl_website(from_id=383300, amount=100)
    save_index(index)
    archive_dump()
