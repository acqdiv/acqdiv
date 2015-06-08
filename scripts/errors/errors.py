import sys
import logging
import regex as re
from path import path

logging.basicConfig(filename='errors.log', level=logging.DEBUG, filemode='w')

obligatory = ["@UTF8", "@Begin", "@Languages:", "@Participants:", "@Options:", "@ID:", "@Media:", "@Angles:", "@End"]
no_tab = ["@UTF8", "@Begin", "@End", "@New Episode"]
changeables = ["@Activities:", "@Bck:", "@Bg", "@Bg:", "@Blank", "@Comment:", "@Date:", "@Eg", "@Eg:", "@EndTurn", "@G:", "@New Episode", "@New Language:", "@Page", "@Situation:", "@T:"]

participants = 
"Target_Child",
"Target_Adult",
"Child",
"Mother",
"Father",
"Brother",
"Sister",
"Sibling",
"Grandmother",
"Grandfather",
"Aunt",
"Uncle",
"Cousin",
"Family_Friend",
"Student",
"Teacher",
"Playmate",
"Visitor",
"Babysitter",
"Caretaker",
"Housekeeper",
"Investigator",
"Observer",
"Clinician",
"Therapist",
"Interviewer",
"Informant",
"Participant",
"Subject",
"Partner",
"Doctor",
"Nurse",
"Patient",
"Unidentified",
"Uncertain",
"Camera_Operator",
"Group",
"Narrator",
"Adult",
"Teenager",
"Boy",
"Girl",
"Male",
"Female",
"Non_Human",
"Toy",
"Media",
"Environment",
"OffScript",
"Text",
"PlayRole",
"Justice",
"Judge",
"Attorney",
"Speaker",
"Audience",
"ShowHost",
"ShowGuest",
"Operator",
"Caller",
"CallTaker"]



def main(path):
    infile = open(path, "r")
    n = 0
    for line in infile:
        n += 1
        line = line.strip()
        
        # get header lines without tabs
        if line.startswith("@") and not line.__contains__("\t") and not line in no_tab:
            logging.debug(str(path)+":"+str(n)+"\tHEADER MISSING TAB\t"+line)

        # get broken lines / lines without valid start character
        if not line.startswith("*") and not line.startswith("@") and not line.startswith("%"):
            logging.debug(str(path)+":"+str(n)+"\tMISSING LINE IDENTIFIER\t"+line)

        # get all lines without tabs
        if not line.__contains__("\t") and not line in no_tab:
            logging.debug(str(path)+":"+str(n)+"\tMISSING TAB\t"+line)

        if not line in no_tab and not line.__contains__(":"):
            logging.debug(str(path.basename())+":"+str(n)+"\tMISSING COLON\t"+line)


        """        
        if not line.__contains__(":") and not line.startswith("@"):
            logging.debug(str(path.basename())+":"+str(n)+"\tMISSING COLON\t"+line)

        if not line.startswith("@") and not line.startswith("%"):
            m = re.search("^((?!\*[A-Z]{3}(?:\-[A-Z]{3})?:).)*$", line)
            if m:
                logging.debug(str(path)+":"+str(n)+"\tINCORRECT PARTICIPANT CODE\t"+line)

        # (almost) every line should have a tab
        if not line in no_tab and not line.__contains__("\t"):
            # if no tab and nothing to split, add to replacements file
            if not line.__contains__(":"):
                print(path.basename()+"\t"+line)

        # header errors
        if line.startswith("@"):
            if not line in no_tab and not line in changeables:
                # catch empty header lines
                if line.endswith(":"):
                    logging.debug(str(path)+":"+str(n)+"\tEMPTY HEADER LINE\t"+line)
                # catch missing tabbed lines
                elif not line.__contains__("\t"):
                    logging.debug(str(path)+":"+str(n)+"\tNO TAB IN LINE\t"+line)
                    tokens = line.split(":")
                    print("\t".join(tokens))

        # quick cha checks
        if line.startswith("*") or line.startswith("%"):
            if not line.__contains__("\t"): # and not line in skip_tiers:
                logging.debug(str(path)+":"+str(n)+"\tNO TAB IN LINE\t"+line)

        if not line.startswith("@") and not line.startswith("%") and not line.startswith("*") and not line == "":
            if len(line) == 1:
                logging.debug(str(path)+":"+str(n)+"\tINCORRECT START CHAR\t"+str(ord(line))+" "+line)

        if line.startswith("@"):
            if line.__contains__(":") and not line.__contains__("\t"):
                print(path.namebase+"\t"+line)
                """
                
    infile.close()

if __name__=="__main__":
    dir = sys.argv[1]
    type = sys.argv[2]
    for f in path(dir).files(type):
        if not f.basename().startswith('.'):
            main(f)
