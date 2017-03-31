from .util import base_dir, load_ground_truth, load_word_pairs
from .evaluation import spearman_correlation
import gensim
import numpy as np
import os

if __name__ == "__main__":
    word_pairs = load_word_pairs()
    ground_truth = load_ground_truth()
    sim_outf = file(os.path.join(base_dir, 'similarity/word2vec_cosine.txt'), 'w')
    model = gensim.models.KeyedVectors.load_word2vec_format("~/data/GoogleNews-vectors-negative300.bin", binary = True)
    sims = []
    successful_indecies = []
    print "test size = %d" %(word_pairs)
    idx = 0
    for w1, w2 in word_pairs:
        if w1 in model.vocab and w2 in model.vocab:
            sim = model.similarity(w1, w2)
            successful_indecies.append(idx)
        else:
            sim = 0
            print "error word %s, %s" %(w1, w2)
        sim_outf.write("%s %s %.6f\n" %(w1, w2, sim))
        sims.append(sim)
        idx += 1
    sim_outf.close()
    successful_indecies = np.array(successful_indecies)

    ground_truth = ground_truth[successful_indecies]
    sims = np.array(sims)[successful_indecies]
    
    print "successful size = %d" %len(successful_indecies)
    correlation = spearman_correlation(ground_truth, sims)



        
        
        
