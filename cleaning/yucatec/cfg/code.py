def clean_filename(fname):
    return fname.rstrip(".txt")

def clean_chat_line(s):
    s = re.sub(":\s+", ":\t", s, 1)
    s = re.sub("^@Begi$", "@Begin", s)
    s = re.sub("^@Fin$", "@End", s)
    s = re.sub("\s###\s", "\sxxx\s", s)
    s = re.sub("XXX", "xxx", s)
    s = re.sub("(^[\*%]\S+\t+[^\t]+)\t", "\1", s)
    s = re.sub("(\w)['’ʼ]", "\\1ʔ", s)
    s = re.sub("['’ʼ](\w)", "ʔ\\1", s)
    s = re.sub("(\w)['’ʼ](\w)", "\\1ʔ\\2", s)
    #This may result in files with two Situation tiers. These will have to be cleaned manually before CLAN will accept them!
    s = re.sub("^@Activities", "@Situation", s)
    s = re.sub("^@Birth of ARM:.*", "@Birth of ARM:\t1994-APR-10\n", s)
    s = re.sub("^@Birth of DAV:.*", "@Birth of DAV:\t1998-APR-18\n", s)
    s = re.sub("^@Birth of Sandi:.*", "@Birth of SAN:\t1993-JUL-23\n", s)
    s = re.sub("^@Translation", "@Translator", s)


    ### TIER NAMES CLEANING ###
    #unification *PARTICIPANT tier
    #correct participants' IDs:
    s=re.sub(r"\*MECH:", r"*MEC:", s)
    s=re.sub(r"\*GOYO:", r"*GOY:", s)
    s=re.sub(r"\*PEPE:", r"*PEP:", s)
    s=re.sub(r"\*ABUE:", r"*ABU:", s)
    s=re.sub(r"\*MARI:", r"*MAR:", s)
    s=re.sub(r"\*CHIC:", r"*CHI:", s)
    s=re.sub(r"\*SANI:", r"*SAN:", s)
    s=re.sub(r"\*ABUELA:", r"*ABU:", s)
    s=re.sub(r"ABUELA:", r"*ABU:", s)
    s=re.sub(r"\*MAMDAV:", r"*FIL:", s)
    s=re.sub(r"\*mamdav:", r"*FIL:", s)
    s=re.sub(r"\*mamdav\*:", r"*FIL:", s)
    s=re.sub(r"\*mamdav", r"*FIL:", s)
    s=re.sub(r"mamdav:", r"*FIL:", s)
    s=re.sub(r"mamdav", r"*FIL:", s)
    s=re.sub(r"\*davdav:", r"*DAV:", s)
    s=re.sub(r"\*davdav", r"*DAV:", s)
    s=re.sub(r"\*davsan:", r"*SAN:", s)
    s=re.sub(r"\*davsan", r"*SAN:", s)
    s=re.sub(r"\*dav\*:", r"*DAV:", s)
    s=re.sub(r"\*dav:", r"*DAV:", s)
    s=re.sub(r"\*dav", r"*DAV:", s)
    s=re.sub(r"\*san:", r"*SAN:", s)
    s=re.sub(r"\*fil:", r"*FIL:", s)
    s=re.sub(r"\*fil", r"*FIL:", s)
    s=re.sub(r"fil:", r"*FIL:", s)
    s=re.sub(r"\*mot::", r"*MOT:", s)
    s=re.sub(r"\*mot:", r"*MOT:", s)
    s=re.sub(r"\*arm:", r"*ARM:", s)
    s=re.sub(r"\*mar:", r"*MAR:", s)
    s=re.sub(r"\*nef:", r"*NEF:", s)
    s=re.sub(r"\*lor:", r"*LOR:", s)
    s=re.sub(r"\*:", r"*UNK:", s)
    s=re.sub(r"\*([A-Z]{3}) :", r"*\1:", s) # if there is a space between the participant's code and the colon, remove it.
    s=re.sub(r"\(\s?(\*[A-Z]{3})\s?\):", r"\1:", s) # participant codes with form e.g. "(*ARM):" or "( *SAN ):" should be transformed into "*ARM:"

    #remove numbers and spaces before the participant's ID so that only the asterisk and code appear:
    s=re.sub(r"[0-9]+(.*)\*([A-Z]{3}:)", r"*\2", s)
    #s=re.sub(r"[0-9]+(.*)\*([A-Z]{4}:)", r"*\2", s) # if the participants' IDs have been changed first, these two are no longer needed. Left here for final checking.
    #s=re.sub(r"[0-9]+(.*)\*([A-Z]{6}:)", r"*\2", s)

    #unification %xpho tier
    s=re.sub(r"\*pho:", r"%xpho:", s)
    s=re.sub(r"%fon:", r"%xpho:", s)
    s=re.sub(r"%pho:", r"%xpho:", s)
    s=re.sub(r"%pho.", r"%xpho:", s)
    s=re.sub(r"%pho :", r"%xpho:", s)
    s=re.sub(r"%pho;", r"%xpho:", s)
    s=re.sub(r"^pho:", r"%xpho:", s)
    s=re.sub(r"%PHO:", r"%xpho:", s)
    s=re.sub(r"%pho", r"%xpho:", s)

    #unification %xmor tier
    s=re.sub(r"%MOR:", r"%xmor:", s)    
    s=re.sub(r"\*mor:", r"%xmor:", s)    
    s=re.sub(r"%mor.", r"%xmor:", s)    
    s=re.sub(r"%mor:", r"%xmor:", s)
            
    #unification %xspa tier
    s=re.sub(r"\*ESPA:", r"%xspa:", s)
    s=re.sub(r"\*ESP:", r"%xspa:", s)
    s=re.sub(r"\*ESP.", r"%xspa:", s)
    s=re.sub(r"[^\*]ESP:", r"%xspa:", s)

    s=re.sub(r"Esp:", r"%xspa:", s)
    s=re.sub(r"Esp.", r"%xspa:", s)

    s=re.sub(r"%esp.", r"%xspa:", s)
    s=re.sub(r"%esp_:", r"%xspa:", s)
    s=re.sub(r"%esp :", r"%xspa:", s)
    s=re.sub(r"%esp:", r"%xspa:", s)
    s=re.sub(r"%\*esp:", r"%xspa:", s)
    s=re.sub(r"\*esp:", r"%xspa:", s)

    s=re.sub(r"%ENG:", r"%xspa:", s)
    s=re.sub(r"%eng:", r"%xspa:", s)
    s=re.sub(r"%eng;", r"%xspa:", s)
    s=re.sub(r"%eng.", r"%xspa:", s)
    s=re.sub(r"%engL:", r"%xspa:", s)
    s=re.sub(r"%eng :", r"%xspa:", s)
    s=re.sub(r"%eng", r"%xspa:", s)

    ### CHARACTER CLEANING ###
    # cf. ../notes/yua-chars.ods for notes on characters that need manual attention and/or need to be interpreted by Barbara (corpus owner)
    s = re.sub(" ", " ", s) # unification of two different space types
    s=re.sub(r"¨(.*)\?", r"¿\1\?", s) # if the dieresis happens at the beginning of a line and later comes "?", then the dieresis has to be replaced by "¿"
    s = re.sub("¢", "ó", s)
    s = re.sub("’", "'", s)
    s = re.sub("£", "ú", s)
    s = re.sub("\\s‘\\s", "?", s) # other uses of "‘" need manual attention
    s = re.sub("¤", "ñ", s)
    s=re.sub("hńn", "hnn", s)
    s=re.sub("ń", "ñ", s)
    s = re.sub("^.+?\\\\.+?$", "", s) # backslashes only occur in lines of jumbled characters (probably information lost from .doc to .txt)
    s = re.sub("^.+?¸.+?$", "", s) # "¸" only occurs in lines of jumbled characters (probably information lost from .doc to .txt)
    s = re.sub("ç", "", s)
    s = re.sub("Æ", "'", s)
    s = re.sub("^.+?Ø.+?$", "", s) # "Ø" only occurs in lines of jumbled characters (probably information lost from .doc to .txt)
    s = re.sub("sÏ", "sí", s)
    s = re.sub("ï", "'", s)
    s = re.sub("Í", "í", s)
    s = re.sub("ë", "é", s)
    s = re.sub("°", "", s)
    s=re.sub("ż", "¿", s)

    #inverted question mark
    s=re.sub(r"^\*([A-Z]{3}:)(.*)¿(.*)$", r"*\1\2\3", s) # not allowed in a *PARTICIPANT tier
    s=re.sub(r"^%xpho:(.*)¿(.*)$", r"%xpho:\1\2", s) # not allowed in a %xpho tier
    s=re.sub(r"%xspa:(.*)¿$", r"%xspa:\1\?", s) # at the end of a %xspa tier, "¿" has to be "?"

    #inverted exclamation mark
    s=re.sub("all¡", "allí", s) # these four refer to consistent errors across the corpus and they simplify the application of other rules below.
    s=re.sub("as¡", "así", s)
    s=re.sub("aqu¡", "aquí", s)
    s=re.sub("ah¡", "ahí", s)


    #cleanup unwanted tiers
    #added by chysi
    s = re.sub("^@Edad.*", "", s)
    s = re.sub("^@Age.*", "", s)
    s = re.sub("^@Birth of Armando.*", "", s)
    s = re.sub("^@Birth of David.*", "", s)
    s = re.sub("^@Birth of child.*", "", s)
    s = re.sub("^@Fecha.*", "", s)
    s = re.sub("^@Font.*", "", s)
    s = re.sub("^@Filename.*", "", s)
    s = re.sub("^@Nombre del Archivo.*", "", s)
    s = re.sub("^@Note.*", "", s)
    s = re.sub("^@Sex.*", "", s)

    if s.startswith("*"):
        s = re.sub("##", "", s)
        s = re.sub("#", "", s)
        s = re.sub("(\\S)\-(\\S)", "\\1\\2", s)
        s = re.sub("^\\s*\\d+\\s+(?=[\*%])", "", s)

        # added by rabart
        s = re.sub('\-?0', '', s)
        s = re.sub('(?<=\\w)&(?=[au])', '', s)

    if s.startswith("%eng"):
        s = re.sub("\[\\s*", "", s)
        s = re.sub("\\s*\]", "", s)
        
        # added by rabart
        s = re.sub('[\(\)]\\s*', '', s) # delete brackets and following spaces
        s = re.sub('%eng:\\s+', '%eng:\\t', s) # replace any spaces left by tab

    if s.startswith("%sit"):
        # added by rabart
        s = re.sub('[()]\s', '', s) # delete brackets and following spaces
        s = re.sub('%sit:\\s+', '%eng:\\t', s) # replace any spaces left by tab
        
    # fix errors in the pho line
    if s.startswith("%pho:"):
        s = re.sub("\.\.\.", ":", s)
        s = re.sub("/", "", s)
        s = re.sub("(?<=\w)[\.,]", "", s)
        s = re.sub("[\.,]\s*$", "", s)
        s = re.sub("\s\.\s", " (.) ", s)
        s = re.sub("\.\n", "\n", s)
        s = re.sub("\t\s", "\t", s)
        s = re.sub('[\?.!]', '', s)

    #miscellaneous errors
    #added by chysi
    if s.startswith("@Pía un pollito."):
        s = re.sub("@", "%sit:\t", s)

    return s
