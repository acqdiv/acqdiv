# -*- coding: utf-8 -*-

# From KULLD .cha to CHILDES CLAN conformant

import os
import re
import sys
import csv
from path import path

def preprocess(line):
    line = re.sub("^@\s", "@", line)
    return line

def rules(line):
    line = re.sub("^@New Episode:$", "@New Episode", line)
    line = re.sub("^@Participants\s+", "@Participants:\t", line)
    line = re.sub("^%act\s+","%act:\t", line)
    line = re.sub("^@Age of CHI$", "@Age of CHI:", line)
    line = re.sub("^@Coder$", "@Coder:", line)
    line = re.sub("^@Date$", "@Date:", line)
    line = re.sub("^@Education of MOT$", "@Education of MOT:", line)
    line = re.sub("^@ID$", "@ID:", line)
    line = re.sub("^@Media$", "@Media:", line)
    line = re.sub("^@Recorder$", "@Recorder:", line)
    line = re.sub("^@Transcriber$", "@Transcriber:", line)
    line = re.sub("^\*MOT$", "", line)
    line = re.sub("^@Child: Tuğçe$", "", line)
    line = re.sub("^@Sex of CHI$", "@Sex of CHI:", line)
    line = re.sub("^@SEX of CHI$", "@SEX of CHI:", line)
    line = re.sub("^@SES of MOT$","@SES of MOT:", line)
    line = re.sub("^@Mother, FAT Father$", "", line)
    # replace <:> space with \t in first occurrence
    line = re.sub(":\s*", ":\t", line, 1)
    
    # get rid of empty headers
    line = re.sub("^@.*:\t*$", "", line)

    """
    line = re.sub("(^[A-Z]{3}\-[A-Z]{3}:)", r"*\1", line) # MOM-CHI:
    line = re.sub("(^\*[A-Z]{3})(-)(:)", r"\1\3", line) # *MOT-:
    line = re.sub("(^\*[A-Z]{3})(.)(:)", r"\1\3", line) # *MOT-:
    line = re.sub("(^\*[A-Z]{3}\-[A-Z]{3})(\s+)(:)", r"\1\3", line) # *MOT-MOM :
    line = re.sub("(^\*[A-Z]{3})(\-)(\s+)([A-Z]{3}:)", r"\1\2\4", line) # *MOT- NEI:
    line = re.sub("(^\*[A-Z]{3})(\s+)(\-)([A-Z]{3}:)", r"\1\3\4", line) # *CHI -MOT:
    line = re.sub("(^\*MM)(\-)([A-Z]{3}:)", r"*MOM\2\3", line) # *MM-CHI:
    line = re.sub("(^\*[A-Z]{3}\-[A-Z]{3})(\.)", r"\1:", line) # *NEI-MOM.
    line = re.sub("\*CHI.\s*", "\*CHI:\t", line)

    """

    # fix roles according the CHILDES's depfile.cut 
    # line = line.replace("Target_Chıld", "Target\_Child")
    # participants have to be fixed
    # @ID has to be fixed
    #  @ID:Burcu-may23-2002 -> 
    # @Age of CHI (not declared in .cha format)
    # transcriber tiers are empty
    #  @Media:burcu-may23-2002 -> add "audio video"
    # @activities -> not in depfile.cut
    # KULLD using MOT & MOM interchangeably
    # "xx" not allowed
    # brackets not allowed
    # utterance delimiter always needed (e.g. ".")

    return(line)

# not used - will change *XX1-XX2: -> *XX1
def repair(line):
    m = re.search("(^\*[A-Z]{3})(\-)([A-Z]{3})(:)(.*)", line)
    if not m == None:
        return m.group(1)+m.group(4)+m.group(5)+"\n"+"%act:\t"+m.group(3)

# CHAT REQUIRED HEADER NAMES:
# @Begin
# @Languages
# @Participants
# @ID
# @End

header = ["@UTF8", "@Begin", "@Languages:\ttur"]
no_tab = ["@UTF8", "@Begin", "@End", "@New Episode"]
empty_body = ["%act:", "%err:", "%exp:", "%mor:", "%pho:"] # no longer needed?

# empty_headers = ["@Media", "@ID", "@Age of CHI", "@SEX of CHI", "@Education of MOT", "@Recorder", ]
# obligatory = ["@UTF8", "@Begin", "@Languages:", "@Participants:", "@Options:", "@ID:", "@Media:", "@Angles:", "@End"]
# changeables = ["@Activities:", "@Bck:","@Bg", "@Bg:", "@Blank", "@Comment:", "@Date:","@Eg", "@Eg:", "@EndTurn", "@G:", "@New Episode", "@New Language:", "@Page", "@Situation:", "@T:"]

cc = [1, 2, 6, 7, 8, 130, 26, 96]
def normalize_string(line):
    # remove weird characters
    return ''.join(c for c in line if not ord(c) in cc)

def replacement(line):
    # perform string replacements
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

def process(path):
    # process file contents
    infile = open(path, "r")
    outpath = path.replace(path.ext, ".cha")
    outfile = open(outpath, "w")
    n = 0
    line = infile.readline()
    prev = ""
    while len(line) > 0:
        n += 1
        line = line.strip()
        line = normalize_string(line) # normalize
        line = preprocess(line) # regex preprocess
        line = replacement(line) # string replace
        line = rules(line) # regex replace

        # skip blank lines, etc.
        if line == "" or line == "*" or line == "%":
            line = infile.readline()
            continue

        # skip end lines
        if line.startswith("@end") or line.startswith("@End") or line.startswith("@ End"):
            line = infile.readline()
            continue

        """
        # skip empty header lines
        if line.startswith("@"):
            if not line in no_tab:
                # catch empty header lines and skip them
                if line.endswith(":"):
                    line = infile.readline()
                    # problem here
                    continue
                    """

        # skip empty body lines
        if line in empty_body:
            line = infile.readline()
            continue

        # catch broken lines
        if not line.startswith("*") and not line.startswith("@") and not line.startswith("%"):
            prev += " "+line
            line = infile.readline()
        else:
            if prev:
                outfile.write(prev+"\n")
                # print(prev)
            prev = line
            line = infile.readline()
    
    if prev:
        outfile.write(prev+"\n")
        # print(prev)

    # outfile.write("\n".join(header)+"\n")
    # outfile.write("\n".join(body)+"\n")
    # outfile.write("@End\n")
    outfile.close()
    infile.close()

participants = {}
def get_participants(filepath):
    # load participant data
    with open(filepath, "r") as infile:
        d = csv.DictReader(infile, delimiter=",", quotechar='"')
        for row in d:
            if not row["filename"] in participants:
                participants[row["filename"]] = row["@Participants:"]

def get_id(k):
    pass

ids = {}
def get_ids(filepath):
    # load participant data; assumes filename is at index 0 and file has header
    with open(filepath, "r") as infile:
        d = csv.reader(infile, delimiter=",")
        header = next(d, None) # skip the header
        for row in d:
            filename = row[0]
            k = row[0]
            v = "|".join(row[1:])

def main(dir, type):
    get_replacements("notes/replacements.csv")
    get_participants("notes/participants.csv")
    get_ids("notes/ids.csv")
    print(participants)
    sys.exit(1)

    for f in path(dir).files(type):
        if not f.basename().startswith('.'):
            process(f)
#            print("PROCESSING:", f.basename())
#            sys.exit(1) 


if __name__=="__main__":
    dir = sys.argv[1]
    type = sys.argv[2]
    main(dir, type)
