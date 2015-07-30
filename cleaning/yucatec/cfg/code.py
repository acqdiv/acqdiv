def clean_filename(fname):
    return fname.rstrip(".txt")

def clean_chat_line(s):

    ### IMPORTANT NOTE: careful with all rules involving "¡", "¿", apostrophe/inverted comma. Check that ordering is correct


    # unification of @Begin and @End lines. -> Commented out since these will be dealt with by the header cleaner.
    '''
    s=re.sub(r"La @Begin", r"@Begin", s)    
    s=re.sub(r"@Begi$", r"@Begin", s)
    s=re.sub(r"@Begin:", r"@Begin", s)
    s=re.sub(r"^Begin", r"@Begin", s)
    s=re.sub(r"@Fin$", r"@End", s)
    s=re.sub(r"^FIN$", r"@End", s)
    s=re.sub(r"@End\.", r"@End", s)
    s=re.sub(r"@End \.", r"@End", s)
    s=re.sub(r"@End:", r"@End", s)
    s=re.sub(r"@End :", r"@End", s)
    s=re.sub(r"@End ", r"@End", s)
    s=re.sub(r"@end\.", r"@End", s)
    s=re.sub(r"@ End", r"@End", s)
    s=re.sub(r"\( FINALIZA \)", r"@End", s)
    s=re.sub(r"\( finaliza \)", r"@End", s)
    '''


    s = re.sub("(^[\*%]\S+\t+[^\t]+)\t", "\1", s)
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
    s=re.sub(r"^\.(.*)", r"\1", s) # remove a dot at the beginning of a line
    s=re.sub(r"<\s*Sandi y Armando\s*>", r"", s)
    s=re.sub(r"^< (.*) >", r"%com:\t\1", s) # place lines with comments in < > into a %com tier
    s=re.sub(r"¡$", r"!", s) # at the end of a line, "¡" has to be "!"
    s=re.sub(r"\-x\-x\-x\-", r"", s)


    ### TIER CLEANING ###
    # At the end existing tiers will be: *XYZ:, %pho:, %xmor:, %spa:, %sit:, %exp:, %com:

    # big tier cleaning done in scripts/edit_yua.py
    s=re.sub(r"\*SEÑ:", r"*UNK:", s)
    s=re.sub(r"@Pía un pollito.", r"%sit:\tPía un pollito.", s)

    s=re.sub(r"^(%pho:)(.*)/(.*)/", r"\1\2\3", s) # remove "/" twice in %pho tiers
    s=re.sub(r"^(%pho:)(.*)/", r"\1\2", s) # remove "/" once in %pho tiers
    s=re.sub(r"^n$", r"", s) # remove lines which have only "n"
    s=re.sub(r"%pho:\t!", r"%pho:\t", s) # remove "!" at the beginning of a %pho tier
    s=re.sub(r"^(.*)\*$", r"\1", s) # remove asterisk at the end of a line
    #s=re.sub(r"^\s+\.$", r"", s) # remove lines which have only " ."
    s=re.sub(r"^\s+\t+\.$", r"", s) # remove lines which have only " ." # the previous rule doesn't work due to the extra white space added at line start.
    #s=re.sub(r"^\n$", r"", s) # remove empty lines # not needed anymore; it is done somewhere else in the cleaning
    s=re.sub(r"(%xmor:)(.*)\\", r"\1\2\|", s) # in %xmor tiers, replace "\" with "|"


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
    
    s=re.sub(r" ", r"á", s) # weird whitespace. Fine to run this rule on all files.
    s=re.sub(r"‚", r"é", s) # specific comma. Fine to run this rule on all files.
    #s=re.sub(r"", r"í", s)
    s=re.sub("¢", "ó", s)
    s=re.sub("£", "ú", s)
    s=re.sub("¤", "ñ", s)

    s=re.sub(r"‡", r"á", s)
    s=re.sub(r"Ž", r"é", s)
    #s=re.sub(r"’", r"í", s) ####### apostrophe/inverted comma involved. Pending.
    s=re.sub(r"—", r"ó", s)
    s=re.sub(r"œ", r"ú", s)
    #s=re.sub(r"–", r"ñ", s) # will be done manually

    s=re.sub(r"ב", r"á", s)
    s=re.sub(r"י", r"é", s) # specific apostrophe. Fine to rule this rule on all files
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

    # dieresis
    s=re.sub(r"^%spa:[\s|\t]+¨(.*)\?", r"%spa:\t¿\1\?", s) # replace a dieresis at the beginning of a %spa tier with "¿"
    s=re.sub(r"^(%pho:[\s|\t]+)¨", r"\1", s) # remove the dieresis at the beginning of a %pho tier
    s=re.sub(r"^(\*[A-Z]{3}:[\s|\t]+)¨", r"\1", s) # remove the dieresis at the beginning of a *PARTICIPANT tier

    # inverted question mark "¿"
    s=re.sub(r"^(\*[A-Z]{3}:)(.*)¿(.*)$", r"\1\2\3", s) # not allowed in a *PARTICIPANT tier
    s=re.sub(r"^(%pho:)(.*)¿(.*)$", r"\1\2\3", s) # not allowed in a %pho tier
    s=re.sub(r"^(%spa:)(.*)¿$", r"\1\2\?", s) # at the end of a %spa tier, "¿" has to be "?"



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


    # The following block is commented out for the moment. As long as chatter doesn't complain, these are not needed.
    '''
    if s.startswith("*"):
        s = re.sub("##", "", s)
        s = re.sub("#", "", s)
        s = re.sub("(\\S)\-(\\S)", "\\1\\2", s) # remove hyphen between non-empty characters
        #s = re.sub("^\\s*\\d+\\s+(?=[\*%])", "", s) # done in edit_yua.py

        # added by rabart
        s = re.sub('\-?0', '', s)
        s = re.sub('(?<=\\w)&(?=[au])', '', s)
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

    return s
