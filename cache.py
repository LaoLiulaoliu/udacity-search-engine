#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>

import time

class cache(object):
    """ A key, value cache"""
    def __init__(self):
        self.N = 20000 # tested good number for double core, 1.75HZ CPU
        self.caching = {}

    def have_key(self, key):
        return key in self.caching

    def get_by_key(self, key):
        return self.caching[key]

    def add_kv(self, key, val):
        self.caching[key] = val

    # keep the size of self.caching small, prevent the performance problem
    def pop_onethird(self):
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
    def __init__(self, N):
        self.N = N
        self.cache_dict = {}

    def insert_dict(self):
        for i in range(self.N):
            for j in range(self.N):
                self.cache_dict[i] = i + j

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

    N = 20000 # 146s to insert_dict(), double this then costing time will grow exponentially
    cc = cache()
    test_cc = cache_test(N)
    result, cost = cc.time_execution('test_cc.insert_dict()')
    print(cost)
    result, cost = cc.time_execution('test_cc.have_key()')
    print(cost)
    result, cost = cc.time_execution('test_cc.pop_half()')
    print(cost, result)
