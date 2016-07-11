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

    # check number of NULLs per corpus.column
    # (1) column mustn't contain a single NULL
    for check in (("sessions","date"),("utterances","speaker_label"),("utterances","utterance_raw"),("utterances","utterance"),("words","word"),("speakers","speaker_label"),("speakers","macrorole"),("uniquespeakers","speaker_label"),("uniquespeakers","corpus")):
        table = check[0]
        column = check[1]
        threshold = 1/8500000 # based on the number of rows in our largest table, words (8,467,107 rows): the only proportion of NULLs that can possibly be smaller than this is a real 0
        for corpus in ('Chintang', 'Cree', 'Indonesian', 'Inuktitut', 'Japanese_Miyata', 'Japanese_MiiPro', 'Russian', 'Sesotho', 'Turkish', 'Yucatec'):
            yield check_proportion_null, corpus, table, column, threshold
            # yield check_any_null, table, column
    
    # (2) column must contain at least one non-NULL
    # TODO some corpora regularly have all-NULL columns, e.g. birthdate in the Japanese corpora or gender in Sesotho -> exclude these from checks to reduce number of fails
    for check in (("utterances","translation"),("utterances","morpheme"),("utterances","gloss_raw"),("utterances","pos_raw"),("words","pos"),("morphemes","morpheme"),("morphemes","gloss_raw"),("morphemes","gloss"),("morphemes","pos_raw"),("morphemes","pos"),("speakers","name"),("speakers","age_raw"),("speakers","age"),("speakers","age_in_days"),("speakers","gender_raw"),("speakers","gender"),("speakers","role_raw"),("speakers","role")):
        table = check[0]
        column = check[1]
        threshold = 1
        for corpus in ('Chintang', 'Cree', 'Indonesian', 'Inuktitut', 'Japanese_Miyata', 'Japanese_MiiPro', 'Russian', 'Sesotho', 'Turkish', 'Yucatec'):
            yield check_proportion_null, corpus, table, column, threshold
            # yield check_all_null, table, column

    # (3) column mustn't contain more NULLs than some other threshold value
    table = 'speakers'
    column = 'macrorole'
    threshold = 0.15
    for corpus in ('Chintang', 'Cree', 'Indonesian', 'Inuktitut', 'Japanese_Miyata', 'Japanese_MiiPro', 'Russian', 'Sesotho', 'Turkish', 'Yucatec'):
        yield check_proportion_null, corpus, table, column, threshold

    # compare word_actual and word_target
    for corpus in ('Chintang', 'Cree', 'Indonesian', 'Inuktitut', 'Japanese_Miyata', 'Japanese_MiiPro', 'Russian', 'Sesotho', 'Turkish', 'Yucatec'):
        yield check_words_actual_target, corpus

    # check various standardized value sets
    # TODO: https://github.com/uzling/acqdiv/issues/351
    # XXX, XX1, etc., and AUX create NULL
    # query = "select count(*) from speakers where name is null"
    # yield check_any_null, query
    
    table = "morphemes"
    column = "gloss"
    values = [None, "0", "1", "2", "3", "4", "4SYL", "A", "ABIL", "ABL", "ABS", "ACC", "ACROSS", "ACT", "ADESS", "ADJ", "ADJZ", "ADN", "ADV", "ADVZ", "AFF", "AGT", "AGR", "ALL", "ALT", "AMBUL", "ANIM", "ANTIP", "AOR", "APPL", "ART", "ASP", "ASS", "ASSOC", "ATTN", "AUTOBEN", "AUX", "AV", "BABBLE", "BEN", "CAUS", "CHOS", "CLF", "CLIT", "CM", "COM", "COMP", "COMPAR", "COMPL", "CONC", "COND", "CONJ", "CONJ", "CON", "CONT", "CONTEMP", "CONTING", "CONTR", "COP", "CVB", "DAT", "DECL", "DEF", "DEICT", "DEM", "DEP", "DEPR", "DESID", "DESTR", "DET", "DETR", "DIM", "DIR", "DIR", "DIST", "DISTR", "DOWN", "DU", "DUB", "DUR", "DYN", "ECHO", "EMPH", "EQU", "ERG", "EVID", "EXCL", "EXCLA", "EXIST", "EXT", "F", "FILLER", "FOC", "FUT", "GEN", "HAB", "HES", "HHON", "HON", "HORT", "IDEOPH", "IMIT", "IMP", "IMPERS", "INAL", "INAN", "INCEP", "INCH", "INCL", "INCOMPL", "IND", "INDF", "INDIR", "INF", "INS", "INSIST", "INTJ", "INTR", "INTRG", "INV", "IPFV", "IRR", "LNK", "LOC", "M", "MED", "MHON", "MIR", "MOD", "MOOD", "MV", "N", "N", "N", "NAG", "NAME", "NC", "NEG", "NICKNAMER", "NMLZ", "NOM", "NPST", "NSG", "NTVZ", "NUM", "OBJ", "OBJVZ", "OBL", "OBLIG", "OBV", "ONOM", "OPT", "ORD", "P", "PARTIT", "PASS", "PEJ", "PERL", "PERMIS", "PERSIST", "PFV", "PL", "POL", "POSS", "POT", "PRAG", "PRED", "PREDADJ", "PREP", "PREP", "PRF", "PRO", "PROB", "PROG", "PROH", "PROP", "PROX", "PRS", "PST", "PTCL", "PTCP", "PURP", "PV", "PVB", "Q", "QUANT", "QUOT", "RECENT", "RECNF", "RECP", "REF", "REFL", "REL", "REM", "REP", "RES", "REVERS", "S", "SBJ", "SBJV", "SEQ", "SG", "SIM", "SOC", "SPEC", "STAT", "STEM", "SUPERL", "SURP", "TEASER", "TEL", "TEMP", "TENSE", "TERM", "TOP", "TR", "UP", "V", "V2", "V.AUX", "V.CAUS", "V.IMP", "V.ITR", "V.PASS", "V.POS", "V.TR", "VBZ", "VOICE", "VN", "VOC", "VOL", "WH", "???"]
    permission = "allow"
    yield check_values, table, column, values, permission

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
    values = ["Female", "Male", "Unknown"]
    permission = "allow"
    yield check_values, table, column, values, permission
    
    table = "speakers"
    column = "role"
    values = ["Adult", "Aunt", "Babysitter", "Brother", "Caller", "Caretaker", "Cousin", "Daughter", "Family_Friend", "Father", "Friend", "Grandfather", "Grandmother", "Great-Grandmother", "Host", "Housekeeper", "Mother", "Neighbour", "Niece", "Playmate", "Research_Team", "Sibling", "Sister", "Sister-in-law", "Son", "Speaker", "Student", "Subject", "Target_Child", "Teacher", "Toy", "Twin_Brother", "Uncle", "Unknown", "Visitor"]
    permission = "allow"
    yield check_values, table, column, values, permission

    table = "speakers"
    column = "macrorole"
    values = ["Adult", "Child", "Target_Child", "Unknown"]
    permission = "allow"
    yield check_values, table, column, values, permission

    table = "speakers"
    column = "macrorole"
    values = ["Unspecified","None","Unidentified","Unidentified_child","Unidentified_adult"]
    permission = "disallow"
    yield check_values, table, column, values, permission
    
    # check format of time columns
    for check in (('sessions','date'),('speakers','birthdate'),('uniquespeakers','birthdate')):
        table = check[0]
        column = check[1]
        yield check_time, table, column
    
    # skim columns for funny characters
    for check in (('words','word','^\s*$','disallow'), ('words','word','^[-.̃]','disallow'), ('words','word','[\'\(\)\*\"\^_\[\]]','disallow'), ('words','word','(?<![^\?])\?(?![^\?])\|^\?[^\?]|[^\?]\?$','disallow'), ('speakers','speaker_label','^[a-zA-Z]{2,}\d*$','allow'), ('speakers','name','\d','disallow'), ('speakers','age','^(\d\d?(;([0-9]|1[01]).([12]?[0-9]|30))?)$','allow')):
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

# # older tests for at least one NULL/all NULL; now covered by check_proportion_null()
# # check if a column in a table contains at least one NULL
# def check_any_null(table, column):
#     query = 'select count(*) from ' + table + ' where ' + column + ' is null'
#     res = session.execute(query)
#     actual = res.fetchone()[0]
#     assert_equal(actual, 0, msg=table + '.' + column + ' contains NULL')

# # check if a column in a table contains nothing but NULL (for all corpora separately)
# def check_all_null(corpus, table, column):
#     query = 'select count(*) from ' + table + ' where corpus="' + corpus + '" and ' + column + ' is not null'
#     res = session.execute(query)
#     actual = res.fetchone()[0]
#     assert_not_equal(actual, 0, msg=corpus + '.' + table + '.' + column + ' contains only NULL')

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
    if permission == 'allow':
        for row in rows:
            label = row[0]
            assert_in(label, values, msg='value in ' + table + '.' + column + ' not in valid labels')
    elif permission == 'disallow':
        for row in rows:
            label = row[0]
            assert_not_in(label, values, msg='value in ' + table + '.' + column+' is not permitted')

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