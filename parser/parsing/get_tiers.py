"""
Extract all tiers from corpus texts in the CHAT or Toolbox format; output as frequency table

Example usage: python get_tiers.py ../Corpora/Indonesian/

Author: Robert Schikowski <robert.schikowski@uzh.ch>
Last modification: 9 October 2014
"""

import os
import sys
import collections
import re

# pass in the root directory to where the corpora are
rootdir = sys.argv[1]

# collect the tiers and their counts
tiers = collections.defaultdict(int)

# recursive walk through all directories and files in the rootdir
for root, subs, files in os.walk(rootdir):
    for file in files:
        # this is a hack
        if file.__contains__("DS"):
            continue

        filepath = os.path.join(root, file)
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                sep = re.compile(r"^[\*%@\\]\w+:?")
                m = sep.match(line)
                if m:
                    tiers[m.group()] += 1
                                        
# sort and print the results
for tuple in sorted(tiers.items()):
    print tuple[0], tuple[1]
