from corpus_parser_functions import parse_corpus_per_file
from corpus_parser_functions import parse_corpus

import errno
import json
import os
import shutil
import sys

def main():

    rootdir = sys.argv[1]
    
    # parse test corpora using functions from corpus_parser_functions

    for root, subs, files in os.walk(rootdir):
        for fp in files:
            filepath = os.path.join(root,fp)
            filename = os.path.basename(filepath)
            corpus_name = os.path.splitext(filename)[0]
            if filename.endswith('.xml'):
                print('Processing: {}'.format(filepath))
                try:
                    for elem in parse_corpus_per_file(corpus_name, filename,
                            filepath, 'XML'):
                        corpus_object = elem

                        outpath = os.path.join(os.path.split(filepath)[0],
                                '../json/{}.json'.format(corpus_name))
                        
                        with open(outpath, 'w') as fp:
                            # careful, sort_keys=True can cause memory errors with bigger corpora such as Japanese_MiiPro
                            fp.write(json.dumps(corpus_object, fp, sort_keys=True, indent=4, ensure_ascii=False))
                except Exception as e:
                    print("Aborted processing with exception {}".format(repr(e)))

if __name__ == '__main__':
    main()
