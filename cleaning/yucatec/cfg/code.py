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
    s = re.sub("^%mor:", "%xmor:", s)
    #This may result in files with two Situation tiers. These will have to be cleaned manually before CLAN will accept them!
    s = re.sub("^@Activities", "@Situation", s)
    s = re.sub("^@Birth of ARM:.*", "@Birth of ARM:\t1994-APR-10\n", s)
    s = re.sub("^@Birth of DAV:.*", "@Birth of DAV:\t1998-APR-18\n", s)
    s = re.sub("^@Birth of Sandi:.*", "@Birth of SAN:\t1993-JUL-23\n", s)
    s = re.sub("^@Translation", "@Translator", s)

    #unification %xspa tier
    s=re.sub("\*ESPA:", "%xspa:", s)
    s=re.sub("\*ESP:", "%xspa:", s)
    s=re.sub("\*ESP.", "%xspa:", s)
    s=re.sub("[^\*]ESP:", "%xspa:", s)

    s=re.sub("Esp:", "%xspa:", s)
    s=re.sub("Esp.", "%xspa:", s)

    s=re.sub("%esp.", "%xspa:", s)
    s=re.sub("%esp_:", "%xspa:", s)
    s=re.sub("%esp :", "%xspa:", s)
    s=re.sub("%esp:", "%xspa:", s)

    s=re.sub("%eng:", "%xspa:", s)
    s=re.sub("%eng;", "%xspa:", s)
    s=re.sub("%eng.", "%xspa:", s)
    s=re.sub("%engL:", "%xspa:", s)
    s=re.sub("%eng :", "%xspa:", s)
    s=re.sub("%eng", "%xspa:", s)

    #unification %xpho tier
    s=re.sub("\*pho:", "%xpho:", s)
    s=re.sub("%fon:", "%xpho:", s)
    s=re.sub("%pho:", "%xpho:", s)
    s=re.sub("%pho.", "%xpho:", s)
    s=re.sub("%pho :", "%xpho:", s)
    s=re.sub("%pho;", "%xpho:", s)
    s=re.sub("^pho:", "%xpho:", s)
    s=re.sub("\s+pho:", "%xpho:", s)
    s=re.sub("%PHO:", "%xpho:", s)
    s=re.sub("%pho", "%xpho:", s)

    #character cleaning; cf. ../notes/yua-chars.ods for notes on characters that need manual attention and/or need to be interpreted by Barbara (corpus owner)
    s = re.sub(" ", " ", s) # unification of two different space types
    s=re.sub("¨(.*)\?", "¿($1)\?", s) # if the dieresis happens at the beginning of a line and then comes "?", then it has to be replaced by "¿"
    #s = re.sub("¨", "", s)
    s = re.sub("¢", "ó", s)
    s = re.sub("’", "'", s)
    s = re.sub("£", "ú", s)
    s = re.sub("\\s‘\\s", "?", s) # other uses of "‘" need manual attention
    s = re.sub("¤", "ñ", s)
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
    #inverted question mark
    s=re.sub("Ts¿a", "Tsʔa", s)
    s=re.sub("k¿aas", "kʔaas", s)
    s=re.sub("yo¿ch", "yoʔch", s)
    s=re.sub("^\*(.*)¿(.*)$", "\*($1)($2)", s) #not allowed in a *PARTICIPANT tier

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
