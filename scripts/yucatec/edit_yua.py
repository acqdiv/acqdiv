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
        with open(os.path.join(root, name), 'r', encoding="utf8") as input_file, open(os.path.join(output_dir, name), 'w', encoding="utf8") as output_file:        
            for line in input_file:
                #unification *PARTICIPANT tier
                #correct participants' IDs:
                line=re.sub(r"\*MECH:", r"*MEC:", line)
                line=re.sub(r"\*:MEC:", r"*MEC:", line)
                line=re.sub(r"\*GOYO:", r"*GOY:", line)
                line=re.sub(r"%GOY:", r"*GOY:", line)
                line=re.sub(r"\*PEPE:", r"*PEP:", line)
                line=re.sub(r"\*ABUE:", r"*ABU:", line)
                line=re.sub(r"\*MARI:", r"*MAR:", line)
                line=re.sub(r"\*MAR[^:]", r"*MAR:", line)
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
                line=re.sub(r"mandav:", r"*FIL:", line)
                line=re.sub(r"\*davdav:", r"*DAV:", line)
                line=re.sub(r"\*davdav", r"*DAV:", line)
                line=re.sub(r"\*davsan:", r"*SAN:", line)
                line=re.sub(r"\*davsan", r"*SAN:", line)
                line=re.sub(r"\*DAv:", r"*DAV:", line)
                line=re.sub(r"^DAV:", r"*DAV:", line)
                line=re.sub(r"DAv:", r"*DAV:", line)
                line=re.sub(r"^\s+DAV:", r"*DAV:", line)
                line=re.sub(r"\*dav\*:", r"*DAV:", line)
                line=re.sub(r"\*dav:", r"*DAV:", line)
                line=re.sub(r"\*dav", r"*DAV:", line)
                line=re.sub(r"\*:DAV", r"*DAV:", line)
                line=re.sub(r"\*DAV :", r"*DAV:", line)
                #line=re.sub(r"\*DAV", r"*DAV:", line)
                line=re.sub(r"dav:", r"*DAV:", line)
                line=re.sub(r"dAV:", r"*DAV:", line)
                line=re.sub(r"[^\*]DAV:", r"*DAV:", line)
                line=re.sub(r"\*san:", r"*SAN:", line)
                line=re.sub(r"\s+SAN:", r"*SAN:", line)
                line=re.sub(r"^\s*san:", r"*SAN:", line)
                line=re.sub(r"^SAN:", r"*SAN:", line)
                line=re.sub(r"%SAN:", r"*SAN:", line)
                line=re.sub(r"[^\*]SAN:", r"*SAN:", line)
                line=re.sub(r"\*SAN :", r"*SAN:", line) # note that it is not the normal whitespace
                line=re.sub(r"[^\*a]san:", r"*SAN:", line)
                line=re.sub(r"\*SAM:", r"*SAN:", line)
                line=re.sub(r"SAN(%pho:)", r"*SAN:\t\.\n\1", line)
                line=re.sub(r"sAN:", r"*SAN:", line)
                line=re.sub(r"SAn:", r"*SAN:", line)
                line=re.sub(r"^\s*FIL:", r"*FIL:", line)
                line=re.sub(r"\*\s+FIL:", r"*FIL:", line)
                line=re.sub(r"\*fil:", r"*FIL:", line)
                line=re.sub(r"\*fil", r"*FIL:", line)
                line=re.sub(r"fil:", r"*FIL:", line)
                line=re.sub(r"\*FIl:", r"*FIL:", line)
                line=re.sub(r"fIL:", r"*FIL:", line)
                line=re.sub(r"%FIL:", r"*FIL:", line)
                line=re.sub(r"\*FIL;", r"*FIL:", line)
                line=re.sub(r"[^\*]FIL:", r"*FIL:", line)
                line=re.sub(r"\*FIL\.", r"*FIL:", line)
                line=re.sub(r"\*mot::", r"*MOT:", line)
                line=re.sub(r"\*mot:", r"*MOT:", line)
                line=re.sub(r"\*arm:", r"*ARM:", line)
                line=re.sub(r"\* Arm:", r"*ARM:", line)
                line=re.sub(r"%ARM:", r"*ARM:", line)
                line=re.sub(r"\*ARM;", r"*ARM:", line)
                line=re.sub(r"[^\*]ARM:", r"*ARM:", line)
                line=re.sub(r"\*ARMcuatro", r"*ARM:\tcuatro", line)
                line=re.sub(r"\*mar:", r"*MAR:", line)
                line=re.sub(r"\*sab:", r"*SAB:", line)
                line=re.sub(r"^\sNEF:", r"*NEF:", line)
                line=re.sub(r"\*NEF[^:]", r"*NEF:", line)
                line=re.sub(r"\*nef:", r"*NEF:", line)
                line=re.sub(r"%NEF:", r"*NEF:", line)
                line=re.sub(r"%NEI:", r"*NEI:", line)
                line=re.sub(r"\* NEI:", r"*NEI:", line)
                line=re.sub(r"[^\*]NEI:", r"*NEI:", line)
                line=re.sub(r"\*lor:", r"*LOR:", line)
                line=re.sub(r"\*LOR\.", r"*LOR:", line)
                line=re.sub(r"[^\*]LOR:", r"*LOR:", line)
                line=re.sub(r"\*:", r"*UNK:", line)
                line=re.sub(r"\*CAR", r"*CAR:", line)
                line=re.sub(r"^\s+:\s$", r"*UNK:", line) # replace ":" at the beginning of a line, with some spaces before and after, with *UNK:
                line=re.sub(r"\*\?:", r"*UNK:", line) # replace "*?:" with "*UNK:"
                line=re.sub(r"\* \?:", r"*UNK:", line) # replace "* ?:" with "*UNK:"
                line=re.sub(r"\(\s+\):", r"*UNK:", line) # replace "(    ):" with "*UNK:"
                line=re.sub(r"xxx:", r"*UNK:", line) # replace "xxx:" with "*UNK:"
                line=re.sub(r"\*XXX:", r"*UNK:", line) # replace "*XXX:" with "*UNK:"
                line=re.sub(r"(\*[A-Z]{3}) :", r"\1:", line) # remove a space between the participant's code and the colon
                line=re.sub(r"\(\s?(\*[A-Z]{3})\s?\):", r"\1:", line) # participant codes with form e.g. "(*ARM):" or "( *SAN ):" should be transformed into "*ARM:"

                #unification %xpho tier
                line=re.sub(r"\*pho:", r"%xpho:", line)
                line=re.sub(r"%fon:", r"%xpho:", line)
                line=re.sub(r"%pho\.", r"%xpho:", line)
                line=re.sub(r"%pho :", r"%xpho:", line) # note that it is not the usual whitespace
                line=re.sub(r"%pho;", r"%xpho:", line)
                line=re.sub(r"^pho:", r"%xpho:", line)
                line=re.sub(r"%PHO:", r"%xpho:", line)
                line=re.sub(r"% pho:", r"%xpho:", line)
                line=re.sub(r"%pho:", r"%xpho:", line)

                #unification %xmor tier
                line=re.sub(r"%MOR:", r"%xmor:", line)
                line=re.sub(r"%mor:", r"%xmor:", line)
                line=re.sub(r"% mor:", r"%xmor:", line)
                line=re.sub(r"\*mor:", r"%xmor:", line)
                line=re.sub(r"%mor\.", r"%xmor:", line)
                line=re.sub(r"%mor\s+:", r"%xmor:", line)
                line=re.sub(r"%mor :", r"%xmor:", line) # note that it is not the usual whitespace

                #unification %spa tier
                line=re.sub(r"\*ESPA:", r"%spa:", line)
                line=re.sub(r"\*ESP:", r"%spa:", line)
                line=re.sub(r"\*ESP\.", r"%spa:", line)
                line=re.sub(r"%ESP:", r"%spa:", line)
                line=re.sub(r"ESP:", r"%spa:", line)

                line=re.sub(r"\*Esp:", r"%spa:", line)
                line=re.sub(r"Esp:", r"%spa:", line)
                line=re.sub(r"Esp\.", r"%spa:", line)

                line=re.sub(r"%esp\.", r"%spa:", line)
                line=re.sub(r"%esp_:", r"%spa:", line)
                line=re.sub(r"%esp :", r"%spa:", line) # note that it is not the usual whitespace
                line=re.sub(r"%esp:", r"%spa:", line)
                line=re.sub(r"%\*esp:", r"%spa:", line)
                line=re.sub(r"\*esp:", r"%spa:", line)
                line=re.sub(r"%:", r"%spa:", line)

                line=re.sub(r"%ENG:", r"%spa:", line)
                line=re.sub(r"%eng: ", r"%spa:	", line) # note that it is not the usual whitespace
                line=re.sub(r"%eng:", r"%spa:", line)
                line=re.sub(r"%eng;", r"%spa:", line)
                line=re.sub(r"%eng\.", r"%spa:", line)
                line=re.sub(r"%engL:", r"%spa:", line)
                line=re.sub(r"%eng :", r"%spa:", line)
                line=re.sub(r"%eng", r"%spa:", line)

                # %com and %sit tiers
                line=re.sub(r"^\s*\((.*)\)$", r"%com:\t\1", line) # place lines with comments in brackets into a %com tier
                line=re.sub(r"^&", r"%com:\t", line) # place lines which start with "&" into a %com tier
                line=re.sub(r"^< (.*) >", r"%com:\t\1", line) # place lines with comments in < > into a %com tier

                line=re.sub(r"\s###\s", r" xxx ", line)
                line=re.sub(r"XXX", r"xxx", line)
                line=re.sub(r"XX", r"xxx", line)
                line=re.sub(r"\. \. \.", r"...", line)
                line=re.sub(r"\s\.\.\s", r"...", line)
                line=re.sub(r"¿\?\?\?", r"?", line)
                line=re.sub(r"¿\?\?", r"?", line)
                line=re.sub(r"\?{2,3,4,5,6,7,8,9}", r"?", line)
                line=re.sub(r"\-x\-x\-x\-", r"", line)
                line=re.sub(r"<\s*Sandi y Armando\s*>", r"", line)

                line=re.sub(r"^\s*[0-9]+\s*(\*[A-Z]{3}:)", r"\1", line) # remove spaces, numbers and/or spaces before *PARTICIPANT tiers
                line=re.sub(r"^\s*[0-9]{3}:\s*(\*[A-Z]{3}:)", r"\1", line)
                line=re.sub(r"^\s*[0-9]+\s*(%[a-z]{3,4}:)", r"\1", line) # remove spaces, numbers and/or spaces before %xxx and %xmor tiers
                line=re.sub(r"^\s*(\*[A-Z]{3}:)", r"\1", line) # remove spaces or tabs before *PARTICIPANT tiers
                line=re.sub(r"^\s*(%[a-z]{3,4}:)", r"\1", line) # remove spaces or tabs before %xxx and %xmor tiers
                line=re.sub(r"^\s*[0-9]+\s*$", r"", line) # remove numbers and/or spaces alone in a line
                line=re.sub(r"^\t*[0-9]+\t*$", r"", line) # remove numbers and/or tabs alone in a line
                line=re.sub(r"^\s*([%|\*])", r"\1", line) # remove all spaces before the beginning of a tier


                # place two different tiers that were in one line into two different lines
                line=re.sub(r"%(.*?)(\*[A-Z]{3}:)", r"%\1\n\2", line)
                line=re.sub(r"(\*[A-Z]{3}:)(.*?)%", r"\1\2\n%", line)
                #line=re.sub(r"(%xmor:)\s*(%spa:)(.*?)$", r"\1\t\n\2\3", line)
                line=re.sub(r"%(.*?)%", r"%\1\n%", line)
                #line=re.sub(r"(\*[A-Z]{3}:)\s*(.*?)$", r"\1\t\2\n", line)
                line=re.sub(r"%(.*?)%(.*?)%", r"%\1\n%\2\n%", line)


                # all tier names must be followed by a tab before the tier content starts (this block has to be in both edit_yua.py and code.py)
                #line=re.sub(r"(%[a-z]{3,4}:)\s*(.*?)$", r"\1\t\2\n", line)
                #line=re.sub(r"(\*[A-Z]{3}:)\s*(.*?)$", r"\1\t\2", line)
                #line=re.sub(r"(%[a-z]{3,4}:)\s*(.*?)$", r"\1\t\2", line)
                line=re.sub(r"(\*[A-Z]{3}:)\s*$", r"\1\t\n", line)
                line=re.sub(r"(%[a-z]{3,4}:)\s*$", r"\1\t\n", line)
                #line=re.sub(r"(\*[A-Z]{3}:)([A-Za-z]+)", r"\1\t\2", line)
                #line=re.sub(r"(%[a-z]{3,4}:)([A-Za-z]+)", r"\1\t\2", line)
                line=re.sub(r"(\*[A-Z]{3}:) *\t* *([A-Za-záéíóú\[\(¡\?]+)", r"\1\t\2", line)
                line=re.sub(r"(%[a-z]{3,4}:) *\t* *([A-Za-záéíóú\[\(¡\?]+)", r"\1\t\2", line)
                #line=re.sub(r"(\*[A-Z]{3}:) *([A-Za-z\[\(¡]*)", r"\1\t\2", line)
                #line=re.sub(r"(%[a-z]{3,4}:) *([A-Za-z\[\(¡])", r"\1\t\2", line)
                line=re.sub(r"(\*[A-Z]{3}:)\s*\n", r"\1\t\n", line)
                line=re.sub(r"(%[a-z]{3,4}:)\s*\n", r"\1\t\n", line)
                line=re.sub(r"(\*[A-Z]{3}:)\t\t([A-Za-z\[\(¡\?]+)", r"\1\t\2", line)
                line=re.sub(r"(%spa:)\t\t([A-Za-z\[\(¡\?]+)", r"\1\t\2", line)
                line=re.sub(r"(\*[A-Z]{3}:) *\.$", r"\1\t.", line)
                line=re.sub(r"(%[a-z]{3,4}:) *\.$", r"\1\t.", line)

                if line.startswith("%xpho"):
                    line=re.sub(r"\-", r"", line) # remove "-" in %pho tiers
                    line=re.sub(r"\.", r"", line) # remove dots in %pho tiers
                    line=re.sub(r"\/", r"", line) # remove "/" in %pho tiers
                    #line=re.sub(r" $\n", r"\n", line) # remove whitespaces at the end of %pho tiers
                    line=re.sub(r"\s[\.\?\!;,]+\s*$\n", r"\n", line) # remove dot/ending mark in %pho tiers
                    line=re.sub(r" ", r"", line) # remove weird whitespaces in %pho tiers

                if line.startswith("*"):
                    line=re.sub(r"/", r"", line) # remove "/" in *PARTICIPANT tiers
                    line=re.sub(r"\+", r" ", line)
                    line=re.sub(r"(\*[A-Z]{3}:\t)$\n", r"\1.\n", line) # add a dot at the end of empty *PARTICIPANT tiers
                    line=re.sub(r"\.\.\.", r" (...) ", line)
                    line=re.sub(r"¿", r"", line) # remove "¿" in *PARTICIPANT tiers
                    line=re.sub(r"¡", r"", line) # remove "¡" in *PARTICIPANT tiers

                if line.startswith("%spa"):
                    line=re.sub(r"¿", r"", line) # remove "¿" in %spa tiers


                #line=re.sub(r"(%pho:)(.*)/(.*)/", r"\1\2\3", line) # remove "/" twice in %pho tiers
                #line=re.sub(r"(%pho:)(.*)/", r"\1\2", line) # remove "/" once in %pho tiers
                #line=re.sub(r"(\*[A-Z]{3}:\t)(.*?)/", r"\1\2", line) # remove "/" in *PARTICIPANT tiers
                line=re.sub(r"\s*n$", r"", line) # remove lines which have only "n"
                line=re.sub(r"(%xpho:\s*)!", r"\1", line) # remove "!" at the beginning of a %pho tier
                line=re.sub(r"(\*[A-Z]{3}:\s*)\?[^$]", r"\1", line) # remove "?" at the beginning of a *PARTICIPANT tier
                line=re.sub(r"(\*[A-Z]{3}:\s*)\!", r"\1", line) # remove "!" at the beginning of a *PARTICIPANT tier
                #line=re.sub(r"(%spa:\s*)\?[^$]", r"\1", line) # remove "?" at the beginning of a %spa tier
                #line=re.sub(r"(%spa:\s*)\?[^$]", r"\1", line) # remove "?" at the beginning of a %spa tier, again
                line=re.sub(r"(%spa:\s*)\![^$]", r"\1", line) # remove "!" at the beginning of a %spa tier
                line=re.sub(r"(%xmor:\s*)\?", r"\1.", line) # replace "?" at the beginning of a %xmor tier with a dot
                line=re.sub(r"^(.*)\*$", r"\1\n", line) # remove asterisk at the end of a line
                line=re.sub(r"^\s*\.$", r"", line) # remove lines which have only " ."
                line=re.sub(r"(%xmor:)(.*)\\", r"\1\2\|", line) # in %xmor tiers, replace "\" with "|"
                line=re.sub(r"¡$", r"!", line) # at the end of a line, "¡" has to be "!"



                #line = re.sub('^\d*\s+(?=[\*%])', '', line)
                print(line, file=output_file, end='')