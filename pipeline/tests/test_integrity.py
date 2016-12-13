import configparser
from nose.tools import assert_equal, assert_not_equal, assert_in, assert_not_in, assert_true, assert_false
import re
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import time


session = None

def setup():
    global cfg, session
    engine = sa.create_engine('sqlite:///test.sqlite3')
    meta = sa.MetaData(engine, reflect=True)
    Session = sessionmaker(bind=engine)
    session = Session()


def test_database_integrity():
    # Note: SQL "NULL" returns as Python None

    # check proportion of NULLs per corpus.column, fail if below threshold value. There are three cases: 
    # (1) column must contain at least one non-NULL, threshold = 1
    # (2) column mustn't contain a single NULL, threshold = lowest possible number > 0
    # (3) column mustn't contain more NULLs than some other threshold value
    mini = 1/8500000 # this is the lowest possible number > 0, based on the number of rows in our largest table (words with 8,467,107 rows)
    
    for check in (("morphemes","gloss",1),
        ("morphemes","gloss_raw",1),
        ("morphemes","morpheme",1),
        ("morphemes","pos",1),
        ("morphemes","pos_raw",1),
        ("sessions","date",mini),
        ("speakers","age",1),
        ("speakers","age_in_days",1),
        ("speakers","age_raw",1),
        ("speakers","gender",1),
        ("speakers","gender_raw",1),
        ("speakers","macrorole",0.15),
        ("speakers","macrorole",mini),
        ("speakers","name",1),
        ("speakers","role",1),
        ("speakers","role_raw",1),
        ("speakers","speaker_label",mini),
        ("uniquespeakers","corpus",mini),
        ("uniquespeakers","speaker_label",mini),
        ("utterances","gloss_raw",1),
        ("utterances","morpheme",1),
        ("utterances","pos_raw",1),
        ("utterances","speaker_label",0.15),
        ("utterances","translation",1),
        ("utterances","utterance",0.15),
        ("utterances","utterance_raw",0.15),
        ("words","pos",1),
        ("words","word",0.15)):
        table = check[0]
        column = check[1]
        threshold = check[2]
        for corpus in ("Chintang", "Cree", "Indonesian", "Inuktitut", "Japanese_Miyata", "Japanese_MiiPro", "Russian", "Sesotho", "Turkish", "Yucatec"):
            # corpus-specific exceptions
            if not ((corpus in ("Japanese_Miyata","Sesotho","Yucatec") and column == "gender_raw") # these corpora never indicates gender in the source metadata, it can only be inferred
                or (corpus == "Indonesian" and column == "pos_raw") # Indonesian doesn't have POS tags
                or (corpus in ("Japanese_Miyata","Japanese_MiiPro","Russian","Turkish") and column == "translation") # not a single translated utterance in these corpora
                ):
                yield check_proportion_null, corpus, table, column, threshold
    
    # compare word_actual and word_target
    for corpus in ('Chintang', 'Cree', 'Indonesian', 'Inuktitut', 'Japanese_Miyata', 'Japanese_MiiPro', 'Russian', 'Sesotho', 'Turkish', 'Yucatec'):
        yield check_words_actual_target, corpus

    # check various standardized value sets
    # TODO: https://github.com/uzling/acqdiv/issues/351
    # XXX, XX1, etc., and AUX create NULL
    # query = "select count(*) from speakers where name is null"
    # yield check_any_null, query
    
    table = "utterances"
    column = "sentence_type"
    values = [None, "default", "question", "exclamation", "imperative", "action", "trail off", "interruption", "trail off question", "self interruption", "quotation precedes", "interruption question"]
    permission = "allow"
    yield check_values, table, column, values, permission

    table = "morphemes"
    column = "pos"
    values = [None, "ADJ", "ADV", "ART", "AUX", "CLF", "CONJ", "IDEOPH", "INTJ", "N", "NUM", "pfx", "POST", "PREP", "PRODEM", "PTCL", "QUANT", "sfx", "stem", "V", "???"]
    permission = "allow"
    yield check_values, table, column, values, permission

    table = "speakers"
    column = "gender"
    values = ["Female", "Male", "None"]
    permission = "allow"
    yield check_values, table, column, values, permission
    
    table = "speakers"
    column = "role"
    values = ["Adult", "Aunt", "Babysitter", "Brother", "Caller", "Caretaker", "Child", "Cousin", "Daughter", "Family_Friend", "Father", "Friend", "Grandfather", "Grandmother", "Great-Grandmother", "Host", "Housekeeper", "Mother", "Neighbour", "Niece", "Playmate", "Research_Team", "Sibling", "Sister", "Sister-in-law", "Son", "Speaker", "Student", "Subject", "Target_Child", "Teacher", "Toy", "Twin_Brother", "Uncle", "Visitor"]
    permission = "allow"
    yield check_values, table, column, values, permission

    table = "speakers"
    column = "macrorole"
    values = ["Adult", "Child", "Target_Child"]
    permission = "allow"
    yield check_values, table, column, values, permission

    table = "speakers"
    column = "macrorole"
    values = ["Unspecified","None","Unidentified","Unidentified_child","Unidentified_adult"]
    permission = "disallow"
    yield check_values, table, column, values, permission

    # check values that can be composed of smaller building blocks
    table = "morphemes"
    column = "gloss"
    values = [None, "0", "1", "1/2PL", "1DL", "1NSG", "1PL", "1SG", "2", "2DL", "NSG", "2SG", "2PL", "3", "3DL", "3NSG", "3SG", "3PL", "4", "4SYL", "A", "ABIL", "ABL", "ABS", "ACC", "ACROSS", "ACT", "ADESS", "ADJ", "ADJZ", "ADN", "ADV", "ADVZ", "AFF", "AGT", "AGR", "ALL", "ALT", "AMBUL", "ANIM", "ANTIP", "AOR", "APPL", "ART", "ASP", "ASS", "ASSOC", "ATTN", "AUTOBEN", "AUX", "AV", "BABBLE", "BEN", "CAUS", "CHOS", "CLF", "CLIT", "CM", "COM", "COMP", "COMPAR", "COMPL", "CONC", "COND", "CONJ", "CONJ", "CON", "CONT", "CONTEMP", "CONTING", "CONTR", "COP", "CVB", "DAT", "DECL", "DEF", "DEICT", "DEM", "DEP", "DEPR", "DESID", "DESTR", "DET", "DETR", "DIM", "DIR", "DIR", "DIST", "DISTR", "DOWN", "DU", "DUB", "DUR", "DYN", "ECHO", "EMPH", "EQU", "ERG", "EVID", "EXCL", "EXCLA", "EXIST", "EXT", "F", "FILLER", "FOC", "FUT", "FUT1", "GEN", "HAB", "HES", "HHON", "HON", "HORT", "I", "IDEOPH",  "II", "III", "IMIT", "IMP", "IMPERS", "INAL", "INAN", "INCEP", "INCH", "INCL", "INCOMPL", "IND", "IND1", "IND2", "INDF", "INDIR", "INF", "INS", "INSIST", "INTJ", "INTR", "INTRG", "INV", "IPFV", "IRR", "IV", "IX", "LHON", "LNK", "LOC", "M", "MED", "MHON", "MIR", "MOD", "MOOD", "MV", "N", "N", "N", "NAG", "NAME", "NC", "NEG", "NICKNAMER", "NMLZ", "NOM", "NPST", "NSG", "NTVZ", "NUM", "OBJ", "OBJVZ", "OBL", "OBLIG", "OBV", "ONOM", "OPT", "ORD", "P", "PARTIT", "PASS", "PEJ", "PERL", "PERMIS", "PERSIST", "PFV", "PL", "POL", "POSS", "POT", "PRAG", "PRED", "PREDADJ", "PREP", "PREP", "PRF", "PRO", "PROB", "PROG", "PROH", "PROP", "PROX", "PRS", "PST", "PTCL", "PTCP", "PURP", "PV", "PVB", "Q", "QUANT", "QUOT", "RECENT", "RECNF", "RECP", "REF", "REFL", "REL", "REM", "REP", "RES", "REVERS", "S", "S/A", "S/P", "SBJ", "SBJV", "SEQ", "SG", "SIM", "SOC", "SPEC", "STAT", "STEM", "SUPERL", "SURP", "TEASER", "TEL", "TEMP", "TENSE", "TERM", "TOP", "TR", "UP", "V", "VI", "VII", "VIII", "V2", "V.AUX", "V.CAUS", "V.IMP", "V.ITR", "V.PASS", "V.POS", "V.TR", "VBZ", "VOICE", "VN", "VOC", "VOL", "WH", "X", "XI", "XII", "XII", "XIV", "???"]
    yield check_combined_values, table, column, values

    # check format of time columns
    for check in (('sessions','date'),('speakers','birthdate'),('uniquespeakers','birthdate')):
        table = check[0]
        column = check[1]
        yield check_time, table, column
    
    # skim columns for funny characters
    for check in (('words','word','^[-.̃]','disallow'), 
        ('words','word','[\'\(\)\*\"\^\[\]]','disallow'), 
        ('words','word','(?<![^\?])\?(?![^\?])\|^\?[^\?]|[^\?]\?$','disallow'), 
        ('speakers','speaker_label','^[a-zA-Z]{2,}\d*$','allow'), 
        ('speakers','name','\d','disallow'), 
        ('speakers','age','^(\d\d?(;([0-9]|1[01]).([12]?[0-9]|30))?)$','allow')):
        table = check[0]
        column = check[1]
        search_expression = check[2]
        permission = check[3]
        yield check_string, table, column, search_expression, permission    


# check if the proportion of NULL rows in a column is above a certain threshold (for all corpora separately)
def check_proportion_null(corpus, table, column, threshold):
    query = 'select count(*) from ' + table + ' where corpus="' + corpus + '"'
    res = session.execute(query)
    count_all_rows = res.fetchone()[0]
    
    query = 'select count(*) from ' + table + ' where corpus="' + corpus + '" and ' + column + ' is null'
    res = session.execute(query)
    count_null_rows = res.fetchone()[0]
    
    proportion_null = count_null_rows/count_all_rows
    if proportion_null >= 0.01:
        string_null = str(round(proportion_null*100))+'%'
    elif proportion_null < 0.01 and proportion_null > 0:
        string_null = 'at least one'
    elif proportion_null == 0:
        string_null = 'no'
    
    assert_true(proportion_null < threshold, msg=corpus + '.' + table + '.' + column + ' contains ' + string_null + ' NULL (threshold is ' + str(threshold) + ')')

# check if actual/target distinction is correctly parsed: either the distinction is not made at all in a corpus (-> exactly one column all NULL) or it is made (-> at least one row where two columns have different values)
def check_words_actual_target(corpus):
    query = 'select count(*) from words where corpus="' + corpus + '" and word_actual is not null'
    res = session.execute(query)
    count_word_actual = res.fetchone()[0]
    query = 'select count(*) from words where corpus="' + corpus + '" and word_target is not null'
    res = session.execute(query)
    count_word_target = res.fetchone()[0]
    query = 'select count(*) from words where corpus="' + corpus + '" and word_actual != word_target'
    res = session.execute(query)
    count_differences = res.fetchone()[0]
    
    assert_true(
        (count_word_actual == 0 and count_word_target > 0) or 
        (count_word_actual > 0 and count_word_target == 0) or 
        (count_word_actual > 0 and count_word_target > 0 and count_differences > 0),
        msg="word_actual/word_target distinction doesn't make sense in " + corpus + "(either the distinction is not made or if it is made, the columns have to have different contents)"
    )

# compare values in table against standardized set
def check_values(table, column, values, permission):
    query = 'select ' + column + ' from ' + table + ' group by ' + column
    res = session.execute(query)
    rows = res.fetchall()
    for row in rows:
        label = row[0]
        if permission == 'allow':
            assert_in(label, values, msg='value in ' + table + '.' + column + ' not in valid labels')
        elif permission == 'disallow':
            assert_not_in(label, values, msg='value in ' + table + '.' + column+' is not permitted')

# compare complex values in table against standardized set of building blocks
def check_combined_values(table, column, values):
    query = 'select ' + column + ' from ' + table + ' group by ' + column
    res = session.execute(query)
    splitexpr = re.compile("[.>]")
    rows = res.fetchall()
    for row in rows:
        labels = row[0]
        if labels is not None:
            labels = splitexpr.split(labels)
            for label in labels:
                assert_in(label, values, msg='value in ' + table + '.' + column + ' not in valid labels')
        

# check if values can be parsed as datetime
def check_time(table, column):
    query = 'select ' + column + ' from ' + table
    res = session.execute(query)
    rows = res.fetchall()
    for row in rows:
        value = row[0]
        row_time = None
        try:
            row_time = time.strptime(value, '%Y-%m-%d')
        except:
            try:
                row_time = time.strptime(value, '%Y')
            except:
                pass
        assert_true(type(row_time) == time.struct_time, msg='value ' + str(value) + ' in ' + table + '.' + column + ' cannot be parsed as YYYY-MM-DD or YYYY')

# check if column values contain characters
def check_string(table, column, search_expression, permission):
    query = 'select ' + column + ' from ' + table
    res = session.execute(query)
    rows = res.fetchall()
        
    if permission == 'allow':
        for row in rows:            
            value = row[0]
            try:
                assert_true(
                    re.search(search_expression,value) is not None,
                    msg='value ' + str(value) + ' in ' + table + '.' + column + ' contains invalid characters (only regex ' + search_expression + ' allowed)'
                )
            except TypeError: # frequent when value is NULL
                pass
                
    elif permission == 'disallow':
        for row in rows:
            value = row[0]
            try:
                assert_true(
                    re.search(search_expression,value) is None,
                    msg='value ' + str(value) + ' in ' + table + '.' + column + ' contains invalid characters (regex ' + search_expression + ' disallowed)'
                )
            except TypeError: # frequent when value is NULL
                pass