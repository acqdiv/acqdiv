# Convert files from chardet-determined encoding to UTF-8

import sys
import codecs
import chardet
from path import path

def main(path):
    f = open(path, "r").read()
    result = chardet.detect(f)
    charenc = result['encoding']

    ifile = codecs.open(path, "r", encoding=charenc)
    ofile = codecs.open(path+".txt", "w", "utf-8")

    for line in ifile:
        # line = "".join(i for i in line if ord(i)<28) # remove control characters
        line = line.strip()+"\n"
        ofile.write(line)

    ofile.close()
    ifile.close()

    print("REENCODING:\t"+path+"\t"+charenc+"\tutf-8")

if __name__=="__main__":
    dir = sys.argv[1]

    if len(sys.argv) > 2:
        type = sys.argv[2]
    else:
        type = None

    for f in path(dir).files(type):
        if not f.basename().startswith('.'):
            main(f)
