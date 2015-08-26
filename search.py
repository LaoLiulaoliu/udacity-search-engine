#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

# data structure {word: {url: {next_word1: None, next_word2: None, ...}, url2:{next_word1: None, next_word2: None,...}}, word2: ...}



def swap(url_rank, left, right):
    if left == right: return
    tmp = url_rank[left]
    url_rank[left] = url_rank[right]
    url_rank[right] = tmp

def quicksort(url_rank, left, right):
    if left >= right: return
    i = left
    j = right
    # i += 1 bug fixed
    while (i < j):
        while (url_rank[i][1] <= url_rank[left][1]):
            i += 1
            if i > j: break # avoid left exceed the right boundary
        while (url_rank[j][1] >= url_rank[left][1]):
            j -= 1
            if i > j: break
        if (i < j): # i > left; j < left;
            swap(url_rank, i, j)
    swap(url_rank, left, j)
    quicksort(url_rank, left, j-1)
    quicksort(url_rank, j+1, right)


def ordered_search(index, ranks, keyword):
    ''' Search one word, result is sorted by rank. '''
    if keyword not in index:
        return []
    result = []
    for url in index[keyword]:
        result.append( (url, ranks[url]) )
    quicksort(result, 0, len(result)-1)
    return [result[i][0] for i in range(len(result)-1, -1, -1)]


def lucky_search(index, ranks, keyword):
    ''' Search one word, result is the highest rank url. '''
    if keyword not in index:
        return []
    high = 0
    best_link = ''
    for url in index[keyword]:
        if ranks[url] >= high:
            high = ranks[url]
            best_link = url
    return best_link


def lack_or_notcontinuation(union):
    query_num_count = {}
    for word, url_dict in union.items():
        for url in url_dict:
            if url in query_num_count:
                query_num_count[url] += 1
            else:
                query_num_count[url] = 1
    result = []
    for url in query_num_count:
        result.append( (url, query_num_count[url]) )
    quicksort(result, 0, len(result)-1)
    return [result[i][0] for i in range(len(result)-1, -1, -1)]

def multi_search(index, ranks, query):
    ''' query [word1, word2, word3, ...]
        when len(query) >= 2,
        if any word in 'query' not in 'index', called 'lack'. travel all url, count the NO. of different word in this url
        else if 'query' not continuous in all page, called 'not continuation'. travel all url, count the NO. of different word in this url
        else if 'query' continuous in some page.
    '''

    length = len(query)
    if length == 0:
        return []
    elif length == 1:
        return ordered_search(index, ranks, query[0])

    # query words more than two
    union = {}
    lack_flag = False
    for word in query:
        if word not in index:
            lack_flag = True
        else:
            union.update({word: index[word]})

    # print(union)
    # {word: {url: {next_word1: None, next_word2: None, ...}, url2:{next_word1: None, next_word2: None,...}}, word2: ...}
    if lack_flag:
        if not union: # not even find one word
            return []
        return lack_or_notcontinuation(union)
    else:
        url_gather = union[query[0]] # {url: {next_word1: None, next_word2: None, ...}, url2:{next_word1: None, next_word2: None,...}}
        not_continuation = False
        # travel all words, eliminate url do not have continuous words
        for i in range(len(query)-1):
            middle = {}
            for url, word_dict in url_gather.items(): # a[url, word]
                if query[i+1] in word_dict:
                    # if query[i+1] is the last word in url, structure is url:{}
                    middle[url] = union[query[i+1]][url] # (b[url] = b.word)  and a.url == b.url
            if not middle:
                not_continuation = True
                break
            url_gather = middle
        if not_continuation:
            return lack_or_notcontinuation(union)

        # sort urls, add urls which not contain all words
        result = []
        for url in url_gather: # every word in the last gather's urls
            result.append( (url, ranks[url]) )
        quicksort(result, 0, len(result)-1)
        top = [result[i][0] for i in range(len(result)-1, -1, -1)]
        for word, url_dict in union.items():
            for url in url_dict:
                if url not in top: top.append(url)
        return top
