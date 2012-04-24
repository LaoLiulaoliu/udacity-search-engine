#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import configparser
import log

class confparse(object):
    ''' read configuration file. '''

    def __init__(self, file_path):
        try:
            self.config = configparser.ConfigParser()
            self.config.read(file_path)
        except:
            log.log_traceback()

    def getall(self):
        conf = {}
        for sec in self.config.sections():
            for tup1, tup2 in self.config.items(sec):
                if tup2.isdigit():
                    conf[tup1] = int(tup2)
                else:
                    conf[tup1] = tup2
        return conf

