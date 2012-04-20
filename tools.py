#!/usr/bin/env python3
# encoding: utf-8

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import sys
import os

def check_dir(directory):
    if os.path.exists(directory):
        if not os.path.isdir(directory):
            print(directory, 'is not a directory!')
            return False
    else:
        try:
            os.makedirs(directory)
        except OSError:
            print(sys.exc_info[:2], directory)
            return False
    return True

