# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 17:51:28 2016

@author: anna
"""


import difflib
import sys
import os
import manage_db
from tqdm import tqdm


def get_import_args(dir_path):
    """Get list of split cmdline arguments for database import"""

    split_args = ["import"]

    for name, filepath in [("-s", "sessions.csv"),
                           ("-p", "participants.csv"),
                           ("-m", "monitor.csv"),
                           ("-l", "file_locations.csv"),
                           ("-f", "files.csv")]:

        split_args.append(name)
        split_args.append(os.path.join(dir_path, filepath))

    split_args.append("-r")

    return split_args


def run(args):
    """Set command line arguments and run database interface application."""
    sys.argv[1:] = args
    manage_db.main()


def get_contents(path):
    """Get content of all metadata files as strings."""
    content = {}
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)

        with open(filepath, "r") as f:
            content[filename] = f.readlines()

    return content


diff = difflib.HtmlDiff()
html = open("diff.html", "w")

# default argument for import and export
import_args = ["import"]
export_args = ["export"]

print("**********First Import**********")
sys.stdout.flush()
import_args = get_import_args("shared/metadata/")
run(import_args)
# TODO: get sql dump

print("**********First Export**********")
sys.stdout.flush()
run(export_args)
content1 = get_contents("Export/")

# second import
print("**********Second Import**********")
sys.stdout.flush()
import_args = get_import_args("Export/")
run(import_args)

# TODO: get sql dump

# second export
print("**********Second Export**********")
sys.stdout.flush()
run(export_args)
content2 = get_contents("Export/")


# compare csv files
for mdata in tqdm(["sessions.csv", "participants.csv", "files.csv",
                   "file_locations.csv", "monitor.csv"]):

    lines1 = content1[mdata]
    lines2 = content2[mdata]

    if lines1 == lines2:
        print(mdata, "files are identical!")
        sys.stdout.flush()
    else:
        print(mdata, "files not identical! HTML diff will be created...")
        sys.stdout.flush()

        html.write(diff.make_file(content1[mdata], content2[mdata],
                                  fromdesc="Import", todesc="Export"))

