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

    # removes empty dependent tiers.
    s = re.sub("^%.{3,4}:$", "", s)
    s = re.sub("\n ", "\n\t", s, re.M)

    # Since replacements.csv is not used anymore
    s = re.sub("@Break", "@New Episode", s)

    # Maybe, I could always insert a @Situation when there is a ":" after "@New Episode"
    s = re.sub("@New Episode:", "@New Episode\n@Situation:", s)

    s = re.sub("\(repeated six times\)", "[x 6]", s)
    s = re.sub("([0-9]+)x", "[x \\1]", s)

    # Removes tabs in the middle of the lines
    # (Couldn't find a way to do this with only one string)
    l = s.split('\t', 1)
    if (len(l) == 2):
        s2 = re.sub("\s+", " ", l[1])
        s = l[0] + '\t' + s2

    # added by rabart
    # replace morphosyntactic annotation by xmor, xcod etc.
    s = re.sub("^%(mor|arg|cod|snd):", "%x\\1:", s)

    s = re.sub("\\s*#\\s*", " ", s) # single "#" on any tier probably marks some kind of break -> delete

    if s.startswith("*"):
        s = re.sub("(\d+)(x)", "\\2 \\1", s)
        s = re.sub("(x)(\d+)", "\\1 \\2", s)
        s = re.sub("\s\(?(\d+)\s+x\)?(\s|$)", " [x \\1] ", s)
        s = re.sub("\s\(?x\s+(\d+)\)?(\s|$)", " [x \\1] ", s)
        s = re.sub("([^\.\?!]$)", "\\1 .", s)
        s = re.sub(",", "", s)
        
        # added by rabart
        s = re.sub('(?<=\\w)\+[\.,\/]*$', '', s)
        s = re.sub('(?<=\\w)\+\.\.\.\s+(?=\\w)', ' ', s)
        s = re.sub('(?<=\\w)\+\.\\s\.$', ' +.', s) # transcription break + utterance delimiter -> utterance delimiter
        s = re.sub('(\\S+)\+\.(?=\\s\\w)', '&\\1', s) # "transcription break" followed by words really marks fragments
        s = re.sub('(?<=\\w)\?!', ',', s) # some utterance delimiters surrounded by words -> comma
        s = re.sub('(?<=\\s)xx(?=\\s)', 'xxx', s) # xx -> xxx

        # These characters are not allowed in the Main Line.
        s = re.sub(' - ', ' (.) ', s)
        s = re.sub(' / ', ' (.) ', s)

    if s.startswith("%eng"):
        # These characters are not allowed in the English transcription.
        s = re.sub(' - ', ' (.) ', s)
        s = re.sub(' / ', ' (.) ', s)


    if s.startswith("%add"):
        s = re.sub("([A-Z]{3})(,)([A-Z]{3})", "\\1\\2\s\\3", s)

    return s
