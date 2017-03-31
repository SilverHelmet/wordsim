from ..util import load_word_pairs, load_ground_truth, base_dir
from ..evaluation import spearman_correlation
import os
import numpy as np

def count_word(abs_filepath, count_word, N):
    hit = False
    hit_cnt = 0
    count_word = count_word.lower()
    for idx, line in enumerate(file(abs_filepath)):
        if idx == N:
            hit = True
            break
        words = "\t".join(line.strip().split('\t')[1:]).split(" ")
        for word in words:
            word = word.strip('.').strip(',').strip('"').lower()
            if word == count_word:
                hit_cnt += 1
        
    if hit:
        return hit_cnt
    else:
        return -1



def calc_CODC(x, y, data_dir, N = 100):
    x_at_x = count_word(os.path.join(data_dir, '%s/abstracts.tsv' %x), x, N)
    y_at_x = count_word(os.path.join(data_dir, '%s/abstracts.tsv' %x), y, N)
    y_at_y = count_word(os.path.join(data_dir, '%s/abstracts.tsv' %y), y, N)
    x_at_y = count_word(os.path.join(data_dir, '%s/abstracts.tsv' %y), x, N)
    if x_at_x == -1 or y_at_y == -1:
        return -1
    if x_at_y == 0 or y_at_x == 0:
        return 0
    x_at_x += 0.0
    y_at_y += 0.0
    CODC = np.exp(np.log(y_at_x / x_at_x) + np.log(x_at_y / y_at_y))
    return CODC
        

if __name__ == "__main__":
    data_dir = os.path.join(base_dir, 'bing_search_result')
    word_pairs = load_word_pairs()
    ground_truth = load_ground_truth()
    indices = []
    idx = 0
    sims = []
    sim_outf = file(os.path.join(base_dir, 'similarity/CODC_sim.txt'), 'w')
    for w1, w2 in word_pairs:
        sim = calc_CODC(w1, w2, data_dir)
        if sim == -1:
            pass
        else:
            indices.append(idx)
        sims.append(sim)

        sim_outf.write("%s %s %.6f\n" %(w1, w2, sim))
        idx += 1
    sim_outf.close()

    print "successful size = %d" %(len(indices))

    indices = np.array(indices)
    sims = np.array(sims)[indices]
    ground_truth = ground_truth[indices]

    correlation = spearman_correlation(ground_truth, sims)    
    print "CODC correlation = %f" %correlation  

