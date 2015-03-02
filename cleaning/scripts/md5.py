# Given a directory generate an md5 hash for each file in it
# Useful for comparing file contents for files with possible different filenames

import sys
import collections
from path import path

dups = collections.defaultdict(list)

def process(path):
    md5 = path.read_md5()
    result = [str(md5)]
    result.append(str(path.basename()))
    # print("\t".join(result))
    dups[md5].append(str(path.namebase))

def main(dir):
    for f in path(dir).files():
        if not f.basename().startswith('.'):
            process(f)

if __name__=="__main__":
    dir = sys.argv[1]
    main(dir)
    for k, v in dups.items():
        if len(v) > 1:
            print(k,str(v))

