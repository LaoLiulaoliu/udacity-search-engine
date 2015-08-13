#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import hashlib

def md5Checksum(file_name, exclude_line='', include_line=''):
    ''' Compute md5 hash of the specified file.
    '''
    m = hashlib.md5()
    try:
        fd = open(file_name, 'rb')
    except IOError:
        fd.close()
        print("Unable to read file in read model: ", file_name)
        return
    content = fd.readlines()
    fd.close()
    for line in content:
        if exclude_line and line.startswith(exclude_line):
            continue
        m.update(line)
    if include_line: m.update(include_line)
    return m.hexdigest()


def md5_bytes(file_name, block_size=8192):
    ''' Compute md5 hash of a file.
        return result in bytes.
    '''
    with open(file_name, 'rb') as fd:
        m = hashlib.md5()
        while True:
            data = fd.read(block_size)
            if not data:
                break
            m.update(data)
    return m.digest()


def md5_str(buf):
    ''' Compute md5 hash of a string.
    '''
    m = hashlib.md5(buf.encode())
    return m.hexdigest()


if __name__ == '__main__':
    print("'who are you' md5sum: ", md5_str("who are you") )
    import sys
    x = md5Checksum(sys.argv[1])
    print(sys.argv[1], 'md5sum:', x)
    x = md5_bytes(sys.argv[1])
    y = md5_bytes(sys.argv[1])
    if x == y:
        print(type(x), x)

