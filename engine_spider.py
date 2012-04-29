#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import os
import signal
import confparse
import crawler
import pickle_file
import log
import tools

seeds = ['http://www.wikipedia.org/', 'http://www.yahoo.com']
#seeds = ['http://www.udacity.com/cs101x/index.html']
g_crawl = None
g_directory = '.'


def sig_handler(signum, frame):
    print('receive signal: {}. Dumping file and exit...'.format(signum))
    ranks = g_crawl.organize_graph_rank()
    dumping(ranks, g_crawl.indexing.index, g_directory)
    exit(2)

def dumping(ranks, index, directory):
    pkfile.dump_file(ranks, directory, 'ranks_pickle')
    pkfile.dump_file(index, directory, 'index_pickle')


signal.signal(signal.SIGINT, sig_handler)
#signal.signal(signal.SIGQUIT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)


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
    g_directory = conf['dump_directory']
    pkfile = pickle_file.pickle_file()
    ret = pkfile.check_dir(g_directory)
    if not ret:
        print('error: ', g_directory, 'use current dir as default.')
        g_directory = './'
    ranks = pkfile.load_file(g_directory, 'ranks_pickle')
    index = pkfile.load_file(g_directory, 'index_pickle')
    if ranks == False or index == False:
        ranks = None
        index = None

    # crawling the web pages
    g_crawl = crawler.crawler(seeds, logger, conf['number_of_threads'], conf['crawl_depth'], ranks, index)
    g_crawl.run_crawl()
    ranks = g_crawl.organize_graph_rank()

    dumping(ranks, g_crawl.indexing.index, g_directory)
