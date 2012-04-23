#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import os
import sys
import pickle
import tools

class pickle_file(object):
    ''' dump and load pickle file. '''

    def __init__(self):
        pass

    def check_dir(self, directory):
        return tools.check_dir(directory)

    def dump_file(self, variable, directory, file_name):
        ''' dump variable to file. '''
        full_name = os.path.join(directory, file_name)
        if os.path.isfile(full_name):
            os.rename(full_name, full_name + '_bak')
        with open(full_name, 'wb') as f:
            try:
                pickle.dump(variable, f)
            except:
                print(sys.exc_info[:2], variable, full_name)
                return False
        return True

    def load_file(self, directory, file_name):
        ''' load dump file to variables. '''
        full_name = os.path.join(directory, file_name)
        open_file = full_name + '_bak'
        if not os.path.isfile(open_file):
            if not os.path.isfile(full_name):
                print('No dump file exist in ', directory, file_name)
                return False
            else:
                open_file = full_name
        with open(open_file, 'rb') as f:
            try:
                variable = pickle.load(f)
            except:
                print(sys.exc_info[:2], variable, full_name)
                return False
        return variable
