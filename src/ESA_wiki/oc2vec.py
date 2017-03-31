import sys
from ..util import base_dir, load_words
import os

def WordVectors:
    def __init__(self, word_size, doc_size):
        self.vectors = [[0] * doc_size for _ in range(size)]
        self.index = -1

    def expand(self):
        self.index += 1

    def add_doc(self, line):
        self.expand()
        p = line.strip().split("\t")
        words = p[1].split(' ')
        words = map(int, words)
        for word in words:
            self.vectors[word][self.index] += 1

    def finish(self):
        assert self.index == len(self.vectors[0]) - 1

def load(filepath, words, doc_size):
    w_vecs = WordVectors(len(words), doc_size) 
    for line in filepath:
        p = line.strip().split('\t')
        

if __name__ == "__main__":
    words = load_words()
    doc_siez = 754
    word_vec = load(os.path.join(base_dir, 'result/oc.tsv'), words)