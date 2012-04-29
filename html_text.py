#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

from lxml import etree


def html_text(content):
    ''' parse all the text in html using xpath '''
    parser = etree.XMLParser(recover=True)
    tree = etree.fromstring(content, parser)
    text = tree.xpath('//text()')
    for sentence in text:
        if not sentence or sentence.isspace():
            continue
        yield sentence.strip()


def html_content(content):
    ''' parse all the text in html,
        not perform well.
    '''
    ignore_tags = ('script','noscript','style')
    result = []
    parser = etree.XMLParser(recover=True)
    tree = etree.fromstring(content, parser)
    for element in tree.iter():
        if element.tag in ignore_tags:
            continue
        plain = element.text
        if not plain or plain.isspace():
            continue
        result.append(plain)
    return result
#    optional code(no tag):
#    root = tree.getroot()
#    for element in tree.itertext():
#        if not element or element.isspace():
#            continue
#        result.append(element)



if __name__ == '__main__':
    html_doc = """
    <html><head><title>The Dormouse's story</title></head>

    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>

    <p class="story">...</p>
    """

    import bs4
    soup = bs4.BeautifulSoup(html_doc)
    s = soup.get_text().splitlines() # ok
    print(s)
    better_s = [x for x in soup.stripped_strings] # best
    print(better_s, '\n\n')

    own = html_content(html_doc) # worse
    print(own)
    better_own = list(html_text(html_doc)) # same best
    print(better_own)
