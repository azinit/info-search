import math
import os
import zipfile
from bs4 import BeautifulSoup

from index_creating import create_inverted_index_tokens, save_inverted_index, read_index, parser, morph, \
    get_list_tokens


def get_tf(q, tokens):
    return tokens.count(q) / float(len(tokens))


def get_idf(q, index, docs_count=100):
    return math.log(docs_count / float(len(index[q])))


def lem(word):
    return morph.parse(word.replace("\n", ""))[0].normal_form


def get_result(zip_f, lemmas_index, tokens_index):
    for i, file in enumerate(zip_file.filelist):
        content = zip_f.open(file)
        text = BeautifulSoup(content, parser).get_text()
        # get tokens from file
        tokens = get_list_tokens(text)
        # lemmas
        lemmas = list(map(lem, tokens))

        res_tokens = []
        res_lemmas = []

        # for tokens
        for token in set(tokens):
            tf = get_tf(token, tokens)
            idf = get_idf(token, tokens_index)
            res_tokens.append(f"{token} {idf} {tf * idf}")

        # for lemmas
        for lemma in set(lemmas):
            tf = get_tf(lemma, lemmas)
            idf = get_idf(lemma, lemmas_index)
            res_lemmas.append(f"{lemma} {idf} {tf * idf}")

        with open(f"tokens_res/{i}.txt", "w") as token_f:
            token_f.write("\n".join(res_tokens))

        with open(f"lemmas_res/{i}.txt", "w") as lemma_f:
            lemma_f.write("\n".join(res_lemmas))

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

if __name__ == '__main__':
    # zip file path
    zip_file_path = "выкачка.zip"
    zip_file = zipfile.ZipFile(zip_file_path, "r")

    lemmas_index_path = "inverted_index.txt"
    tokens_index_path = "inverted_index_tokens.txt"

    # create inverted index tokens
    inverted_index_tokens = create_inverted_index_tokens(zip_file)

    # write to file
    save_inverted_index(tokens_index_path, inverted_index_tokens)

    # read files
    read_inverted_index = read_index(lemmas_index_path)
    read_inverted_index_tokens = read_index(tokens_index_path)

    get_result(zip_file, read_inverted_index, read_inverted_index_tokens)
