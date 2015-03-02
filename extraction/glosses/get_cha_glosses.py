"""
Script to gather glosses from the CHILDES files; outputs gloss type \t frequency table

Example usage: python get_cha_glosses.py ../Corpora/Indonesian/ %flo:

Author: Steven Moran <steven.moran@uzh.ch>
Date: October 2014
"""

import os
import sys
import collections

# pass in the root directory to where the childes/acqdiv corpora are
rootdir = sys.argv[1]

# gloss line marked with
gloss_line_label = sys.argv[2] # e.g. Indonesian "%flo:"

# collect the gloss types and their counts
glosses = collections.defaultdict(int)

# recursive walk through all directories and files in the rootdir
for root, subs, files in os.walk(rootdir):
    for file in files:
        # this is a hack
        if file.__contains__("DS"):
            continue

        filepath = os.path.join(root, file)
        with open(filepath, "r") as file:
            for line in file:
                # skip all lines 
                if not line.startswith(gloss_line_label):
                    continue
                line = line.strip()
                tokens = line.partition("\t")
                gloss_line = tokens[2].strip()

                gloss_tokens = gloss_line.split()
                for token in gloss_tokens:
                    glosses[token] += 1

# print the results
for k, v in glosses.items():
    print(k, v)
