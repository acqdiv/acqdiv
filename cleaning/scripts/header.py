# Generate metadata table
# Steven Moran <steven.moran@uzh.ch>
# Feb 2015

# grep "^@" *.cha > temp
# python3 header.py temp > table

import sys
import csv
import collections

infile = open(sys.argv[1], "r")
# SUP94W.txt:@Time:3:00 - 3:30 p.m.

skip = ["@End", "@Situation:"]

data = collections.defaultdict(lambda: collections.defaultdict(list))
headers = collections.defaultdict(int)
lines = []
for line in infile:
    line = line.strip()
    tokens = line.split(".cha:")
    filename = tokens[0].replace("../turkish/cha/", "") # get base filename
    filename = tokens[0].replace("../inuktitut/cha/", "") # get base filename
    filename = tokens[0].replace("../yucatec/cha/", "") # get base filename
    htokens = tokens[1].split("\t") # not all categories contain values
    if htokens[0] in skip:
        continue
    headers[htokens[0]] += 1 # category
    if len(htokens) > 1:
        result = [filename, htokens[0], htokens[1]] # if value
        data[filename][htokens[0]].append(htokens[1])
    else:
        result = [filename, htokens[0], ""] # no value
    lines.append(result)
infile.close()

# unique strings in header categories
header = []
for k, v in headers.items():
    header.append(k)
header.sort()
print("\t".join(header)+"\t"+"filename")

row = []
for k, v in data.items():
    for i in header:
        if i in data[k]:
            row.append(";".join(data[k][i]))
        else:
            row.append("")
    print("\t".join(row)+"\t"+k)
    row = []


print(header)
