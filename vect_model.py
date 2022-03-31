import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import pymorphy2
import collections
from scipy import spatial


class VectorModel:
    def __init__(self):
        self.matrix, self.index, self.lemmas = self.get_matrix()

    def load_index(self):
        file = open('inverted_index.txt', 'r')
        lines = file.readlines()

        index = dict()
        lemmas = []
        for line in lines:
            line = line.replace('\n', '')
            pages = line.split(': ')[1].split(' ')
            index[line.split(':')[0]] = pages
            lemmas.append(line.split(':')[0])
        return lemmas, index

    def load_idf(self):
        file = open('lemmas_idf.txt', 'r')
        lines = file.readlines()

        idf = dict()
        for line in lines:
            line = line.replace('\n', '')
            idf[line.split(' ')[0]] = float(line.split(' ')[1])
        return idf

    def load_tf_idf(self, i):
        file = open("/lemmas_res/" + str(i) + ".txt", "r")
        lines = file.readlines()

        tf_idf = dict()
        for line in lines:
            line = line.replace('\n', '')
            tf_idf[line.split(' ')[0]] = line.split(' ')[2]
        return tf_idf

    def load_matrix(self):
        lemmas, index = self.load_index()

        matrix = np.zeros((217, len(index)))

        for i in range(1, 218):
            tf_idf = self.load_tf_idf(i)
            for lemma in tf_idf:
                matrix[i - 1][lemmas.index(lemma)] = tf_idf[lemma]

        matrix_file = open("m.txt", "a")
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix_file.write(str(matrix[i][j]) + " ")
            matrix_file.write("\n")
        matrix_file.close()
        return matrix, index, lemmas

    def get_matrix(self):
        lemmas, index = self.load_index()

        matrix = np.zeros((217, len(index)))

        file = open('m.txt', 'r')
        lines = file.readlines()

        for i in range(len(lines)):
            cols = lines[i].replace(' \n', '').split(' ')
            for j in range(len(cols)):
                matrix[i, j] = float(cols[j])

        return matrix, index, lemmas

    def get_lemmas(self, text):
        text_tokens = word_tokenize(text.replace('.', ' '))
        stop_words = stopwords.words("russian")
        lemmas = []
        morph = pymorphy2.MorphAnalyzer()
        r = re.compile("[а-я]")
        for token in text_tokens:
            if token not in stop_words and r.match(token) and len(token) > 1:
                lemmas.append(morph.parse(token)[0].normal_form)
        return lemmas

    def search(self, text):
        search_lemmas = self.get_lemmas(text.lower())
        idf = self.load_idf()

        words_frequency = collections.Counter(search_lemmas)

        vector = np.zeros(len(self.index))
        for lemma in self.index:
            if lemma in search_lemmas:
                vector[self.lemmas.index(lemma)] = (words_frequency[lemma] / float(len(self.index[lemma]))) * idf[lemma]

        texts = dict()
        for idx, row in enumerate(self.matrix):
            texts[idx + 1] = 1 - spatial.distance.cosine(vector, row)

        texts_sorted = dict(sorted(texts.items(), key=lambda item: item[1], reverse=True))
        texts_filtered = dict(filter(lambda b: b[1] > 0, texts_sorted.items()))
        list = []
        for t in texts_filtered:
            file = open('/data' + str(t) + '.html', 'r')
            list.append(str(t) + ". " + (file.readlines()[0])[:100] + "...")
        return list