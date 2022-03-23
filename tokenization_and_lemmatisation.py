import zipfile
import re
import pymorphy2
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def get_text(zip_f):
    text = ''
    parser = 'html.parser'
    for file in zip_f.filelist:
        content = zip_f.open(file)
        text += BeautifulSoup(content, parser).get_text()
    return text


def get_tokens(text):
    return word_tokenize(text.replace('.', ' '))


def normalize_tokens(tokens):
    res = []
    # leave just russian words
    for token in tokens:
        if token.lower() not in stopwords.words("russian") and re.compile("^[а-я]+$").match(token.lower()):
            res.append(token.lower())
    # return unique tokens
    return set(res)


def get_lemmas(file_with_tokens):
    morph = pymorphy2.MorphAnalyzer()
    file = open(file_with_tokens, "r")
    tokens = file.readlines()
    lemmas = {}

    # fill lemmas dictionary
    for token in tokens:
        token = token.replace("\n", "")
        normalized = morph.parse(token)[0].normal_form
        if normalized in lemmas:
            lemmas[normalized].append(token)
        else:
            lemmas[normalized] = [token]

    return lemmas


if __name__ == '__main__':
    # zip file path
    zip_file_path = "выкачка.zip"
    zip_file = zipfile.ZipFile(zip_file_path, "r")

    # text from file
    text_from_file = get_text(zip_file)

    # get tokens
    tkns = get_tokens(text_from_file)
    t = normalize_tokens(tkns)
    tokensWithNewLines = "\n".join(t)

    # write to file
    tokens_file = open("tokens.txt", "a")
    tokens_file.write(tokensWithNewLines)

    # get lemmas
    lmms = get_lemmas("tokens.txt")
    # write to file
    lemmas_file = open("lemmas.txt", "a")
    for l in lmms:
        lemmas_file.write(l + " " + " ".join(lmms[l]) + '\n')
    lemmas_file.close()
