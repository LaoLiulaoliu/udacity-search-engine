#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import os
import confparse
import crawler
import pickle_file
import log
import tools

seeds = ['http://www.wikipedia.org/', 'http://www.yahoo.com']
seeds = ['http://www.udacity.com/cs101x/index.html']

if __name__ == '__main__':
    # get configuration
    conf = confparse.confparse('./engine.ini')
    conf = conf.getall()

    # log
    log_dir = conf['log_directory']
    ret = tools.check_dir(log_dir)
    if not ret: log_dir = './'
    log_file = os.path.join(log_dir, conf['crawl_log'])
    logger = log.init('engine_spider', log_file)

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
        ranks = None
        index = {}

    # crawling the web pages
    crawl = crawler.crawler(seeds, logger, conf['number_of_threads'], conf['crawl_depth'], ranks)
    if index: crawl.indexing.index.update(index)
    crawl.run_crawl()
    ranks = crawl.organize_graph_rank()


    # dumping
    pkfile.dump_file(ranks, directory, 'ranks_pickle')
    pkfile.dump_file(crawl.indexing.index, directory, 'index_pickle')
