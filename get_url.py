#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import httplib2
import sys
import log

class get_url(object):
    def __init__(self, logger):
        ''' self.http = httplib2.Http() 
            multi-thread use same httplib2.Http() object cause socket error
        '''
        self.logger = logger

    def get(self, url):
        try:
            http = httplib2.Http()
            response, content = http.request(url, 'GET')
            if response['status'] != '200':
                return
            encode = 'utf-8'
            for item in response['content-type'].lower().split(';'):
                if 'charset' in item:
                    encode = item.split('=')[1]
            if content == b'Access Denied': return
            content = content.decode(encode)
            # if type(content) == type(b''): # perform bad in gbk
            #    content = ''.join( map(chr, filter(None, content)) )
            return content
        except UnicodeDecodeError:
            log.log_traceback(self.logger)
            self.logger.debug(response)
            self.logger.debug(sys.exc_info()[:2])
        except:
            log.log_traceback(self.logger)
            self.logger.debug(sys.exc_info()[:2])
            return



if __name__ == '__main__':
    url = ['http://djt.qq.com/api.php', 'http://www.youku.com/']
    obj = get_url()
    for u in url:
        content = obj.get(u)
        if content: print(content)
        else: print(False)
# content = ''.join( map(chr, filter(None, content)) )
