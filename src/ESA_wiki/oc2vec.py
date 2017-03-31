import sys
from ..util import base_dir, load_words, load_word_pairs, load_ground_truth
import os
import numpy as np
from ..evaluation import cosine, jaccard, dice, spearman_correlation

class WordVectors:
    word_df_bias = 5
    def __init__(self, word_size, doc_size):
        self.vectors = [[0] * doc_size for _ in range(word_size)]
        self.index = -1
        self.doc_size = doc_size

    def expand(self):
        self.index += 1

    def add_doc(self, line):
        line = line.strip("\n")
        if line == "":
            return
        self.expand()
        p = line.strip().split("\t")
        if len(p) < 2:
            return
        words = p[1].split(' ')
        words = map(int, words)
        for word in words:
            self.vectors[word][self.index] += 1

    def calc_tfidf(self):
        self.vectors = np.array(self.vectors)
        df = np.not_equal(self.vectors, 0).sum(1) + WordVectors.word_df_bias
        idf = np.log((self.doc_size + 0.0) / df)
        idf = np.expand_dims(idf, 1)
        self.vectors = idf * self.vectors
        
    def finish(self):
        assert self.index == len(self.vectors[0]) - 1
        self.calc_tfidf()

def load(filepath, words, doc_size):
    w_vecs = WordVectors(len(words), doc_size) 
    for idx, line in enumerate(file(filepath)):
        if idx % 10000 == 0:
            print "\t load cnt = %d" %idx
        w_vecs.add_doc(line)

    w_vecs.finish()
    return w_vecs.vectors

    

        

if __name__ == "__main__":
    words = load_words()
    # doc_size = 5347267
    doc_size = 754
    word_vec = load(os.path.join(base_dir, 'result/oc.tsv'), words, doc_size)
    print "start calc similarity"

    sim_out_dir = os.path.join(base_dir, "similarity")
    if not os.path.exists(sim_out_dir):
        os.mkdir(sim_out_dir)
    
    funcs = [cosine, jaccard, dice]
    for func in funcs:
        func_name = func.__name__
        outf = file(sim_out_dir + "/ESA_wiki_%s.tsv" %func_name, 'w')
        word_pairs = load_word_pairs()
        sims = []
        cnt = 0
        for w1, w2 in word_pairs:
            cnt += 1
            print "eval = %d" %cnt
            w1_idx = words.index(w1)
            w2_idx = words.index(w2)
            sim = func(word_vec[w1_idx], word_vec[w2_idx])
            sims.append(sim)
            outf.write("%s %s %.6f\n" %(w1, w2, sim))
        outf.close()

        sims = np.array(sims)
        ground_truth = load_ground_truth()
        print "correlation_%s" %func_name, spearman_correlation(ground_truth, sims)


    # np.save(os.path.join(base_dir, 'result/word_ESA_vector'), word_vec)
