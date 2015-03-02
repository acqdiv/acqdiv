"""
Create new filenames for KULLD

Call: python filenames.py path/to/files

Turkish: replace KULLD Turkish .cha filenames with "-" instead of ";". E.g.:

burcu27_21july03_01;10;00.cha
burcu27_21july03_01-10-00

"""
import os
import sys
from path import path
import logging

def metadata(path):
    # WIP: extract metadata from Turkish filenames
    logging.basicConfig(filename='filenames.log', level=logging.DEBUG, filemode='w')
    elements = []
    elements.append(path)
    tokens = path.split("/")
    filename = tokens[-1]
    elements.append(filename)
    logging.debug(",".join(elements))

def turkish(path, ext=True):
    path = path.lower()
    if path.__contains__(" first 30 minutes"):
        path = path.replace(" first 30 minutes", "")
    if path.__contains__(" first 35 minutes"):
        path = path.replace(" first 35 minutes", "")
    if path.__contains__("cansu36_ 20feb04_02-03-26"):
        path = path.replace("cansu36_ 20feb04_02-03-26", "cansu36_20feb04_02-03-26")
    if path.__contains__("ogun31-05july503_02-05-01"):
        path = path.replace("ogun31-05july503_02-05-01", "ogun31-05july03_02-05-01")      
    if path.__contains__(";"):
        path = path.replace(";", "-")
    if ext:
        path = path.replace(".cha", "")
    path = path.replace(".", "-")
    return path

def main(path):
    original = path
    path = turkish(path)
    os.rename(original, path)
    print("RENAMING\t"+original+"\t"+path)

    # metadata(path)

if __name__=="__main__":
    dir = sys.argv[1]
    for f in path(dir).files():
        if not f.basename().startswith('.'):
            main(f)
