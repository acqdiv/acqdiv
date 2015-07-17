def clean_filename(fname):
    return fname.rstrip(".txt")

def clean_chat_line(s):

    #s = re.sub(":\s+", ":\t", s, 1) #### has to do with syntax having to be: [tier-name]:\t -> update now that all tiers are unified and place in right place

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

    '''
    s = re.sub("(^[\*%]\S+\t+[^\t]+)\t", "\1", s)
    s = re.sub("(\w)['’ʼ]", "\\1ʔ", s)
    s = re.sub("['’ʼ](\w)", "ʔ\\1", s)
    s = re.sub("(\w)['’ʼ](\w)", "\\1ʔ\\2", s)
    '''

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



    ### TIER CLEANING ###
    # At the end existing tiers will be: *XYZ:, %pho:, %mor:, %xspa:, %sit:, %exp:, %com:

    #unification *PARTICIPANT tier
    #correct participants' IDs:
    s=re.sub(r"\*MECH:", r"*MEC:", s)
    s=re.sub(r"\*:MEC:", r"*MEC:", s)    
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
    s=re.sub(r"\*:DAV", r"*DAV:", s)
    s=re.sub(r"\*DAV :", r"*DAV:", s)
    s=re.sub(r"\*DAV", r"*DAV:", s)
    s=re.sub(r"dav:", r"*DAV:", s)
    s=re.sub(r"\*san:", r"*SAN:", s)
    s=re.sub(r"\*fil:", r"*FIL:", s)
    s=re.sub(r"\*fil", r"*FIL:", s)
    s=re.sub(r"fil:", r"*FIL:", s)
    s=re.sub(r"\*FIl:", r"*FIL:", s)
    s=re.sub(r"\*mot::", r"*MOT:", s)
    s=re.sub(r"\*mot:", r"*MOT:", s)
    s=re.sub(r"\*arm:", r"*ARM:", s)
    s=re.sub(r"\* Arm:", r"*ARM:", s)
    s=re.sub(r"\*mar:", r"*MAR:", s)
    s=re.sub(r"\*nef:", r"*NEF:", s)
    s=re.sub(r"\*lor:", r"*LOR:", s)
    s=re.sub(r"\*SEÑ:", r"*UNK:", s)
    s=re.sub(r"\*:", r"*UNK:", s)
    s=re.sub(r"^\s+:\s$", r"*UNK:", s) # replace ":" at the beginning of a line, with some spaces before and after, with *UNK:
    s=re.sub(r"\*\?:", r"*UNK:", s) # replace "*?:" with "*UNK:"
    s=re.sub(r"\(\s+\):", r"*UNK:", s) # replace "(    ):" with "*UNK:"
    s=re.sub(r"xxx:", r"*UNK:", s) # replace "xxx:" with "*UNK:"
    s=re.sub(r"\*XXX:", r"*UNK:", s) # replace "*XXX:" with "*UNK:"
    s=re.sub(r"(\*[A-Z]{3}) :", r"\1:", s) # remove a space between the participant's code and the colon
    s=re.sub(r"\(\s?(\*[A-Z]{3})\s?\):", r"\1:", s) # participant codes with form e.g. "(*ARM):" or "( *SAN ):" should be transformed into "*ARM:"

    #unification %pho tier
    s=re.sub(r"\*pho:", r"%pho:", s)
    s=re.sub(r"%fon:", r"%pho:", s)
    s=re.sub(r"%pho\.", r"%pho:", s)
    s=re.sub(r"%pho :", r"%pho:", s) # note that it is not the usual whitespace
    s=re.sub(r"%pho;", r"%pho:", s)
    s=re.sub(r"^pho:", r"%pho:", s)
    s=re.sub(r"%PHO:", r"%pho:", s)

    #unification %mor tier
    s=re.sub(r"%MOR:", r"%mor:", s)
    s=re.sub(r"\*mor:", r"%mor:", s)
    s=re.sub(r"%mor\.", r"%mor:", s)
    s=re.sub(r"%mor\s+:", r"%mor:", s)
    s=re.sub(r"%mor :", r"%mor:", s) # note that it is not the usual whitespace

    #unification %xspa tier
    s=re.sub(r"\*ESPA:", r"%xspa:", s)
    s=re.sub(r"\*ESP:", r"%xspa:", s)
    s=re.sub(r"\*ESP\.", r"%xspa:", s)
    s=re.sub(r"%ESP:", r"%xspa:", s)
    s=re.sub(r"ESP:", r"%xspa:", s)

    s=re.sub(r"Esp:", r"%xspa:", s)
    s=re.sub(r"Esp\.", r"%xspa:", s)

    s=re.sub(r"%esp\.", r"%xspa:", s)
    s=re.sub(r"%esp_:", r"%xspa:", s)
    s=re.sub(r"%esp :", r"%xspa:", s) # note that it is not the usual whitespace
    s=re.sub(r"%esp:", r"%xspa:", s)
    s=re.sub(r"%\*esp:", r"%xspa:", s)
    s=re.sub(r"\*esp:", r"%xspa:", s)

    s=re.sub(r"%ENG:", r"%xspa:", s)
    s=re.sub(r"%eng:", r"%xspa:", s)
    s=re.sub(r"%eng;", r"%xspa:", s)
    s=re.sub(r"%eng\.", r"%xspa:", s)
    s=re.sub(r"%engL:", r"%xspa:", s)
    s=re.sub(r"%eng :", r"%xspa:", s)
    s=re.sub(r"%eng", r"%xspa:", s)

    # placing uncategorized comments into a %com tier
    s=re.sub(r"^\((.*)\)$", r"%com:\t\1", s) # lines with comments in brackets
    s=re.sub(r"^&", r"%com:\t", s) # lines which start with "&"





    ######some of these should go before the tier name cleaning above. Check
    s=re.sub(r"\s###\s", r" xxx ", s)
    s=re.sub(r"XXX", r"xxx", s)



    s=re.sub(r"^\s+[0-9]+\s+(\*[A-Z]{3}:)", r"\1", s) # remove spaces, numbers and spaces before *PARTICIPANT tiers
    s=re.sub(r"^\s+[0-9]+\s+(%[a-z]{3}:)", r"\1", s) # remove spaces, numbers and spaces before %xxx tiers
    s=re.sub(r"^\s+[0-9]+\s+(%xspa:)", r"\1", s) # remove spaces, numbers and spaces before %xspa tiers
    s=re.sub(r"^\s+(\*[A-Z]{3}:)", r"\1", s) # remove spaces before *PARTICIPANT tiers
    s=re.sub(r"^\s+(%[a-z]{3}:)", r"\1", s) # remove spaces before %xxx tiers
    s=re.sub(r"^\s+(%xspa:)", r"\1", s) # remove spaces before %xspa tiers
    s=re.sub(r"^\t+(\*[A-Z]{3}:)", r"\1", s) # remove tabs before *PARTICIPANT tiers
    s=re.sub(r"^\t+(%[a-z]{3}:)", r"\1", s) # remove tabs before %xxx tiers
    s=re.sub(r"^\t+(%xspa:)", r"\1", s) # remove tabs before %xspa tiers
    s=re.sub(r"^\s+[0-9]+\s+$", r"", s) # remove numbers and/or spaces alone in a line
    s=re.sub(r"^\t+[0-9]+\t+$", r"", s) # remove numbers and/or tabs alone in a line
    #s=re.sub(r"^\s+([%|\*])", r"\1", s) # remove all spaces before the beginning of a tier
    s=re.sub(r"^(%pho:)(.*)/(.*)/", r"\1\2\3", s) # remove "/" twice in %pho tiers
    s=re.sub(r"^(%pho:)(.*)/", r"\1\2", s) # remove "/" once in %pho tiers
    s=re.sub(r"^n$", r"", s) # remove lines which have only "n"


    '''
    s=re.sub(r"^\s+\.$", r"", s) # remove lines which have only " ." ##### careful! this seems to be "content of %mor tiers divided sometimes in two lines". recheck at the end.
    s=re.sub(r"^\n$", r"", s) # remove empty lines ######## recheck! is this correct? See with Andi/Steve/Robert
    s=re.sub(r"^(.*)\*$", r"\1", s) # remove asterisk at the end of a line
    s=re.sub(r"%xpho:\s!", r"%xpho:\s", s) # remove "!" at the beginning of a %xpho tier
    s=re.sub(r"(%pho:\s+)\((.*?)\)(\s+\.)", r"\1\2\3", s) # in %xpho tiers that end in a dot, remove the brackets that surround all the content of the tier
    s=re.sub(r"(%pho:\s+)\((.*?)\)", r"\1\2", s) # in %xpho tiers that don't end in a dot, remove the brackets that surround all the content of the tier
    # there are lines with numbers and an asterisk only, e.g. 020101-DAV: 003 *  ### check lines beginning with numbers
    '''


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
    s=re.sub("ż", "¿", s)
    s=re.sub("Ê", "", s)
    s=re.sub("hńn", "hnn", s) ########## recheck. Also "hn´n" was found. Maybe there is something else there... Also look for hm@i, and for @ alone... It looks like the pattern is @i or @in or @ia. Check. And when there is this in a *PARTICIPANT tier, then there are no other tiers following. There is also hn'n in *XYZ (and right below, in %pho, it was written as hn’h). Check. Check CHAT manual, @i/@in... seems to have a meaning...
    s=re.sub("ń", "ñ", s)
    s=re.sub(r"(%xmor:)(.*)\\", r"\1\2\|", s) # in %xmor tiers, replace "\" with "|"

    # dieresis
    s=re.sub(r"^%xspa:[\s|\t]+¨(.*)\?", r"%xspa:\t¿\1\?", s) # replace a dieresis at the beginning of a %xspa tier with a "¿"
    s=re.sub(r"^(%xpho:[\s|\t]+)¨", r"\1", s) # remove the dieresis at the beginning of a %xpho tier
    s=re.sub(r"^(\*[A-Z]{3}:[\s|\t]+)¨", r"\1", s) # remove the dieresis at the beginning of a *PARTICIPANT tier
    #s=re.sub(r"", r"", s) ######### What about a dieresis in %mor tiers?

    # inverted question mark
    s=re.sub(r"^\*([A-Z]{3}:)(.*)¿(.*)$", r"*\1\2\3", s) # not allowed in a *PARTICIPANT tier
    s=re.sub(r"^%xpho:(.*)¿(.*)$", r"%xpho:\1\2", s) # not allowed in a %xpho tier
    s=re.sub(r"^%xspa:(.*)¿$", r"%xspa:\1\?", s) # at the end of a %xspa tier, "¿" has to be "?"





    '''
    s = re.sub("\\s‘\\s", "?", s) # other uses of "‘" need manual attention
    s = re.sub("^.+?\\\\.+?$", "", s) # backslashes only occur in lines of jumbled characters (probably information lost from .doc to .txt) ##### Not there anymore. grep backslash. -> all the lines in capital letters LOWER, MERGEFORMAT, usw. have to go away too. Check
    s = re.sub("ï", "'", s)
    '''


    #inverted exclamation mark (work in progress...)
    s=re.sub(r"¡$", r"!", s) # at the end of a line, "¡" has to be "!"
    s=re.sub("all¡", "allí", s) # these four refer to consistent errors across the corpus and they simplify the application of other rules below.
    s=re.sub("as¡", "así", s)
    s=re.sub("aqu¡", "aquí", s)
    s=re.sub("ah¡", "ahí", s)
    s=re.sub("m¡ralo", "míralo", s)
    s=re.sub("ma¡z", "maíz", s)
    s=re.sub("m¡o", "mío", s)
    s=re.sub("j¡cara", "jícara", s)
    s=re.sub("todav¡a", "todavía", s)
    s=re.sub("sand¡a", "sandía", s) ########## only two instances. Move to manual changes... ?
    #s=re.sub(r"^\*([A-Z]{3}:)(.*)¡(.*)$", r"*\1\2\3", s) # not allowed in a *PARTICIPANT tier

    ### OTHER CLEANING ###
    s=re.sub("ERg", "ERG", s)
    s=re.sub(r"mçuu", r"múu", s)
    s=re.sub(r"dçomde", r"dónde", s)
    s=re.sub("ç", "", s)
    s=re.sub("quë", "qué", s)
    s=re.sub(r"\-x\-x\-x\-", r"", s) ##### this one has to go before the one that deletes the empty tiers.






    '''
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
        s = re.sub("(\\S)\-(\\S)", "\\1\\2", s) # remove hyphen between non-empty characters
        s = re.sub("^\\s*\\d+\\s+(?=[\*%])", "", s)

        # added by rabart
        s = re.sub('\-?0', '', s)
        s = re.sub('(?<=\\w)&(?=[au])', '', s)

    if s.startswith("%eng"):
        s = re.sub("\[\\s*", "", s) # remove [ from %eng tiers... ------> ? check.
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
    '''

    return s
