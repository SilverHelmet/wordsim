import sys
from ..util import base_dir, load_words
import os
import glob
import re

id_pattern = re.compile(r'id="(?P<doc_id>\d+)"')


def stat(filepath, words, outf):
    global id_pattern
    docid = None

    print "stat [%s]" %filepath
    for line in file(filepath):
        if line.startswith("<doc"):
            res = id_pattern.search(line)
            if res is None:
                continue
            docid = res.group('doc_id')
            outf.write('\n' + docid + '\t')
        elif line.startswith("</doc>"):
            docid = None
        else:
            if docid is None:
                continue
            for word in line.strip().split(" "):
                word = word.strip(',').strip('.')
                if word in words:
                    outf.write(words[word] + " ")

if __name__ == "__main__":
    word_list = load_words()
    words = {}
    for idx, word in enumerate(word_list):
        words[word] = str(idx)
    wiki_dir = os.path.join(base_dir,  'enwiki')
    if len(sys.argv) >= 2:
        wiki_dir = sys.argv[1]
    out_dir = os.path.join(base_dir, "result")
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    outf = file(os.path.join(out_dir, "oc.tsv"), 'w')
    for filepath in glob.glob(wiki_dir + "/*/wiki*"):
        stat(filepath, words, outf)
    outf.close()
        
