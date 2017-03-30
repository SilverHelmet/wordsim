from bs4 import BeautifulSoup

def load(filepath):
    h = "".join(file(filepath, 'r').readlines())
    return h


def parse_cnt(soup):
    content = soup.select('span.sb_count')
    if len(content) == 0:
        return 0
    content = content[0].string.strip()
    num = content.split(" ")[0]
    num = int(num.replace(",",''))
    return num

def parse_next_page(soup):
    a = soup.select('a.sb_pagN')[0]
    x = a['href']
    pairs = a['href'].split('?')[1].split("&")
    for key_value in pairs:
        key, value = key_value.split("=")
        if key == 'first':
            return int(value)

def parse_abstract(soup):
    abstract_li = soup.select('li.b_algo')
    ret = {}
    for li in abstract_li:
        title_div = li.select('div.b_title')
        if len(title_div) == 0:
            continue
        href = title_div.select('h2 > a[target=_blank]')[0]['href'].encode('utf-8')
        abstract_div = li.select('div.b_caption')[0]
        abstract = abstract_div.p.text.encode('utf-8')
        ret[href] = abstract
    return ret


if __name__ == "__main__":
    soup = BeautifulSoup(load('bing_search_result/Arafat_first=67.html'), 'html.parser')
    print parse_cnt(soup)
    print parse_next_page(soup)
    print parse_abstract(soup)['https://en.wikipedia.org/wiki/History_of_the_Internet']

