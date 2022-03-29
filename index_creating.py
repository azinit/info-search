import zipfile
import pymorphy2
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from lib import Logger

morph = pymorphy2.MorphAnalyzer()
parser = 'html.parser'
logger = Logger('indexing')


def normalize_tokens(tokens):
    res = []
    # leave just russian words
    for token in tokens:
        if token.lower() not in stopwords.words("russian") and re.compile("^[а-я]+$").match(token.lower()):
            res.append(token.lower())
    # return unique tokens
    return set(res)


def list_normalize_tokens(tokens):
    res = []
    # leave just russian words
    for token in tokens:
        if token.lower() not in stopwords.words("russian") and re.compile("^[а-я]+$").match(token.lower()):
            res.append(token.lower())
    # return unique tokens
    return list(res)


def get_tokens(text):
    tokens = word_tokenize(text.replace('.', ' '))
    return normalize_tokens(tokens)


def get_list_tokens(text):
    tokens = word_tokenize(text.replace('.', ' '))
    return list_normalize_tokens(tokens)


def create_inverted_index(zip_f):
    logger.log("CREATE INVERTED_INDEX".center(64, "="))
    # get lemmas from lemmas.txt file
    lemmas_file = open("lemmas.txt", "r", encoding="utf-8")
    index = {}
    for row in lemmas_file:
        lemma = row.split(':')[0]
        index[lemma] = []

    # range zip file with data (html)
    for i, file in enumerate(zip_f.filelist):
        content = zip_f.open(file)
        text = BeautifulSoup(content, parser).get_text()
        # get tokens from file
        tokens = get_tokens(text)
        for token in tokens:
            normal_form = morph.parse(token)[0].normal_form
            if normal_form in index:
                index[normal_form].append(i)
    # return inverted index
    return index


def create_inverted_index_tokens(zip_f):
    logger.log("CREATE INVERTED_INDEX_TOKENS".center(64, "="))
    index = {}

    # range zip file with data (html)
    for i, file in enumerate(zip_f.filelist):
        content = zip_f.open(file)
        text = BeautifulSoup(content, parser).get_text()
        # get tokens from file
        tokens = set(get_tokens(text))

        for token in tokens:
            if token in index:
                index[token].add(i)
            else:
                index[token] = {i}
    # return inverted index
    return index


def save_inverted_index(filename, ind):
    logger.log("SAVING INDEX".center(64, "="))

    inverted_index_file = open(filename, "a", encoding="utf-8")
    for i in ind:
        inverted_index_file.write(i + ": " + " ".join(map(lambda file_number: str(file_number), ind[i])) + "\n")
    inverted_index_file.close()


def bool_search(query, index):
    logger.log("BOOL SEARCHING".center(64, "="))

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

    # print(result)
    return result


def read_index(index_file_path):
    logger.log("READING INDEX".center(64, "="))

    index_dict = {}
    with open(index_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            items = line.split(": ")
            index_dict[items[0]] = items[1].split()
    return index_dict


if __name__ == '__main__':
    # zip file path
    zip_file_path = "выкачка.zip"
    zip_file = zipfile.ZipFile(zip_file_path, "r")

    # # create inverted index
    # inverted_index = create_inverted_index(zip_file)
    #
    # # write to file
    inverted_index_path = "inverted_index.txt"
    # save_inverted_index(inverted_index_path, inverted_index)

    # read inverted index
    read_inverted_index = read_index(inverted_index_path)

    # q = "буквально or новый стриминговый сервис"
    q = "буквально or абьюзер"
    results = bool_search(q, read_inverted_index)
    print(f"BoolSearch indices = {results}")
