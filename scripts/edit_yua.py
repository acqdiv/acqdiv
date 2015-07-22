#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Make simple regex replacements in all files in a directory
Usage: python3 edit.py path/to/dir
'''

import os
import re
import sys

try:
    input_dir = sys.argv[1]
except IndexError:
    input_dir = os.getcwd()

for root, dirs, files in os.walk(input_dir):
    output_dir = re.sub('\/?$', '_edited/', root)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for name in files:
        with open(os.path.join(root, name), 'r') as input_file, open(os.path.join(output_dir, name), 'w') as output_file:        
            for line in input_file:
				#unification *PARTICIPANT tier
				#correct participants' IDs:
                line=re.sub(r"\*MECH:", r"*MEC:", line)
                line=re.sub(r"\*:MEC:", r"*MEC:", line)
                line=re.sub(r"\*GOYO:", r"*GOY:", line)
                line=re.sub(r"\*PEPE:", r"*PEP:", line)
                line=re.sub(r"\*ABUE:", r"*ABU:", line)
                line=re.sub(r"\*MARI:", r"*MAR:", line)
                line=re.sub(r"\*CHIC:", r"*CHI:", line)
                line=re.sub(r"\*SANI:", r"*SAN:", line)
                line=re.sub(r"\*ABUELA:", r"*ABU:", line)
                line=re.sub(r"ABUELA:", r"*ABU:", line)
                line=re.sub(r"\*MAMDAV:", r"*FIL:", line)
                line=re.sub(r"\*mamdav:", r"*FIL:", line)
                line=re.sub(r"\*mamdav\*:", r"*FIL:", line)
                line=re.sub(r"\*mamdav", r"*FIL:", line)
                line=re.sub(r"mamdav:", r"*FIL:", line)
                line=re.sub(r"mamdav", r"*FIL:", line)
                line=re.sub(r"\*davdav:", r"*DAV:", line)
                line=re.sub(r"\*davdav", r"*DAV:", line)
                line=re.sub(r"\*davsan:", r"*SAN:", line)
                line=re.sub(r"\*davsan", r"*SAN:", line)
                line=re.sub(r"\*dav\*:", r"*DAV:", line)
                line=re.sub(r"\*dav:", r"*DAV:", line)
                line=re.sub(r"\*dav", r"*DAV:", line)
                line=re.sub(r"\*:DAV", r"*DAV:", line)
                line=re.sub(r"\*DAV :", r"*DAV:", line)
                line=re.sub(r"\*DAV", r"*DAV:", line)
                line=re.sub(r"dav:", r"*DAV:", line)
                line=re.sub(r"\*san:", r"*SAN:", line)
                line=re.sub(r"\*fil:", r"*FIL:", line)
                line=re.sub(r"\*fil", r"*FIL:", line)
                line=re.sub(r"fil:", r"*FIL:", line)
                line=re.sub(r"\*FIl:", r"*FIL:", line)
                line=re.sub(r"\*mot::", r"*MOT:", line)
                line=re.sub(r"\*mot:", r"*MOT:", line)
                line=re.sub(r"\*arm:", r"*ARM:", line)
                line=re.sub(r"\* Arm:", r"*ARM:", line)
                line=re.sub(r"\*mar:", r"*MAR:", line)
                line=re.sub(r"\*nef:", r"*NEF:", line)
                line=re.sub(r"\*lor:", r"*LOR:", line)
                line=re.sub(r"\*:", r"*UNK:", line)
                line=re.sub(r"^\s+:\s$", r"*UNK:", line) # replace ":" at the beginning of a line, with some spaces before and after, with *UNK:
                line=re.sub(r"\*\?:", r"*UNK:", line) # replace "*?:" with "*UNK:"
                line=re.sub(r"\(\s+\):", r"*UNK:", line) # replace "(    ):" with "*UNK:"
                line=re.sub(r"xxx:", r"*UNK:", line) # replace "xxx:" with "*UNK:"
                line=re.sub(r"\*XXX:", r"*UNK:", line) # replace "*XXX:" with "*UNK:"
                line=re.sub(r"(\*[A-Z]{3}) :", r"\1:", line) # remove a space between the participant's code and the colon
                line=re.sub(r"\(\s?(\*[A-Z]{3})\s?\):", r"\1:", line) # participant codes with form e.g. "(*ARM):" or "( *SAN ):" should be transformed into "*ARM:"

                #unification %pho tier
                line=re.sub(r"\*pho:", r"%pho:", line)
                line=re.sub(r"%fon:", r"%pho:", line)
                line=re.sub(r"%pho\.", r"%pho:", line)
                line=re.sub(r"%pho :", r"%pho:", line) # note that it is not the usual whitespace
                line=re.sub(r"%pho;", r"%pho:", line)
                line=re.sub(r"^pho:", r"%pho:", line)
                line=re.sub(r"%PHO:", r"%pho:", line)

                #unification %mor tier
                line=re.sub(r"%MOR:", r"%mor:", line)
                line=re.sub(r"\*mor:", r"%mor:", line)
                line=re.sub(r"%mor\.", r"%mor:", line)
                line=re.sub(r"%mor\s+:", r"%mor:", line)
                line=re.sub(r"%mor :", r"%mor:", line) # note that it is not the usual whitespace

                #unification %xspa tier
                line=re.sub(r"\*ESPA:", r"%xspa:", line)
                line=re.sub(r"\*ESP:", r"%xspa:", line)
                line=re.sub(r"\*ESP\.", r"%xspa:", line)
                line=re.sub(r"%ESP:", r"%xspa:", line)
                line=re.sub(r"ESP:", r"%xspa:", line)

                line=re.sub(r"Esp:", r"%xspa:", line)
                line=re.sub(r"Esp\.", r"%xspa:", line)

                line=re.sub(r"%esp\.", r"%xspa:", line)
                line=re.sub(r"%esp_:", r"%xspa:", line)
                line=re.sub(r"%esp :", r"%xspa:", line) # note that it is not the usual whitespace
                line=re.sub(r"%esp:", r"%xspa:", line)
                line=re.sub(r"%\*esp:", r"%xspa:", line)
                line=re.sub(r"\*esp:", r"%xspa:", line)

                line=re.sub(r"%ENG:", r"%xspa:", line)
                line=re.sub(r"%eng:", r"%xspa:", line)
                line=re.sub(r"%eng;", r"%xspa:", line)
                line=re.sub(r"%eng\.", r"%xspa:", line)
                line=re.sub(r"%engL:", r"%xspa:", line)
                line=re.sub(r"%eng :", r"%xspa:", line)
                line=re.sub(r"%eng", r"%xspa:", line)

                # placing uncategorized comments into a %com tier
                line=re.sub(r"^\((.*)\)$", r"%com:\t\1", line) # lines with comments in brackets
                line=re.sub(r"^&", r"%com:\t", line) # lines which start with "&"

                # all tier names must be followed by a tab before the tier content starts
                line=re.sub(r"(\*[A-Z]{3}:)\s+", r"\1\t", line)
                line=re.sub(r"(%[a-z]{3}:)\s+", r"\1\t", line)

                line=re.sub(r"\s###\s", r" xxx ", line)
                line=re.sub(r"XXX", r"xxx", line)

                line=re.sub(r"^\s+[0-9]+\s+(\*[A-Z]{3}:)", r"\1", line) # remove spaces, numbers and spaces before *PARTICIPANT tiers
                line=re.sub(r"^\s+[0-9]+\s+(%[a-z]{3}:)", r"\1", line) # remove spaces, numbers and spaces before %xxx tiers
                line=re.sub(r"^\s+[0-9]+\s+(%xspa:)", r"\1", line) # remove spaces, numbers and spaces before %xspa tiers
                line=re.sub(r"^\s+(\*[A-Z]{3}:)", r"\1", line) # remove spaces before *PARTICIPANT tiers
                line=re.sub(r"^\s+(%[a-z]{3}:)", r"\1", line) # remove spaces before %xxx tiers
                line=re.sub(r"^\s+(%xspa:)", r"\1", line) # remove spaces before %xspa tiers
                line=re.sub(r"^\t+(\*[A-Z]{3}:)", r"\1", line) # remove tabs before *PARTICIPANT tiers
                line=re.sub(r"^\t+(%[a-z]{3}:)", r"\1", line) # remove tabs before %xxx tiers
                line=re.sub(r"^\t+(%xspa:)", r"\1", line) # remove tabs before %xspa tiers
                line=re.sub(r"^\s+[0-9]+\s+$", r"", line) # remove numbers and/or spaces alone in a line
                line=re.sub(r"^\t+[0-9]+\t+$", r"", line) # remove numbers and/or tabs alone in a line
                #line=re.sub(r"^\s+([%|\*])", r"\1", line) # remove all spaces before the beginning of a tier

                # place two different tiers that were in one line into two different lines
                line=re.sub(r"^(\*[A-Z]{3}:)(.*?)(%[a-z]{3}:)(.*?)$", r"\1\2\n\3\4", line)
                line=re.sub(r"^(%[a-z]{3}:)(.*?)(%[a-z]{3}:)(.*?)$", r"\1\2\n\3\4", line)

                #line = re.sub('^\d*\s+(?=[\*%])', '', line)
                print(line, file=output_file, end='')
