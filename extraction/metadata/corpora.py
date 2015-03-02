"""
Script to gather metadata from the CHILDES .cdc files and outputs a tab delimited table

Author: Steven Moran <steven.moran@uzh.ch>
Date: October 2014

$ python metadata.py path/to/corpora/

"""

import os
import sys
import collections

# pass in the root directory to where the childes/acqdiv corpora are
rootdir = sys.argv[1]

# dictionary to hold the metadata label keys of all .cdc files
keys = collections.defaultdict(int)

# dictionary for each corpora-specific metadata
corpora = {}

# dig through the directory looking for filenames with "metadata" in them, e.g. "metadata.cdc"
# TODO: output corpora directory that *don't have* a metadata.cdc file (look out for acqdiv-specific corpora!)
for root, subs, files in os.walk(rootdir):
    for file in files:
        if file.__contains__("metadata"):
            filepath = os.path.join(root, file)

            # if you want to print the length of each file
            # s = "wc -l "+filepath
            # os.system(s)

            if not filepath in corpora:
                corpora[filepath] = {}

            # loop through each line of the .cdc file and gather its contents
            with open(filepath, "r") as file:
                for line in file:
                    # process each line; if no ":" skip the line
                    line = line.strip()
                    line = line.replace("\t", "")
                    if not line.__contains__(":"):
                        continue
                    tokens = line.partition(":")
                    property = tokens[0]
                    data = tokens[2].strip()

                    # you can check if a particular propert exists
                    # if property.__contains__("kindergarten"):
                    #    print(filepath, line)

                    # add each metadata category to a category hash set
                    keys[property] += 1
                    if not property in corpora[filepath]:
                        corpora[filepath][property] = data

# create the header row for the output table
header = []
for key in keys:
    header.append(key)
print("CorpusMetadataID"+","+",".join(header))

# gather the results and print as rows
result = ""
for key in corpora:
    result = []
    result.append(key)
    for head in header:
        if head in corpora[key]:
            result.append(corpora[key][head])
        else:
            result.append("")
    print(",".join(result))

