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
    
    
    main tier:
    re.sub('-?0', '', tier)
    re.sub('(?<=\w)&(?=[au])', '', tier)

    %eng: and %sit: tier:
    re.sub('[()]\s', '', tier) # delete brackets and following spaces
    re.sub('%(eng|sit):\s(', '\1', tier) # also delete preceding space when bracket directly follows tier marker    

    if s.startswith("*"):
        s = re.sub("##", "", s)
        s = re.sub("#", "", s)
        s = re.sub("(\\S)\-(\\S)", "\\1\\2", s)
        s = re.sub("^\\s*\\d+\\s+(?=[\*%])", "", s)

    if s.startswith("%eng"):
        s = re.sub("\[\\s*", "", s)
        s = re.sub("\\s*\]", "", s)
        s = re.sub('[\(\)]\\s*', '', s) # delete brackets and following spaces
        s = re.sub('%eng:\\s+', '%eng:\\t', s) # replace any spaces left by tab

    if s.startswith("%sit"):
        s = re.sub('[()]\s', '', s) # delete brackets and following spaces
        s = re.sub('%sit:\\s+', '%eng:\\t', s) # replace any spaces left by tab
        
    # fix erros in the pho line
    if s.startswith("%pho:"):
        s = re.sub("\.\.\.", ":", s)
        s = re.sub("/", "", s)
        s = re.sub("(?<=\w)[\.,]", "", s)
        s = re.sub("[\.,]\s*$", "", s)
        s = re.sub("\s\.\s", " (.) ", s)
        s = re.sub("\.\n", "\n", s)
        s = re.sub("\t\s", "\t", s)
        s = re.sub('[\?.!]', '', s)

    return s
