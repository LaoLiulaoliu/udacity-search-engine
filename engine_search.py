#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import os
import sys
import confparse
import pickle_file
import log
import tools
import porter_stemming
import search

class cache(object):
    """ A key, value cache"""
    def __init__(self):
        self.caching = {}

    def cached_execution(self, code):
        if code in self.caching:
            return self.caching[code]
        result = eval(code)
        self.caching[code] = result
        return result

if __name__ == '__main__':
    # get configuration
    conf = confparse.confparse('./engine.ini')
    conf = conf.getall()

    # log
    log_dir = conf['log_directory']
    ret = tools.check_dir(log_dir)
    if not ret: log_dir = './'
    log_file = os.path.join(log_dir, conf['search_log'])
    logger = log.init('engine_search', log_file)

    # pickle ranks and index
    directory = conf['dump_directory']
    pkfile = pickle_file.pickle_file()
    ret = pkfile.check_dir(directory)
    if not ret:
        print('error: ', directory, 'use current dir as default.')
        directory = './'
    ranks = pkfile.load_file(directory, 'ranks_pickle')
    index = pkfile.load_file(directory, 'index_pickle')
    if ranks == False or index == False:
        print('No data can be load. Program exit.')
        exit(1)

    # stemming
    pstem = porter_stemming.PorterStemmer()
    # cache
    cache_stem = cache()
    cache_search = cache()

    # for search cycle
    while True:
        try:
            words = input('Please input words to search: ')
        except EOFError:
            print('Ctrl-d, program exit.')
            exit(0)
        except:
            log.log_traceback(logger)
            logger.debug(sys.exc_info()[:2])
            exit(0)
        logger.info('search: %s', words)
#        query = cache_stem.cached_execution( 'pstem.controling(words)' ) # a words list
#        result = cache_stem.cached_execution( 'search.multi_search(index, ranks, query)' )
        query = pstem.controling(words) # a words list
        result = search.multi_search(index, ranks, query)
        if not result:
            print('Sorry, the engine can not find what you want.')
        for item in result: print(item)

