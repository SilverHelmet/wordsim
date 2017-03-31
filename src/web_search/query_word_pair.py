from .query_util import call
from ..util import base_dir, load_word_pairs
from .parse import parse_cnt
from bs4 import BeautifulSoup
import os

if __name__ == "__main__":
    word_pairs = load_word_pairs()
    cnt_outfilepath = os.path.join(base_dir, 'bing_search_result/word_pair_cnt.txt')
    first = 1
    for w1, w2 in word_pairs:
        query = "%s %s" %(w1, w2)
        html = call(query, first)
        soup = BeautifulSoup(html, 'html.parser')
        cnt = parse_cnt(soup)
        print "%s cnt = %d" %(query, cnt)

        outf = file(cnt_outfilepath, 'a')
        outf.write(query + "\t" + str(cnt) + '\n')
        outf.close()
