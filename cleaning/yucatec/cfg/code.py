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
