#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import time

class cache(object):
    ''' A key, value cache. '''

    def __init__(self):
        self.N = 100000 # tested fast number
        self.caching = {}

    def have_key(self, key):
        return key in self.caching

    def get_by_key(self, key):
        return self.caching[key]

    def add_kv(self, key, val):
        self.caching[key] = val

    def pop_onethird(self):
        ''' keep the size of self.caching small
            prevent the performance problem
        '''
        if len(self.caching) >= self.N:
            for i in range(self.N // 3):
                self.caching.popitem()

    def time_execution(self, code):
        start = time.clock()
        result = eval(code)
        run_time = time.clock() - start
        return result, run_time


    def cached_execution(self, code):
        if code in self.caching:
            return self.caching[code]
        result = eval(code)
        self.caching[code] = result
        return result


class cache_test(object):
    ''' Both insert and popitem have the same speed. '''

    def __init__(self, N):
        self.N = N
        self.cache_dict = {}

    def insert_dict(self):
        for i in range(self.N):
            self.cache_dict[i] = i

    def have_key(self):
        num = self.N // 3
        return num in self.cache_dict

    def pop_half(self):
        num = self.N // 2
        if len(self.cache_dict) >= self.N:
            for i in range(num):
                self.cache_dict.popitem()
        return self.cache_dict.__len__()

if __name__ == '__main__':

    N = 1000000 # 0.67s to insert new items for 1.75HZ CPU
    cc = cache()
    test_cc = cache_test(N)
    result, cost = cc.time_execution('test_cc.insert_dict()')
    print(cost)
    result, cost = cc.time_execution('test_cc.have_key()')
    print(cost)
    result, cost = cc.time_execution('test_cc.pop_half()')
    print(cost, result)
