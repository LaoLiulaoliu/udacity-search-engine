#!/usr/bin/env python3
# encoding: utf-8

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import threading
import urllib.parse
import log
import get_url
import indexing
import thread_pool
import rank
import search

    
class crawler(object):
    """A simple web crawler."""

    def __init__(self, seeds, logger, thread_num=5, max_depth=9, ranks=None):
        self.init_seeds_num = len(seeds)
        self.tocrawl = {}
        for seed in seeds:
            self.tocrawl[seed] = 0  # {url: current_depth, ...}
        self.crawled = {}           # {url1: None, url2: None, ...}
        self.max_depth = max_depth  # traversal depth
        self.logger = logger
        self.ranks = ranks
        self.down_url = get_url.get_url(logger)
        self.indexing = indexing.indexing()
        self.threadpool = thread_pool.thread_pool(thread_num)
        self.lock = threading.Lock()

    def run_crawl(self):
        for i in range(self.init_seeds_num):
            self.threadpool.add_job(self.crawl_web)
        self.threadpool.start()
        self.logger.info('Start to crawl webpages.')
        self.threadpool.wait_completion()
        self.logger.info('Finish crawling webpages.')

    def organize_graph_rank(self):
        """Get the graph for ranking.
           After run_crawl, this call can run once(because queue can get once)."""
        self.logger.info('Merge url graph.')
        graph = {}
        ret = self.threadpool.get_one_result()
        while ret:
            graph.update(ret)
            ret = self.threadpool.get_one_result()
        self.logger.info('Compute the ranks.')
        ranks = rank.compute_ranks(graph)

        if self.ranks: # if read ranks from pickle file at startup
            self.ranks.update(ranks) # old.update(new)
            return self.ranks
        return ranks

    def crawl_web(self):
        graph = {} # <url>, [list of pages it links to]
        while True:
            try:
                self.lock.acquire()
                pageurl, depth = self.tocrawl.popitem() # add lock
                self.lock.release()
            except:
                self.lock.release()
                break
            
            if pageurl not in self.crawled and depth < self.max_depth: # no lock, improve efficiency
                depth += 1
                content = self.down_url.get(pageurl)
                if not content: continue
                # self.indexing.add_page_to_index(pageurl, content)
                # add lock or got to a queue then run indexing
                # add indexing to the same thread_pool
                self.threadpool.add_job(self.indexing.add_page_to_index, pageurl, content)
                outlinks = self.get_all_links(pageurl, content)
                graph[pageurl] = outlinks
                self.lock.acquire()
                for link in outlinks:
                    if link in self.tocrawl: # add lock
                        break
                    else:
                        self.tocrawl[link] = depth # add lock
                self.crawled[pageurl] = None # lock
                self.lock.release()
        return graph # a.update(b), dict(a, **b), dict(list(a.items()) + list(b.items()))

    # TODO: need html.parser
    def get_all_links(self, pageurl, page):
        links = []
        while True:
            url, endpos = self.get_next_target(page)
            if endpos != 0:
                if url:
                    if not url.startswith('http://'):  # relative url, like '/fiEfds', 'ccepI', '//en.wikipedia.org/'
                        url = urllib.parse.urljoin(pageurl, url)
                    links.append(url)
                page = page[endpos:]
            else:
                break
        return links

    def get_next_target(self, page):
        find_str = '<a href='
        quote = ['\'', '"']     # ' and " 2 kinds of quote
        start_link = page.find(find_str)
        if start_link == -1: 
            return None, 0
        start_quote = start_link + len(find_str)
        if page[start_quote] == quote[0]:
            end_quote = page.find(quote[0], start_quote + 1)
        elif page[start_quote] == quote[1]:
            end_quote = page.find(quote[1], start_quote + 1)
        else:
            end_quote = start_quote + 1 # no proper quote, url will be ''
        url = page[start_quote + 1:end_quote]
        return url, end_quote

#def union(p,q):
#    for e in q:
#        if e not in p:
#            p.append(e)
#
## TODO: r-tree
#def crawl_web_breadth(seed):
#    tocrawl = [seed]
#    crawled = []
#    while tocrawl:
#        pageurl = tocrawl.pop(0) # breadth-first search
#        if pageurl not in crawled:
#            union(tocrawl, get_all_links(get_page(pageurl)))
#            crawled.append(pageurl)
#    return crawled

if __name__ == '__main__':
    seeds = ['http://www.google.com']
    cr = crawler(seeds)
    content = cr.down_url.get(seeds[0])
    print( cr.get_all_links(seeds[0], content) )
