def clean_filename(fname): 
    fname = fname.lower()
    fname = fname.replace(" first 30 minutes", "")
    fname = fname.replace(" first 35 minutes", "")
    fname = fname.replace("cansu36_ 20feb04_02-03-26", "")
    fname = fname.replace("ogun31-05july503_02-05-01", "")
    fname = fname.replace(";", "-")
    fname = fname.rstrip(".cha")
    return fname

def clean_chat_line(s):
    s = re.sub("^@New Episode:$", "@New Episode", s)
    s = re.sub("^@Participants\\s+", "@Participants:\\t", s)
    s = re.sub("^%act\\s+","%act:\\t", s)
    s = re.sub("^@Age of CHI$", "@Age of CHI:", s)
    s = re.sub("^@Coder$", "@Coder:", s)
    s = re.sub("^@Date$", "@Date:", s)
    s = re.sub("^@Education of MOT$", "@Education of MOT:", s)
    s = re.sub("^@ID$", "@ID:", s)
    s = re.sub("^@Media$", "@Media:", s)
    s = re.sub("^@Recorder$", "@Recorder:", s)
    s = re.sub("^@Transcriber$", "@Transcriber:", s)
    s = re.sub("^\\*MOT$", "", s)
    s = re.sub("^@Child: Tuğçe$", "", s)
    s = re.sub("^@Sex of CHI$", "@Sex of CHI:", s)
    s = re.sub("^@SEX of CHI$", "@SEX of CHI:", s)
    s = re.sub("^@SES of MOT$","@SES of MOT:", s)
    s = re.sub("^@Mother, FAT Father$", "", s)
    # replace <:> space with \t in first occurrence
    s = re.sub(":\\s*", ":\\t", s, 1)
    
    # added by rabart
    s = re.sub("^%mor:", "%xmor:", s)

    

    # get rid of empty headers
    s = re.sub("^@.*:\\s*$", "", s)
    
    s = re.sub("^%pho:", "%tim:", s)
    s = re.sub(r"(\*[A-Z]{1,3}\d{0,2}:)\s*(\d{1,2}:\d\d)", r"\1\txxx .\n%tim:\t\2", s)
    s = re.sub(r'.%snd:".+?"_(\d)_(\d+)(\d\d\d+).', r'\n%tim:\t\1-\2.\3', s)
    s = re.sub(r'.%snd:".+?"_(\d+)(\d\d\d)_(\d+)(\d\d\d+).', r'\n%tim:\t\1.\2-\3.\4', s)
    s = re.sub(r"%tim:\s(\d:\d\d)", r"%tim:\t0\1", s) # prefixes 0 to > 10 min
    s = re.sub("^%acT:", "%act:", s)
    s = re.sub("^%atc:", "%act:", s)
    s = re.sub("^%EXP:", "%exp:", s)
    s = re.sub("\\byy\\b", "yyy", s)
    s = re.sub("\\bxx\\b", "xxx", s)
    s = re.sub(":\\t\[!", ":\\t0 [!", s) 
    s = re.sub(r"\n\n", r"\n", s) # gets rid of empty lines
    s = re.sub(r"\n\s+", r" ", s) # gets rid of line breaks in utterance; IMPORTANT: this must go before the following replacement, otherwise %add is inserted into the middle of utterances.
    s = re.sub(r"(\*[A-Z]{3})-([A-Z]{3})(:.+)", r"\1\3\n%add:\t\2", s) # puts addressee into separate dependent tier (%add), instead of in the format speaker-addressee (SSS-AAA).
    s = re.sub(r"(\*[A-Z]{2}\d)-([A-Z]{2}\d)(:.+)", r"\1\3\n%add:\t\2", s) # puts addressee into separate dependent tier (%add), instead of in the format speaker-addressee (SS\d-AA\d).
    s = re.sub(r"(\*[A-Z]{3})-([A-Z]{2}\d)(:.+)", r"\1\3\n%add:\t\2", s) # puts addressee into separate dependent tier (%add), instead of in the format speaker-addressee (SSS-AA\d).
    s = re.sub(r"(\*[A-Z]{2}\d)-([A-Z]{3})(:.+)", r"\1\3\n%add:\t\2", s) # puts addressee into separate dependent tier (%add), instead of in the format speaker-addressee (SS\d-AAA).
    s = re.sub(r"(\[x)(\d\])", r"\1 \2", s) # fixes repetitions
    s = re.sub(r"&=\s+", "&=", s)
    s = re.sub(r"\+''", r'+"', s)
    s = re.sub(r"\[\s+=", r"[=", s)
    s = re.sub(r"\[!", r"[=!", s)
    s = re.sub(r"(@New Episode):\s(.+$)", r"\1\n%sit:\t\2", s)
    s = re.sub(r"#", r"(.)", s) # hashtag is equivalent to (.) which is CHAT for notation for pauses.
    s = re.sub(r"\[[X\*]\s?(\d)\]", r"[x \1]", s)
    # many uses of "@" (plus following code) are inconsistent and are not CHAT compliant. cf. issue #86
    s = re.sub(r"(@fp|@e|@s|@oın|@İ|@lsi|@i_ham@i_ham|@oı|@s|@ı|@fmı|@fi|@s|@i_ham@i_ha:m|@omı|@oa|@ia|@fmi|@cmı|@y|@r|@oını|@l'in|@imi|@i_ham@i_ham@i_ham@i_ham@i_ham|@fb|@eng|@eın|@oe|@m|@lyi|@imı|@ie|@:i|@fyı|@fnı|@fa|@en|@eler|@e|@sit|@si_kızını|@oü|@o_şupur|@omu|@olatmadık|@lidi|@is|@iksin|@i_hey@i_hey|@i_ham@i_ham@i_ham@i_ham@i_ham@i_ham|@i_ham@i_ham@i_ham@i_ham|@i_ham@i_ham@i_ham|@i_ham@i_ham|@i_ham@i_ha:m_ham@i_ham@i_ha:m|@ie|@i_benim_kuzum|@ì|@fmu|@fler|@elerde|@e_bye@e|@cnın|@c:e|@yu|@verme|@tıtı|@swi|@S-QUE|@simu|@si_kıvrıla|@se|@ş|@o'yi|@ou|@o_şıkır@o_şıkır|@o_miyav|@olerle|@olatmadık|@oların|@oları|@olar|@ola|@o_kırt@o_kırt@o_kırt@o_kırt|@o_kırt@o_kırt|@o_kırt|@oına|@oımız|@o_huppur|@o&hav|@o\[/\]hav|@o_havmı|@o_ham@o_ham@o_ham|@o_fırıl|@odan|@o_cuf@o_cuf|@ob|@ö|@mı|@lylen|@lsi|@l\^si|@lni|@kurmasınlar|@köpek|@kızım|@i_uf|@i_tu|@ir|@int|@inmi|@inı|@i_ne_güzel|@imuş|@im|@iktim|@iktim|@ikmisin|@ikmisin|@ii\(y\)im|@iives|@i_ı@i_ı@i_ı|@i_ı@i_ı|@i_ı|@iıhı|@i_ıh|@i@ie|@iı|@ii|@ihıhı|@i_hıh|@ihıha|@i_hı|@ihı|@,ıh|@i_ham@i_ham@i_ham@i_ham@i_ham@i_ham@i_ham|@i_ham@i_ham@i_ham@i_ha:m_ham@i_ham@i_ham@i_ham@i_ha:m|@i_ham@i_ham@i_ham@i_ha:m|@i_ham@i_ham@i_ham@i_ha|@i_ham|@iğinmi|@iee|@iee|@iee|@ie|@i_benim_yy_bunu_ben_yapalım|@iama|@hav|@ha|@h|@fyü|@fylamı|@fyi|@f_yapıyo\(r|@fya|@ftan|@fsını|@fsini|@fsı|@f_oldu|@foldu|@fo|@fnin|@fmü|@flara|@fı|@f_ham|@fbıdı|@eye|@:e's|@erın|@en|@emi|@eların|@elar|@ede|@ea|@ea|@e|@e|@dı|@da|@cuna|@cü|@cmi|@clarmı|@c_kut:u|@c_by:e@e|@c_adamalar|@bur\(a\)da|@b=&laugh|@bi|@b_ga|@bak|@babbab|@ba|@\[b26\]i|@ai|@0)", r"", s)
    s = re.sub(r"@(\W+)", r"\1", s) #gets rid of "@" at the end of words
    s = re.sub(r'<(.+?)>\s\["\]', r"'\1'", s)
    s = re.sub(r'(\S+)\s\["\]', r"'\1'", s)
    s = re.sub(r'\+/([^/])', r'+//\1', s) # check CHAT manual, this might be a dirty fix for legitimate CHAT with an utterance delimiter missing
    s = re.sub(r"\+//\s\.", r"+//.", s)
    s = re.sub(r"\+//\n", r"+//.\n", s)
    s = re.sub(r"\[:\s(\w)", r"[: \1", s)
    s = re.sub(r"\[\s?(\w+)\]", r"[: \1]", s)
    
    
        
    """
    s = re.sub("(^[A-Z]{3}\-[A-Z]{3}:)", r"*\1", s) # MOM-CHI:
    s = re.sub("(^\*[A-Z]{3})(-)(:)", r"\1\3", s) # *MOT-:
    s = re.sub("(^\*[A-Z]{3})(.)(:)", r"\1\3", s) # *MOT-:
    s = re.sub("(^\*[A-Z]{3}\-[A-Z]{3})(\s+)(:)", r"\1\3", s) # *MOT-MOM :
    s = re.sub("(^\*[A-Z]{3})(\-)(\s+)([A-Z]{3}:)", r"\1\2\4", s) # *MOT- NEI:
    s = re.sub("(^\*[A-Z]{3})(\s+)(\-)([A-Z]{3}:)", r"\1\3\4", s) # *CHI -MOT:
    s = re.sub("(^\*MM)(\-)([A-Z]{3}:)", r"*MOM\2\3", s) # *MM-CHI:
    s = re.sub("(^\*[A-Z]{3}\-[A-Z]{3})(\.)", r"\1:", s) # *NEI-MOM.
    s = re.sub("\*CHI.\s*", "\*CHI:\t", s)  
    """
    
    #character replacements
    s = re.sub("þ", "ş", s)
    s = re.sub("ð", "ğ", s)
    s = re.sub("", "]", s)
    s = re.sub("", "[", s)
    s = re.sub("’", "'", s)
    s = re.sub("", "#", s)
    s = re.sub("\\}", "]", s)
    s = re.sub("×", "x", s)
    s = re.sub("…", "...", s)
    s = re.sub("⧣", "#", s)
    s = re.sub("Þ", "Ş", s)
    s = re.sub("\\{", "[", s)
    s = re.sub("д", "d", s)
    s = re.sub("а", "a", s) # Cyrillic a vs Latin a (has been done manually, but put here in case new Turkish files appear)
    s = re.sub("‘", "'", s) # has been done manually, but put here in case new Turkish files appear
    s = re.sub('”', '"', s)
    s = re.sub('“', '"', s)
    s = re.sub("Ð", "Ğ", s) # has been done manually, but put here in case new Turkish files appear
    s = re.sub("®", "r", s) # has been done manually, but put here in case new Turkish files appear
    s = re.sub("ƒ", "f", s) # has been done manually, but put here in case new Turkish files appear
    s = re.sub("", "(", s) # has been done manually, but put here in case new Turkish files appear
    s = re.sub("≥", ">", s) # has been done manually, but put here in case new Turkish files appear
    s = re.sub("\\\\", "", s)
    s = re.sub("`", "'", s)
    s = re.sub("å", "a", s)

    
    
    # fix roles according the CHILDES's depfile.cut 
    # line = line.replace("Target_Chıld", "Target\_Child")
    # participants have to be fixed
    # @ID has to be fixed
    #  @ID:Burcu-may23-2002 -> 
    # @Age of CHI (not declared in .cha format)
    # transcriber tiers are empty
    #  @Media:burcu-may23-2002 -> add "audio video"
    # @activities -> not in depfile.cut
    # KULLD using MOT & MOM interchangeably
    # "xx" not allowed
    # brackets not allowed
    # utterance delimiter always needed (e.g. ".")

    return s
