import numpy as np


def spearman_class(x):
    values = sorted(x)
    r_values = sorted(x, reverse = True)
    class_x = []
    for v in x:
        p1 = values.index(x)
        p2 = len(values) - 1 - r_values.index(x)
        class_x.append((p1 + p2) / 2.0)
    return np.array(class_x)

def spearman_correlation(x, y):
    x = spearman_class(x)
    y = spearman_class(y)
    n = len(x) + 0.0
    p = 1.0 - 6.0 * ((x - y) ** 2).sum() / (n * (n*n - 1))
    return p

def cosine(x, y):
    return (x * y).sum() / np.sqrt((x ** 2).sum() * (y ** 2).sum())

def jaccard(x, y):
    z = np.stack(x, y)
    minv = z.min(axis = 0).sum()
    maxv = z.max(axis = 0).sum()
    return (minv + 0.0) / (maxv)

def dice(x, y):
    z = np.stack(x, y)
    minv = z.min(axis = 0).sum()
    return minv * 2.0 / z.sum()

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
    
