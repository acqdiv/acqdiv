# -*- coding: utf-8 -*-

"""
Clean Inuktitut corpora and make CHAT compliant

NOTE, TO FIX STILL:

DEBUG:root:../inuktitut/cha/MAE51W.utf8:3082    NO TAB IN LINE  %arg:

New Epsiode: -> Situation


*ALI:una. una.
%eng:this one. this one.

%add:ALI,DAN

%mor:oh yes.

*ALI:Alec sings a song (nonsense) .


- @Break is for breaks in the tape --> we can drop it. 
- @Situation in the middle of file is for information on changes in the situation --> apparently this was allowed when the Inuktitut corpus was compiled; if the present CHAT standard doesn't allow it, convert it to %sit:
- The codes in %arg: are documented in the attached file, which Shanley can't open anymore... nor can I! Could you give it a try? There must be some textual data in the file because when I open it as ISO-Latin or UTF-8 in Textmate I can see some things that make sense, but there is a large amount of clutter wrapped around it. Best thing would be if we could convert this to pdf somehow and put it under Acqdiv/Documentation. 


"""

import os
import re
import sys
import csv
import configparser
from path import path

skip_tiers = ["%sit:", "%com:", "%err:", "%mor:", "%tim:", "%add:", "%cod:", "%snd:", "%eng:"]
skip_headers = ["@Enterer:", "@Checker:", "@Reviser:", "@Coder:", "@Coding:", "@Other Info:", "@Participants:", "@Birth of MAE:", "@Section:"]
participants = {}

# not used
def remove_control_chars(s):
    mpa = dict.fromkeys(range(32))
    return s.translate(mpa)

# "_",""
def rules(s):
    # be ware of feeding and bleeding substrings!
    s = re.sub("(^\*[A-Z]{3}:)(\s+)", r"\1\t", s)
    s = re.sub("(^\%[a-z]{3}:)(\s+)", r"\1\t", s)
    s = re.sub("\u001A", r"", s)
    s = re.sub("\*xxx:\s", r"*UNK:\t", s)
    s = re.sub("%COM:", "%com:", s)
    s = re.sub("%tim:0:20:00", "", s)
#    s = re.sub("^_$", "", s)
    s = re.sub("^\.$", "", s)
    s = re.sub("^~$", "", s)
    s = re.sub("^%$", "", s)
    s = re.sub("^\*$", "", s)
    s = re.sub("^\*LIZ:$", "", s)
    s = re.sub("^\*DAI:$", "", s)
    s = re.sub("^%rr:$", "%err:", s)
    s = re.sub("^%it:$", "%sit:", s)
    s = re.sub("^sit:$", "%sit:", s)
    s = re.sub("@tim:", "%tim:", s) 
    s = re.sub("^v%tim:\s", "%tim:\t", s)
    s = re.sub("^xxx:\s", "%tim:\t", s)
    s = re.sub("^\|%mor:\s", "%mor:\t", s)
    s = re.sub("(^\*\?\?\?:)(\s+)", r"\1\t", s)
    s = re.sub("@ŽIP0,16Ż", "", s)
    s = re.sub("@ŽIP0,8Ż", "", s)
    s = re.sub("ŽIP0,16Ż", "", s)
    s = re.sub("ŽIP0,8Ż", "", s)
    s = re.sub("ŽIP0DI,15DIŻ", "", s)
    s = re.sub("®IP0DI,15DI¯", "", s)
    s = re.sub("®IP0,16¯:", "", s)
    s = re.sub("@оIP0,16п", "", s)
    s = re.sub("оIP0,16п", "", s)
    s = re.sub("@оIP0,8п", "", s)
    s = re.sub("@End\s+_", "@End", s)
    s = re.sub(":\s+", ":\t", s, 1)    
    s = re.sub("(\S)([!\?\.])$", "\\1 \\2", s)
    s = re.sub("(\S)[,\.]", "\\1", s)
    s = re.sub("\-\-", "", s)

    if s.startswith("*"):
        s = re.sub("(\d+)(x)", "\\2 \\1", s)
        s = re.sub("(x)(\d+)", "\\1 \\2", s)
        s = re.sub("\s\(?(\d+)\s+x\)?(\s|$)", " [x \\1] ", s)
        s = re.sub("\s\(?x\s+(\d+)\)?(\s|$)", " [x \\1] ", s)
        s = re.sub("([^\.\?!]$)", "\\1 .", s)
        s = re.sub(",", "", s)

    if s.startswith("%add"):
        s = re.sub("([A-Z]{3})(,)([A-Z]{3})", "\\1\\2\s\\3", s)




    return(s.strip())

cc = [6, 130, 26, 96]
def normalize_sting(line):
    # remove weird characters
    return ''.join(c for c in line if not ord(c) in cc)

def get_media(path):
    pass

def replacement(line):
    for f, t in replacements:
        line = line.replace(f, t)
    return(line)

replacements = []
def get_replacements(filepath):
    # load replacement strings
    with open(filepath, "r") as infile:
        d = csv.reader(infile, delimiter=",")
        for row in d:
            if not len(row) == 2:
                sys.exit("Replacements input longer than two columns")
            replacements.append(tuple(row))

ids = {}
def get_ids(filepath):
    # load @IDs
    with open(filepath, "r") as infile:
        d = csv.reader(infile, delimiter="\t")
        next(d, None) # skip the header
        for row in d:
            id = []
            for i in range(1, len(row)-1):
                id.append(row[i])
            # populate look up table
            if not row[0] in ids:
                ids[row[0]] = []
                ids[row[0]].append("@ID:\t"+"|".join(id)+"|")
            else:
                ids[row[0]].append("@ID:\t"+"|".join(id)+"|")                

participants = {}
def get_participants(filepath):
    # load participant data
    with open(filepath, "r") as infile:
        d = csv.DictReader(infile, delimiter=",", quotechar='"')
        for row in d:
            if not row["filename"] in participants:
                participants[row["filename"]] = row["@Participants:"]

# blank headers to skip - replace with 
# skip = ["@Break", "%tim:", "%snd:", "%sit:", "%mor:", "%err:", "%eng:", "%com:", "%cod:", "%arg:", "%add:"]
changeables = ["@Activities:", "@Bck:", "@Bg", "@Bg:", "@Blank", "@Comment:", "@Date:", "@Eg", "@Eg:", "@EndTurn", "@G:", "@New Episode", "@New Language:", "@Page", "@Situation:", "@T:"]
no_tab = ["@UTF8", "@Begin", "@End", "@New Episode"]

skip_header = ["@UTF8", "@Begin", "@Languages", "@Participants", "@ID"]

def get_header(path):
    header = ["@UTF8", "@Begin", "@Languages:\tike"]
    participant = participants[path.namebase]
    header.append("@Participants:\t"+participant)
    id = ids[path.namebase]
    for i in id:
        header.append(i)
    # header.append(get_media(path))
    header.append("@Media:\t"+path.namebase+", audio")
    # add other corpus-specific header data here
    return(header)

def process(path):
    infile = open(path, "r")
    outpath = path.replace(path.ext, ".cha")
    outfile = open(outpath, "w")

    # add interim header
#    header = get_header(path)
#    outfile.write("\n".join(header)+"\n")

    # process file contents
    n = 0
    line = infile.readline()
    prev = ""
    while len(line) > 0:
        n += 1
        line = line.strip()
        line = normalize_sting(line) # do character replacements for each line
        line = rules(line) # do regex replacements for each line
        line = replacement(line) # do manual replacements for each line

        """
        for i in skip_header:
            if line.startswith(i):
                line = infile.readline()
                continue
                """
        # skip blank lines, etc.
        if line == "" or line == "*" or line == "%" or line == " ":
            line = infile.readline()
            continue

        # skip empty header lines
        if line.startswith("@") and line.endswith(":") or line.endswith(":\t"):
            line = infile.readline()
            continue

        # skip empty body lines
        if line.startswith("%") and line.endswith(":") or line.endswith(":\t"):
            line = infile.readline()
            continue

        # skip end lines
        if line.startswith("@end") or line.startswith("@End") or line.startswith("@ End"):
            line = infile.readline()
            continue

        # catch broken lines
        if not line.startswith("*") and not line.startswith("@") and not line.startswith("%"):
            prev += " "+line
            line = infile.readline()
        else:
            if prev:
                outfile.write(prev+"\n")
            prev = line
            line = infile.readline()

    if prev:
        outfile.write(prev+"\n")

    outfile.write("@End\n")
    infile.close()
    outfile.close()

def main(dir, type):
    # replace this with filepaths from the config file
    get_replacements("notes/replacements.csv")
    get_participants("notes/participants.csv")
    get_ids("notes/IDs.tsv")

    # replace this with the root filepath
    for f in path(dir).files(type):
        if not f.basename().startswith('.'):
            process(f)
            print("PROCESSING:", f.basename())
#            sys.exit(1)

    # set up directory structure
    # original/ files from the original source
    # rename and copy to temp/
    # call 

if __name__=="__main__":
    # config = configparser.ConfigParser()
    # config.read(sys.argv[1])
    # config.read("inuktitut.conf")
    # call the rename filename functions
    # print(config["filepaths"]["rules"])
    dir = sys.argv[1]
    type = sys.argv[2]
    main(dir, type)

    


# python inuktitut.py ../inuktitut/cha *.utf8
