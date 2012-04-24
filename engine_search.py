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
import cache


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
    cache_stem = cache.cache()
    cache_search = cache.cache()

    # for search cycle
    while True:
        cache_stem.pop_onethird()
        cache_search.pop_onethird()
        try:
            words = input('Please input words to search: ')
        except EOFError:
            print('Ctrl-d, program exit.')
            exit(0)
        except:
            log.log_traceback(logger)
            exit(0)
        logger.info('search: %s', words)
        if cache_stem.have_key(str(words)):
            query = cache_stem.get_by_key(str(words))
        else:
            query = pstem.controling(words) # a words list
            cache_stem.add_kv(str(words), query)
        if cache_search.have_key(str(query)): # unhashable type: list
            result = cache_search.get_by_key(str(query))
        else:
            result = search.multi_search(index, ranks, query)
            cache_search.add_kv(str(query), result)

        if not result:
            print('Sorry, the engine can not find what you want.')
        for item in result: print(item)

