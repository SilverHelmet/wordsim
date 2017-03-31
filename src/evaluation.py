import numpy as np
from .util import load_word_pairs, load_ground_truth, load_words


def spearman_class(x):
    values = sorted(x)
    r_values = sorted(x, reverse = True)
    class_x = []
    for v in x:
        p1 = values.index(v)
        p2 = len(values) - 1 - r_values.index(v)
        class_x.append((p1 + p2) / 2.0)
    return np.array(class_x)

def spearman_correlation(x, y):
    x = spearman_class(x)
    y = spearman_class(y)
    n = len(x) + 0.0
    p = 1.0 - 6.0 * ((x - y) ** 2).sum() / (n * (n*n - 1))
    return p

def cosine(x, y):
    z = (x * y).sum() + 0.0
    mu = (x ** 2).sum() * (y ** 2).sum()
    return z  / np.sqrt(mu + 0.000001)

def jaccard(x, y):
    z = np.stack([x, y])
    minv = z.min(axis = 0).sum()
    maxv = z.max(axis = 0).sum() + 0.000001
    return (minv + 0.0) / maxv

def dice(x, y):
    z = np.stack([x, y])
    minv = z.min(axis = 0).sum()
    return minv * 2.0 / (z.sum()  + 0.000001)

def web_jaccard(p, q, pq, c = 5):
    if pq <= c:
        return 0
    return (pq + 0.0) / (p + q - pq)

def web_overlap(p, q, pq, c = 5):
    if pq <= 5:
        return 0
    return (pq + 0.0) / min(p, q)

def web_dice(p, q, pq, c = 5):
    if pq <= c:
        return 0
    return (2.0 * pq) / (p + q)

def web_pmi(p, q, pq, c = 5, N = 1.0):
    p = p / N
    q = q / N
    pq = pq / N
    return np.log2(pq / (p * q))

def ESA_wiki(func):
    word_pairs = load_word_pairs()
    ground_truth = load_ground_truth()
    words = load_words()
    wv = np.load('result/word_ESA_vector.npy')
    similarity = []
    for w1, w2 in word_pairs:
        w1 = words.index(w1)
        w2 = words.index(w2)
        similarity.append(func(wv[w1], wv[w2]))
    similarity = np.array(similarity)
    return spearman_correlation(ground_truth, similarity)
        
    

if __name__ == '__main__':
    print ESA_wiki(cosine)
    
        
    
