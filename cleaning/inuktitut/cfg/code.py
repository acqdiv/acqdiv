def clean_filename(fname): 
    return fname.rstrip(".NAC").rstrip(".XXS").rstrip(".XXX").rstrip(".MAY")

def clean_chat_line(s):
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

    return s
