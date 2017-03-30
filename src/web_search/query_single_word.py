from .query_util import call
from ..util import base_dir, load_words
import os
from bs4 import BeautifulSoup
from .parse import parse_cnt, parse_next_page, parse_abstract
import time



def query(word):
    global cnt_file
    print "query %s" %word
    html_out_dir = os.path.join(base_dir, "bing_search_result/%s" %word)
    if not os.path.exists(html_out_dir):
        os.mkdir(html_out_dir)
    
    abstract = {}
    first = 1
    while first < 120:
        time.sleep(3)
        print "\tquery word = %s first = %d" %(word, first)
        html = call(word, first)

        outf = file(os.path.join(html_out_dir, "%s_first=%d.html" %(word, first)), 'w')
        outf.write(html)
        outf.close()

        soup = BeautifulSoup(html, 'html.parser')
        if first == 1:
            cnt = parse_cnt(soup)
            outf = file(cnt_file, 'a')
            outf.write("%s\t%d\n" %(word, cnt))
            outf.close()
            if cnt == 0:
                outf = file(os.path.join(base_dir, 'bing_saerch_result/error.txt'), 'a')
                outf.write(word + '\n')
                outf.close()
                break

        new_abstracts = parse_abstract(soup)
        for url in new_abstracts:
            abstract[url] = new_abstracts[url]


        next_pg = parse_next_page(soup)
        first = next_pg

    abs_outf = file(os.path.join(html_out_dir, 'abstracts.tsv'), 'w')
    for url in abstract:
        abs_outf.write(url + '\t' + abstract[url] + '\n')
    abs_outf.close()

        

if __name__ == "__main__":
    words = load_words()
    cnt_file = os.path.join(base_dir, 'bing_search_result/cnt.tsv')
    for word in words:
        query(word)

