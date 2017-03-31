from ..util import load_words, load_ground_truth, load_word_pairs, base_dir
from ..evaluation import web_jaccard, web_overlap, web_dice, web_pmi, spearman_correlation
import os
import numpy as np

def load_word_cnt(filepath):
    ret = {}
    for line in file(filepath):
        p = line.strip().split('\t')
        w = p[0]
        cnt = int(p[1])
        ret[w] = cnt
    return ret

def calc(func, word_cnt, word_pair_cnt):
    outf = file(os.path.join(base_dir, 'similarity/page_cnt_%s.txt' %func.__name__), 'w')
    word_pairs = load_word_pairs()
    indices = []
    idx = 0
    sims = []
    for w1, w2 in word_pairs:
        p = word_cnt[w1]
        q = word_cnt[w2]
        pq = word_pair_cnt[w1 + " " + w2]
        if p == 0 or q == 0 or pq == 0:
            sim = 0
        else:
            sim = func(p, q, pq)
            indices.append(idx)
        idx += 1
        outf.write("%s %s %.6f\n" %(w1, w2, sim))
        sims.append(sim)
    outf.close()
    print "size = %d" %(len(indices))
    indices = np.array(indices)
    ground_truth = load_ground_truth()[indices]
    sims = np.array(sims)[indices]

    correlation = spearman_correlation(ground_truth, sims)
    print "%s correlation = %.6f" %(func.__name__, correlation)


if __name__ == "__main__":
    word_cnt = load_word_cnt(os.path.join(base_dir, "bing_search_result/cnt.tsv"))
    word_pair_cnt = load_word_cnt(os.path.join(base_dir, "bing_search_result/word_pair_cnt.tsv"))

    funcs = [web_jaccard, web_overlap, web_dice, web_pmi]
    for func in funcs:
        calc(func, word_cnt, word_pair_cnt)
    


