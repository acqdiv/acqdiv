"""
Script to extract glosses from CHILDES XML for Indonesian

Note: doesn't seem possible to extract glosses from the 
Indonesian XML files with the NLTK CHILDES XML CorpusReader

Here I use the ElementTree XML library (standard Python)

Steven Moran <steven.moran@uzh.ch>
October 2014

$ python get_xml_glosses.py path/to/xml/files

"""

import os
import sys
import collections
from xml.etree.ElementTree import ElementTree

glosses = collections.defaultdict(int)
# rootdir = "../Corpora/Indonesian/xml/"
rootdir = sys.argv[1]

# recursive walk through all directories and files in the rootdir
for root, subs, files in os.walk(rootdir):
    for file in files:
        # stupid hack to skip Mac OS DS_Store files
        if file.__contains__("DS_"):
            continue
        filepath = os.path.join(root, file)
        rootnode = ElementTree().parse(filepath)

        # get the text out of the flow attibutes in the <a> tags and count it
        flows = [x.text for x in rootnode.findall(".//{http://www.talkbank.org/ns/talkbank}a[@type='flow']")]
        for text in flows:
            text = text.strip()
            tokens = text.split()
            for token in tokens:
                glosses[token] += 1

for k, v in glosses.items():
    print(k, v)

