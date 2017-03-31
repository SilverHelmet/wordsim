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
    a = soup.select('a.sb_pagN')
    if len(a) == 0:
        return 0
    a = a[0]
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
        title_div = title_div[0]
        href = title_div.select('h2 > a[target=_blank]')[0]['href'].encode('utf-8')
        abstract_div = li.select('div.b_caption')
        if len(abstract_div) == 0:
            continue
        abstract_div = abstract_div[0]
        abs_p = abstract_div.p
        if abs_p is None:
            continue
        abstract = abs_p.text.encode('utf-8')
        ret[href] = abstract
    return ret


if __name__ == "__main__":
    soup = BeautifulSoup(load('bing_search_result/cock_first=50.html'), 'html.parser')
    print parse_cnt(soup)
    print parse_next_page(soup)
    print parse_abstract(soup)['https://en.wikipedia.org/wiki/History_of_the_Internet']

