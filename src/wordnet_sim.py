from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from .util import load_word_pairs, base_dir, load_ground_truth
from .evaluation import spearman_correlation
import os
import numpy as np

if __name__ == "__main__":
    word_pairs = load_word_pairs()
    path_sims = []
    wup_sims = []
    lin_sims = []
    path_sim_outf = file(os.path.join(base_dir, 'similarity/pathsim.txt'), 'w')
    wup_sim_outf = file(os.path.join(base_dir, 'similarity/wupsim.txt'), 'w')
    lin_sim_outf = file(os.path.join(base_dir, 'similarity/linsim.txt'), 'w')
    semcor_ic = wordnet_ic.ic('ic-semcor.dat')
    for w1, w2 in word_pairs:
        s1 = wn.synsets(w1)
        s2 = wn.synsets(w2)
        path_sim = 0
        wup_sim = 0
        lin_sim = 0
        for x in s1:
            for y in s2:
                sim = x.path_similarity(y)
                if sim is not None:
                    path_sim = max(path_sim, sim)
                if x.pos() == y.pos():
                    sim = x.lin_similarity(y, semcor_ic)
                    if sim is not None:
                        lin_sim = max(lin_sim, sim)
                sim = x.wup_similarity(y)
                if sim is not None:
                    wup_sim = max(wup_sim, sim)
                
        path_sim_outf.write("%s %s %.6f\n" %(w1, w2, path_sim))
        wup_sim_outf.write("%s %s %.6f\n" %(w1, w2, wup_sim))
        lin_sim_outf.write("%s %s %.6f\n" %(w1, w2, lin_sim))

        path_sims.append(path_sim)
        wup_sims.append(wup_sim)
        lin_sims.append(lin_sim)

    path_sims = np.array(path_sims)
    wup_sims = np.array(wup_sims)
    lin_sims = np.array(lin_sims)
    path_sim_outf.close()
    wup_sim_outf.close()
    lin_sim_outf.close()

    ground_truth = load_ground_truth()
    path_sim_correlation = spearman_correlation(ground_truth, path_sims)
    wup_sim_correlation = spearman_correlation(ground_truth, wup_sims)
    lim_sim_correlation = spearman_correlation(ground_truth, lin_sims)

    print "pathsim correlation = %f" %(path_sim_correlation)
    print "wupsim correlation = %f" %(wup_sim_correlation)
    print "linsim correlation = %f" %(lin_sim_correlation)
    

    
        



                

        
