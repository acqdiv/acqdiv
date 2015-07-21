#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Make simple regex replacements in all files in a directory
Usage: python3 edit.py path/to/dir
'''

import os
import re
import sys

try:
    input_dir = sys.argv[1]
except IndexError:
    input_dir = os.getcwd()

for root, dirs, files in os.walk(input_dir):
    output_dir = re.sub('\/?$', '_edited/', root)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for name in files:
        with open(os.path.join(root, name), 'r') as input_file, open(os.path.join(output_dir, name), 'w') as output_file:        
            for line in input_file:
                line = re.sub('^\d*\s+(?=[\*%])', '', line)
                print(line, file=output_file, end='')