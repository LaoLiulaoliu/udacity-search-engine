#!/usr/bin/env python3
# encoding: utf-8

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import configparser

class confparse(object):
    """read configuration"""
    def __init__(self, file_path):
        try:
            self.config = configparser.ConfigParser()
            self.config.read(file_path)
        except:
            import sys
            print(sys.exc_info()[:2])

    def getall(self):
        conf = {}
        for sec in self.config.sections():
            for tup1, tup2 in self.config.items(sec):
                if tup2.isdigit():
                    conf[tup1] = int(tup2)
                else:
                    conf[tup1] = tup2
        return conf

