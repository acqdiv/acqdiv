"""
Script to get the number of words in a .cha file for comparison with 
the NLTK CHILDESCorpusReader method. 

Steven Moran <steven.moran@uzh.ch>
August 2014

"""

import re
import collections

infile = open("../Corpora/Sesotho/cha/hia.cha", "r")

list_words = []
dict_words = collections.defaultdict(int)

for line in infile:
    line = line.strip()
    if line.startswith("@") or line.startswith("%"):
        continue
    if line.startswith("*CHI"):
        tokens = line.split("\t")
        # print(tokens[1])
        w = re.findall(r"[\w']+", tokens[1])

        for i in range(0, len(w)-1):
            # print(w[i])
            list_words.append(w[i])
            dict_words[w[i]] += 1

print()
print(infile)
print()
print("Number of word tokens:", len(list_words))
print("Number of word types:", len(dict_words))
print()
print(list_words)
print()
print(dict_words)
print()
