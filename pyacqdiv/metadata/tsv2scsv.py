#!usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to convert tsv into strict csv files with quotes and commas.
Usage: python tsv2scsv.py <infile.tsv> <outfile.csv>
Author: Cazim Amadeo Hysi
<firstnames.lastname>@uzh.ch
"""

import csv
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile, newline='') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    with open(outfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in reader:
            writer.writerow(row)

print("Done.")
