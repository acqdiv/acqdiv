"""
Inuktitut: remove file extensions .NAC, .XXS, .XXX, .MAY

Call: python filenames.py path/to/files

"""
import os
import sys
from path import path

def main(path):
    original = path
    path = path.replace(path.ext, "")
    os.rename(original, path)
    print("RENAMING\t"+original+"\t"+path)

    # should we remove this stuff?
    # _2dp

if __name__=="__main__":
    dir = sys.argv[1]
    for f in path(dir).files():
        if not f.basename().startswith('.'):
            main(f)
