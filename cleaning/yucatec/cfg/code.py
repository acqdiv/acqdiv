def clean_filename(fname):
    return fname.rstrip(".txt")

def clean_chat_line(s):

    ### IMPORTANT NOTE: careful with all rules involving "¡", "¿", apostrophe/inverted comma. Check that ordering is correct

    #s = re.sub("(^[\*%]\S+\t+[^\t]+)\t", "\1", s)
    s = re.sub("(\w)['’ʼ]", "\\1ʔ", s)
    s = re.sub("['’ʼ](\w)", "ʔ\\1", s)
    s = re.sub("(\w)['’ʼ](\w)", "\\1ʔ\\2", s)


    #This may result in files with two Situation tiers. These will have to be cleaned manually before CLAN will accept them!
    '''
    s = re.sub("^@Activities", "@Situation", s)
    s = re.sub("^@Birth of ARM:.*", "@Birth of ARM:\t1994-APR-10\n", s)
    s = re.sub("^@Birth of DAV:.*", "@Birth of DAV:\t1998-APR-18\n", s)
    s = re.sub("^@Birth of Sandi:.*", "@Birth of SAN:\t1993-JUL-23\n", s)
    # this three above... search for cases...
    s = re.sub("^@Translation", "@Translator", s)
    '''


    ### LINE CLEANING ###
    s=re.sub(r"^\.\s*([\*%])", r"\1", s) # remove a dot and/or spaces at the beginning of a line


    if s.startswith("%xpho"):
         s=re.sub(r"\-", r"", s) # remove "-" in %pho tiers
         s=re.sub(r"\.", r"", s) # remove dots in %pho tiers
         s=re.sub(r"\/", r"", s) # remove "/" in %pho tiers
         #s=re.sub(r" $\n", r"\n", s) # remove whitespaces at the end of %pho tiers
         s=re.sub(r"\s[\.\?\!;,]+\s*$\n", r"\n", s) # remove dot/ending mark in %pho tiers
         s=re.sub(r" ", r"", s) # remove weird whitespaces in %pho tiers

    if s.startswith("*"):
         s=re.sub(r"/", r"", s) # remove "/" in *PARTICIPANT tiers
         s=re.sub(r"\+", r" ", s)
         s=re.sub(r"(\*[A-Z]{3}:\t)$\n", r"\1.\n", s) # add a dot at the end of empty *PARTICIPANT tiers
         #s=re.sub(r"[^\(]\.\.\.[^\)]", r" (...) ", s)
         #s=re.sub(r"\S\.\.\.\S", r" (...) ", s)
         s=re.sub(r"([A-Z a-z])\.\.\.([A-Z a-z])", r"\1 (...) \2", s)
         s=re.sub(r"¿", r"", s) # remove "¿" in *PARTICIPANT tiers
         s=re.sub(r"¡", r"", s) # remove "¡" in *PARTICIPANT tiers
         #s=re.sub(r"\.(.+)", r"", s) # no dots allowed in *PARTICIPANT tiers; replacing them by a comma

    if s.startswith("%spa"):
         s=re.sub(r"¿", r"", s) # remove "¿" in %spa tiers



    ### TIER CLEANING ###
    # At the end existing tiers will be: *XYZ:, %xpho:, %xmor:, %spa:, %sit:, %exp:, %com:, %cod:

    # Big line and tier cleaning done in acqdiv/scripts/yucatec/edit_yua.py

    s=re.sub(r"\*SEÑ:", r"*UNK:", s)
    s=re.sub(r"@Pía un pollito.", r"%sit:\tPía un pollito.", s)
    s=re.sub(r"@Nefi burla a Aamando.", r"%sit:\tNeifi burla a Armando.", s)

    s=re.sub(r"(\*[A-Z]{3}:)(.*?)\t$", r"\1\2", s) # remove tabs at the end of *PARTICIPANT tiers
    s=re.sub(r"(%[a-z]{3,4}:)(.*?)\t$", r"\1\2", s) # remove tabs at the end of %xxx(x) tiers

    if s.endswith((" ")):
         s=re.sub(r" $\n", r"\n", s) # remove whitespaces at the end of lines


    # all tier names must be followed by a tab before the tier content starts (this block has to be in both edit_yua.py and code.py)
    #s=re.sub(r"(%[a-z]{3,4}:)\s*(.*?)$", r"\1\t\2\n", s)
    #s=re.sub(r"(\*[A-Z]{3}:)\s*(.*?)$", r"\1\t\2", s)
    #s=re.sub(r"(%[a-z]{3,4}:)\s*(.*?)$", r"\1\t\2", s)
    s=re.sub(r"(\*[A-Z]{3}:)\s*$", r"\1\t\n", s)
    s=re.sub(r"(%[a-z]{3,4}:)\s*$", r"\1\t\n", s)
    #s=re.sub(r"(\*[A-Z]{3}:)([A-Za-z]+)", r"\1\t\2", s)
    #s=re.sub(r"(%[a-z]{3,4}:)([A-Za-z]+)", r"\1\t\2", s)
    s=re.sub(r"(\*[A-Z]{3}:) *\t* *([A-Za-záéíóú\[\(¡\?]+)", r"\1\t\2", s)
    s=re.sub(r"(%[a-z]{3,4}:) *\t* *([A-Za-záéíóú\[\(¡\?]+)", r"\1\t\2", s)
    #s=re.sub(r"(\*[A-Z]{3}:) *([A-Za-z\[\(¡]*)", r"\1\t\2", s)
    #s=re.sub(r"(%[a-z]{3,4}:) *([A-Za-z\[\(¡])", r"\1\t\2", s)
    s=re.sub(r"(\*[A-Z]{3}:)\s*\n", r"\1\t\n", s)
    s=re.sub(r"(%[a-z]{3,4}:)\s*\n", r"\1\t\n", s)
    s=re.sub(r"(\*[A-Z]{3}:)\t\t([A-Za-z\[\(¡\?]+)", r"\1\t\2", s)
    s=re.sub(r"(\*[A-Z]{3}:) *\.$", r"\1\t.", s)
    s=re.sub(r"(%[a-z]{3,4}:) *\.$", r"\1\t.", s)


    #s=re.sub(r"(%xmor:\t)$\n", r"\1.\n", s) # add a dot at the end of an empty %xmor tier without terminator
    s=re.sub(r"^%xmor:\t\s*$", r"", s) # remove empty %xmor tiers
    s=re.sub(r"^%xpho:\t\s*$", r"", s) # remove empty %xpho tiers
    s=re.sub(r"^%spa:\t\s*$", r"", s) # remove empty %spa tiers

    s=re.sub(r"^([\*%])(.*?),$", r"\1\2.", s) # replace a comma at the end of a line with a dot
    s=re.sub(r"(%spa)(.*?)([^\.\!\?])$", r"\1\2\3.", s) # add a dot at the end of %spa tiers when there is no proper terminator
    s=re.sub(r"(\*[A-Z]{3})(.*?)([^\.\!\?])$", r"\1\2\3.", s) # add a dot at the end of *PARTICIPANT tiers when there is no proper terminator
    s=re.sub(r"(%xmor:\t)(.*?)\t", r"\1\2 ", s) # replace a tab in the content of an %xmor tier with a space

    #s=re.sub(r"@End", r"@End\n", s) # add a newline after @End



    ### CHARACTER CLEANING ###
    # cf. ../notes/yua-chars.ods for notes on characters that need manual attention and/or need to be interpreted by Barbara (corpus owner)
    
    s=re.sub(r"α", r"á", s)
    s=re.sub(r"ι", r"é", s)
    s=re.sub(r"ν", r"í", s)
    s=re.sub(r"σ", r"ó", s)
    s=re.sub(r"ϊ", r"ú", s)
    s=re.sub(r"ρ", r"ñ", s)
    s=re.sub(r"Ώ", r"¿", s)
    #s=re.sub(r"‘", r"¡", s) ####### apostrophe/inverted comma involved. Pending.

    s=re.sub(r"б", r"á", s)
    s=re.sub(r"й", r"é", s)
    s=re.sub(r"н", r"í", s)
    s=re.sub(r"у", r"ó", s)
    s=re.sub(r"ъ", r"ú", s)
    s=re.sub(r"с", r"ñ", s)

    s=re.sub(r"está ", r"está", s) # remove weird whitespace after "está"
    s=re.sub(r" ", r"á", s) # weird whitespace. Fine to run this rule on all files at this position (careful with all rules involving weird whitespace!! order very important!).
    s=re.sub(r"‚", r"é", s) # specific comma. Fine to run this rule on all files.
    #s=re.sub(r"¡", r"í", s) # to be done manually
    s=re.sub("¢", "ó", s)
    s=re.sub("£", "ú", s)
    s=re.sub("¤", "ñ", s)

    s=re.sub(r"‡", r"á", s)
    s=re.sub(r"Ž", r"é", s)
    #s=re.sub(r"’", r"í", s) ####### apostrophe/inverted comma involved. Pending.
    s=re.sub(r"—", r"ó", s)
    s=re.sub(r"œ", r"ú", s)
    #s=re.sub(r"–", r"ñ", s) # to be done manually

    s=re.sub(r"ב", r"á", s)
    s=re.sub(r"י", r"é", s) # specific apostrophe. Fine to rule this rule on all files.
    s=re.sub(r"ם", r"í", s)
    s=re.sub(r"ף", r"ó", s)
    s=re.sub(r"ת", r"ú", s)
    s=re.sub(r"ס", r"ñ", s)

    s=re.sub("pochĄech", "pochkech", s) #### confirm with Barbara?
    s=re.sub("Ą", "¡", s)
    s=re.sub("Æ", "'", s)
    s=re.sub("sÏ", "sí", s)
    s=re.sub("à", "á", s)
    s=re.sub("è", "é", s)
    s=re.sub("ì", "í", s)
    s = re.sub("ï", "'", s)
    s=re.sub("ż", "¿", s)
    s=re.sub("Ê", "", s)
    s=re.sub("hńn", "hnn", s) #
    s=re.sub("dińo", "dino", s)
    s=re.sub("ń", "ñ", s)
    s=re.sub("ò", "ó", s)

    # dieresis
    s=re.sub(r"^(%spa:\t+)¨(.*)\?", r"\1\2?", s) # remove the dieresis at the beginning of a %spa tier
    s=re.sub(r"^(%xpho:\t+)¨", r"\1", s) # remove the dieresis at the beginning of a %pho tier
    s=re.sub(r"^(\*[A-Z]{3}:\t+)¨", r"\1", s) # remove the dieresis at the beginning of a *PARTICIPANT tier

    # inverted question mark "¿"
    s=re.sub(r"^(\*[A-Z]{3}:)(.*)¿(.*)$", r"\1\2\3", s) # not allowed in a *PARTICIPANT tier
    s=re.sub(r"^(%xpho:\t)(.*)¿(.*)$", r"\1\2\3", s) # not allowed in a %pho tier
    s=re.sub(r"^(%spa:\t)(.*)¿$", r"\1\2\?", s) # at the end of a %spa tier, "¿" has to be "?"

    s=re.sub(r"¿", r"", s) # "¿" not allowed anywhere


    '''
    s = re.sub("\\s‘\\s", "?", s) # other uses of "‘" need manual attention
    s = re.sub("^.+?\\\\.+?$", "", s) # backslashes only occur in lines of jumbled characters (probably information lost from .doc to .txt) ##### Not there anymore. grep backslash. -> all the lines in capital letters LOWER, MERGEFORMAT, usw. have to go away too. Check
    '''


    #inverted exclamation mark
    s=re.sub("all¡", "allí", s) # these four refer to consistent errors across the corpus and they simplify the application of other rules below.
    s=re.sub("as¡", "así", s)
    s=re.sub("aqu¡", "aquí", s)
    s=re.sub("ah¡", "ahí", s)
    s=re.sub("m¡ralo", "míralo", s)
    s=re.sub("ma¡z", "maíz", s)
    s=re.sub("m¡o", "mío", s)
    s=re.sub("j¡cara", "jícara", s)
    s=re.sub("todav¡a", "todavía", s)
    s=re.sub("sand¡a", "sandía", s)
    #s=re.sub(r"^\*([A-Z]{3}:)(.*)¡(.*)$", r"*\1\2\3", s) # not allowed in a *PARTICIPANT tier


    ### OTHER CLEANING ###
    s=re.sub("ERg", "ERG", s)
    s=re.sub(r"mçuu", r"múu", s)
    s=re.sub(r"dçomde", r"dónde", s)
    s=re.sub("ç", "", s)
    s=re.sub("quë", "qué", s)
    s=re.sub("Cárga,e", "Cárgame", s)
    s=re.sub("laìz", "lápiz", s)


    #cleanup unwanted tiers -> Commented out. Done somewhere else in the cleaning
    #added by chysi
    '''
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
    '''


    if s.startswith("*"):
        s=re.sub("##", "", s)
        s=re.sub("#", "", s)
        #s = re.sub("(\\S)\-(\\S)", "\\1\\2", s) # remove hyphen between non-empty characters

        # added by rabart
        #s = re.sub('\-?0', '', s)
        #s = re.sub('(?<=\\w)&(?=[au])', '', s)

    if s.startswith("%xpho"):
        s=s.lower() # no capital letters allowed in %pho tiers

    '''
    # all tier names must be followed by a tab before the tier content starts (this block has to be in both edit_yua.py and code.py)
    #s=re.sub(r"(%[a-z]{3,4}:)\s*(.*?)$", r"\1\t\2\n", s)
    #s=re.sub(r"(\*[A-Z]{3}:)\s*(.*?)$", r"\1\t\2", s)
    #s=re.sub(r"(%[a-z]{3,4}:)\s*(.*?)$", r"\1\t\2", s)
    s=re.sub(r"(\*[A-Z]{3}:)\s*$", r"\1\t\n", s)
    s=re.sub(r"(%[a-z]{3,4}:)\s*$", r"\1\t\n", s)
    #s=re.sub(r"(\*[A-Z]{3}:)([A-Za-z]+)", r"\1\t\2", s)
    #s=re.sub(r"(%[a-z]{3,4}:)([A-Za-z]+)", r"\1\t\2", s)
    s=re.sub(r"(\*[A-Z]{3}:) *\t* *([A-Za-z\[\(¡\?]+)", r"\1\t\2", s)
    s=re.sub(r"(%[a-z]{3,4}:) *\t* *([A-Za-z\[\(¡\?]+)", r"\1\t\2", s)
    #s=re.sub(r"(\*[A-Z]{3}:) *([A-Za-z\[\(¡]*)", r"\1\t\2", s)
    #s=re.sub(r"(%[a-z]{3,4}:) *([A-Za-z\[\(¡])", r"\1\t\2", s)
    s=re.sub(r"(\*[A-Z]{3}:)\s*\n", r"\1\t\n", s)
    s=re.sub(r"(%[a-z]{3,4}:)\s*\n", r"\1\t\n", s)
    s=re.sub(r"(\*[A-Z]{3}:)\t\t([A-Za-z\[\(¡\?]+)", r"\1\t\2", s)
    '''



    # The following block is commented out for the moment, as these characters seem to be allowed, and have a meaning.
    '''
    if s.startswith("%eng"):
        s = re.sub("\[\\s*", "", s) # remove "[" from %spa tiers
        s = re.sub("\\s*\]", "", s) # remove "]" from %spa tiers
        # added by rabart
        s = re.sub('[\(\)]\\s*', '', s) # delete brackets and following spaces
        s = re.sub('%eng:\\s+', '%eng:\\t', s) # replace any spaces left by tab
    '''

    if s.startswith("*"):
        s=re.sub(r"(\(\.\.\.\))$", r"\1.", s) # add a dot at the end of *PARTICIPANT tiers ending in "(...)"


    return s
