#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import sys
import os
import log

def check_dir(directory):
    ''' Check whether directory exist.
        If so, make sure it is not a file.
        If not, create one.
    '''

    if os.path.exists(directory):
        if not os.path.isdir(directory):
            print(directory, 'is not a directory!')
            return False
    else:
        try:
            os.makedirs(directory)
        except OSError:
            log.log_traceback(msg=directory)
            return False
    return True

