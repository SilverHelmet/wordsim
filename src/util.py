import os
import numpy as np

def load_words():
    global data_dir
    words = set()
    for idx, line in enumerate(file(os.path.join(data_dir, 'combined.tab'))):
        if idx == 0:
            continue
        p = line.strip().split('\t')
        words.add(p[0])
        words.add(p[1])
    return sorted(words)

def load_word_pairs():
    global data_dir
    word_pairs = []
    for idx, line in enumerate(file(os.path.join(data_dir, 'combined.tab'))):
        if idx == 0:
            continue
        p = line.strip().split('\t')
        word_pairs.append((p[0], p[1]))
    return word_pairs

def load_ground_truth():
    global data_dir
    x = []
    for idx, line in enumerate(file(os.path.join(data_dir, 'combined.tab'))):
        if idx == 0:
            continue
        p = line.strip().split("\t")
        x.append(float(p[2]))
    return np.array(x)



base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_dir = os.path.join(base_dir, "wordsim353")


if __name__ == "__main__":
    words = load_words()
    word_pairs = load_word_pairs()
    print "#word = %d" %len(words)
    print "#word_pair = %d" %len(word_pairs)
    print words[139]
    print sorted(load_ground_truth())
