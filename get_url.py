#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import httplib2
import re
import log

class get_url(object):
    def __init__(self, logger):
        ''' self.http = httplib2.Http() 
            multi-thread use same httplib2.Http() object cause socket error
        '''
        self.logger = logger
        self.pat = re.compile(b'<(meta.*charset=|\?xml.*encoding=")(\w+-?\w*-?\w*)"', re.IGNORECASE)

    def get(self, url):
        try:
            http = httplib2.Http()
            response, content = http.request(url, 'GET')
            if response['status'] != '200': return
            if content == b'Access Denied': return

            encode = ''
            for item in response['content-type'].lower().split(';'):
                if 'charset' in item:
                    encode = item.split('=')[1]
            if not encode:
                re_sh = self.pat.search(content)
                if re_sh:
                    encode = re_sh.group(2).decode()
                    print('\n--group2: ', re_sh.group(2), '\t', re_sh.group(0))
            if not encode: encode = 'utf-8'
            return content.decode(encode)
        except UnicodeDecodeError:
            self.logger.debug(response)
            log.log_traceback(self.logger)
        except:
            log.log_traceback(self.logger)


if __name__ == '__main__':
    url = ['http://djt.qq.com/api.php', 'http://www.youku.com/']
    obj = get_url(None)
    for u in url:
        content = obj.get(u)
        if content: print(content)
        else: print(False)
# content = ''.join( map(chr, filter(None, content)) )
