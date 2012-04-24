#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

# data structure {word: {url: {next_word1: None, next_word2: None, ...}, url2:{next_word1: None, next_word2: None,...}}, word2: ...}
import queue
import threading
import porter_stemming

class indexing(object):
    def __init__(self):
        self.index = {}
        self.index_lock = threading.Lock()
        self.pstem = porter_stemming.PorterStemmer()


    def add_to_index(self, keyword, nextword, url):
        ''' One word appeared more than once in a url.
            If this word have different next word,we can distinguish them,
            else we mix them up(not record their exact position).
        '''
        if keyword in self.index:
            if url in self.index[keyword]:
                if nextword: self.index[keyword][url][nextword] = None # two adjacent words appear more than once in one url,no judge just assign
            else:
                if nextword: self.index[keyword][url] = {nextword: None}
                else: self.index[keyword][url] = {}
        else:
            if nextword: self.index[keyword] = {url:{nextword: None}}
            else: self.index[keyword] = {url:{}}


    # TODO: html parse 
    def add_page_to_index(self, url, content):
        ''' one word -> next word.
            When there is a multi-words search, we can search 'index' to find whether two words are next to each other in this url.
            Or (word, position++) tuple to record the word position.
        '''
        if not content: # len(words)-1 == -1 if content is empty
            return
        words = self.pstem.controling(content)
#        punctuation = ['"', ',', '.', '!', '?', '-', '(', ')', ':', '<', '>', '/', '\\']
#        for sign in punctuation:
#            content = content.replace(sign, ' ')
#        words = content.split()
        # thread_pool to deal with it. self.index need a lock
        self.index_lock.acquire()
        for i in range(len(words)-1):
            self.add_to_index(words[i], words[i+1], url)
        self.add_to_index(words[len(words)-1], '', url)
        self.index_lock.release()

