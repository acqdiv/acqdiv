"""
Inuktitut: remove file extensions .NAC, .XXS, .XXX, .MAY

Call: python filenames.py path/to/files

"""
import os
import sys
from path import path

def main(path):
    original = path
    path = path.rstrip(".NAC")
    path = path.rstrip(".XXS")
    path = path.rstrip(".XXX")
    path = path.rstrip(".MAY")
    os.rename(original, path)
    print("RENAMING\t"+original+"\t"+path)

if __name__=="__main__":
    dir = sys.argv[1]
    for f in path(dir).files():
        if not f.basename().startswith('.'):
            main(f)
