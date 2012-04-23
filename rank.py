#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/


def compute_ranks(graph):
    ''' rank 
        1.Do you hava a lot of friends? (incoming links) up
        2.Is each of your friend popular? (You have a lot of nerd friends,your rank won't be high.) up
        3.Is each of your friend have a lot of friends? (outgoing links) down
    '''

    d = 0.8 # damping factor
            # The probability of he get link in this page,rather than starting from a random new page.
    numloops = 10
    
    ranks = {} # {url:rank, url:rank}
    npages = len(graph)
    # initial state
    for page in graph:
        ranks[page] = 1.0 / npages
    
    # iterate several times to converge
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank += d * ranks[node] / len(graph[node])
            
            newranks[page] = newrank
        ranks = newranks
    return ranks
