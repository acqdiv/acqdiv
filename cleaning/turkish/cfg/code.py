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
    s = re.sub("^@Participants\s+", "@Participants:\t", s)
    s = re.sub("^%act\s+","%act:\t", s)
    s = re.sub("^@Age of CHI$", "@Age of CHI:", s)
    s = re.sub("^@Coder$", "@Coder:", s)
    s = re.sub("^@Date$", "@Date:", s)
    s = re.sub("^@Education of MOT$", "@Education of MOT:", s)
    s = re.sub("^@ID$", "@ID:", s)
    s = re.sub("^@Media$", "@Media:", s)
    s = re.sub("^@Recorder$", "@Recorder:", s)
    s = re.sub("^@Transcriber$", "@Transcriber:", s)
    s = re.sub("^\*MOT$", "", s)
    s = re.sub("^@Child: Tuğçe$", "", s)
    s = re.sub("^@Sex of CHI$", "@Sex of CHI:", s)
    s = re.sub("^@SEX of CHI$", "@SEX of CHI:", s)
    s = re.sub("^@SES of MOT$","@SES of MOT:", s)
    s = re.sub("^@Mother, FAT Father$", "", s)
    # replace <:> space with \t in first occurrence
    s = re.sub(":\s*", ":\t", s, 1)
    
    # get rid of empty headers
    s = re.sub("^@.*:\t*$", "", s)

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
    s = re.sub("^%pho:", "%tim:", s)
    s = re.sub("(\b)yy(\b)", "$1yyy$2", s)
    s = re.sub("(\b)xx(\b)", "$1xxx$2", s)
    s = re.sub(":\t[!", ":\t0 [!", s)
    
    """

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
