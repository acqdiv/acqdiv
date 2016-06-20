import configparser
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import time
from nose.tools import assert_equal, assert_in, assert_not_equal, assert_true, assert_false


session = None

def setup():
    global cfg, session
    engine = sa.create_engine('sqlite:///test.sqlite3')
    meta = sa.MetaData(engine, reflect=True)
    Session = sessionmaker(bind=engine)
    session = Session()


def test_database_integrity():
    # Note: SQL "NULL" returns as Python None

    # check various value sets
    table = "morphemes"
    column = "gloss"
    values = [None, "0", "1", "2", "3", "4", "4SYL", "A", "ABIL", "ABL", "ABS", "ACC", "ACROSS", "ACT", "ADESS", "ADJ", "ADJZ", "ADN", "ADV", "ADVZ", "AFF", "AGT", "AGR", "ALL", "ALT", "AMBUL", "ANIM", "ANTIP", "AOR", "APPL", "ART", "ASP", "ASS", "ASSOC", "ATTN", "AUTOBEN", "AUX", "AV", "BABBLE", "BEN", "CAUS", "CHOS", "CLF", "CLIT", "CM", "COM", "COMP", "COMPAR", "COMPL", "CONC", "COND", "CONJ", "CONJ", "CON", "CONT", "CONTEMP", "CONTING", "CONTR", "COP", "CVB", "DAT", "DECL", "DEF", "DEICT", "DEM", "DEP", "DEPR", "DESID", "DESTR", "DET", "DETR", "DIM", "DIR", "DIR", "DIST", "DISTR", "DOWN", "DU", "DUB", "DUR", "DYN", "ECHO", "EMPH", "EQU", "ERG", "EVID", "EXCL", "EXCLA", "EXIST", "EXT", "F", "FILLER", "FOC", "FUT", "GEN", "HAB", "HES", "HHON", "HON", "HORT", "IDEOPH", "IMIT", "IMP", "IMPERS", "INAL", "INAN", "INCEP", "INCH", "INCL", "INCOMPL", "IND", "INDF", "INDIR", "INF", "INS", "INSIST", "INTJ", "INTR", "INTRG", "INV", "IPFV", "IRR", "LNK", "LOC", "M", "MED", "MHON", "MIR", "MOD", "MOOD", "MV", "N", "N", "N", "NAG", "NAME", "NC", "NEG", "NICKNAMER", "NMLZ", "NOM", "NPST", "NSG", "NTVZ", "NUM", "OBJ", "OBJVZ", "OBL", "OBLIG", "OBV", "ONOM", "OPT", "ORD", "P", "PARTIT", "PASS", "PEJ", "PERL", "PERMIS", "PERSIST", "PFV", "PL", "POL", "POSS", "POT", "PRAG", "PRED", "PREDADJ", "PREP", "PREP", "PRF", "PRO", "PROB", "PROG", "PROH", "PROP", "PROX", "PRS", "PST", "PTCL", "PTCP", "PURP", "PV", "PVB", "Q", "QUANT", "QUOT", "RECENT", "RECNF", "RECP", "REF", "REFL", "REL", "REM", "REP", "RES", "REVERS", "S", "SBJ", "SBJV", "SEQ", "SG", "SIM", "SOC", "SPEC", "STAT", "STEM", "SUPERL", "SURP", "TEASER", "TEL", "TEMP", "TENSE", "TERM", "TOP", "TR", "UP", "V", "V2", "V.AUX", "V.CAUS", "V.IMP", "V.ITR", "V.PASS", "V.POS", "V.TR", "VBZ", "VOICE", "VN", "VOC", "VOL", "WH", "???"]
    yield check_values, table, column, values

    table = "utterances"
    column = "sentence_type"
    values = [None, "default", "question", "exclamation", "imperative", "action", "trail off", "interruption", "trail off question", "self interruption", "quotation precedes", "interruption question"]
    yield check_values, table, column, values

    table = "morphemes"
    column = "pos"
    values = [None, "ADJ", "ADV", "ART", "AUX", "CLF", "CONJ", "IDEOPH", "INTJ", "N", "NUM", "pfx", "POST", "PREP", "PRODEM", "PTCL", "QUANT", "sfx", "stem", "V", "???"]
    yield check_values, table, column, values

    table = "speakers"
    column = "gender"
    values = ["Female", "Male", "Unknown"]
    yield check_values, table, column, values

    # TODO: https://github.com/uzling/acqdiv/issues/351
    table = "speakers"
    column = "role"
    values = ["Adult", "Aunt", "Babysitter", "Brother", "Caller", "Caretaker", "Cousin", "Daughter", "Family_Friend", "Father", "Friend", "Grandfather", "Grandmother", "Great-Grandmother", "Host", "Housekeeper", "Mother", "Neighbour", "Niece", "Playmate", "Research_Team", "Sibling", "Sister", "Sister-in-law", "Son", "Speaker", "Student", "Subject", "Target_Child", "Teacher", "Toy", "Twin_Brother", "Uncle", "Unknown", "Visitor"]
    yield check_values, table, column, values

    table = "speakers"
    column = "macrorole"
    values = ["Adult", "Child", "Target_Child", "Unknown"]
    yield check_values, table, column, values

    # check columns for at least one NULL
    for check in (("sessions","date"),("utterances","speaker_label"),("utterances","utterance_raw"),("utterances","utterance"),("words","word"),("speakers","speaker_label"),("speakers","macrorole"),("uniquespeakers","speaker_label"),("uniquespeakers","corpus")):
        table = check[0]
        column = check[1]
        yield check_any_null, table, column    
    
    # XXX, XX1, etc., and AUX create NULL
    # query = "select count(*) from speakers where name is null"
    # yield check_any_null, query

    # check columns for all NULL
    for check in (("utterances","translation"),("utterances","morpheme"),("utterances","gloss_raw"),("utterances","pos_raw"),("words","pos"),("morphemes","morpheme"),("morphemes","gloss_raw"),("morphemes","gloss"),("morphemes","pos_raw"),("morphemes","pos"),("speakers","name"),("speakers","age_raw"),("speakers","age"),("speakers","age_in_days"),("speakers","gender_raw"),("speakers","gender"),("speakers","role_raw"),("speakers","role")):
        table = check[0]
        column = check[1]
        yield check_all_null, table, column

    # compare word_actual and word_target
    yield check_words_actual_target
        
    # skim columns for funny characters
    table = 'words'
    column = 'word'
    search_expression = '^\s*$'
    permission = 'disallow'
    yield check_string, table, column, search_expression, permission

    table = 'words'
    column = 'word'
    search_expression = '^[-.̃]'
    permission = 'disallow'
    yield check_string, table, column, search_expression, permission
    
    table = 'words'
    column = 'word'
    search_expression = '[\'\(\)\*\"\^_\[\]]'
    permission = 'disallow'
    yield check_string, table, column, search_expression, permission

    table = 'words'
    column = 'word'
    search_expression = '(?<![^\?])\?(?![^\?])\|^\?[^\?]|[^\?]\?$'
    permission = 'disallow'
    yield check_string, table, column, search_expression, permission

    table = 'speakers'
    column = 'speaker_label'
    search_expression = '^[a-zA-Z]{2,}\d*$'
    permission = 'allow'
    yield check_string, table, column, search_expression, permission
    
    table = 'speakers'
    column = 'name'
    search_expression = '\d'
    permission = 'disallow'
    yield check_string, table, column, search_expression, permission
    
    table = 'speakers'
    column = 'age'
    search_expression = '^(\d\d?(;([0-9]|1[01]).([12]?[0-9]|30))?)$'
    permission = 'allow'
    yield check_string, table, column, search_expression, permission
    
    for check in (('sessions','date'),('speakers','birthdate'),('uniquespeakers','birthdate')):
        table = check[0]
        column = check[1]
        yield check_time, table, column


# check if values can be parsed as datetime
def check_time(table, column):
    query = 'select ' + column + ' from ' + table
    res = session.execute(query)
    rows = res.fetchall()
    for row in rows:
        label = row[0]
        try:
            time.strptime(label, '%Y-%m-%d')
        except:
            try:
                time.strptime(label, '%Y')
            except:
                assert_true(0, msg=table+'.'+column+' cannot be parsed as YYYY-MM-DD')
            
# compare values in table against standardized set
def check_values(table, column, values):
    query = 'select ' + column + ' from ' + table + ' group by ' + column
    res = session.execute(query)
    rows = res.fetchall()
    for row in rows:
        label = row[0]
        assert_in(label, values, msg='%s in database, but not in valid labels' % (label))

# check if column values contain characters
def check_string(table, column, search_expression, permission):
    query = 'select ' + column + ' from ' + table
    res = session.execute(query)
    rows = res.fetchall()
    regex = re.compile(search_expression)
    for row in rows:
        if permission == 'disallow':
            assert_false(
                re.search(regex,row),
                msg=table+'.'+column+' contains invalid characters (regex '+regex+' disallowed)'
            )
        elif permission == 'allow':
            assert_true(
                re.search(regex,row),
                msg=table+'.'+column+' contains invalid characters (only regex '+regex+' allowed)'
            )

# check if a column in a table contains at least one NULL
def check_any_null(table, column):
    query = 'select count(*) from ' + table + ' where ' + column + ' is null'
    res = session.execute(query)
    actual = res.fetchone()[0]
    assert_equal(actual, 0, msg=table+'.'+column+' contains NULL')

# check if a column in a table contains nothing but NULL (for all corpora separately)
def check_all_null(table, column):
    for corpus in ('Chintang', 'Cree', 'Indonesian', 'Inuktitut', 'Japanese_Miyata', 'Japanese_MiiPro', 'Russian', 'Sesotho', 'Turkish', 'Yucatec'):
        query = 'select count(*) from ' + table + ' where corpus="' + corpus + '" and ' + column + ' is not null'
        res = session.execute(query)
        actual = res.fetchone()[0]
        assert_not_equal(actual, 0, msg=corpus+'.'+table+'.'+column+' contains only NULL')

# check if actual/target distinction is correctly parsed: either the distinction is not made at all in a corpus (-> exactly one column all NULL) or it is made (-> at least one row where two columns have different values)
def check_words_actual_target():
    for corpus in ('Chintang', 'Cree', 'Indonesian', 'Inuktitut', 'Japanese_Miyata', 'Japanese_MiiPro', 'Russian', 'Sesotho', 'Turkish', 'Yucatec'):
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


# TODO
# 
# # name can be anything or "Unknown" but not "Unspecified" or "None" (the problem with these values is that they can create additional unique pseudo-speakers)
# # the majority of rows should not have NULL in macrorole. A threshold of 15% should be realistic.
# # extract list of all speakers where out of {speaker_label, name, birthdate} two are identical. Sort by speaker label and check manually for mistakes (two speakers as one, one speaker as two)


"""
# TODO: add more tests... on the corpus by corpus level
def test_percent_nulls():
    corpora = ['Chintang', 'Cree', 'Indonesian', 'Inuktitut', 'Japanese_Miyata',
               'Japanese_MiiPro', 'Russian', 'Sesotho', 'Turkish', 'Yucatec']
    res = session.execute("select count(*) from ")
    actual = res.fetchone()[0]
    assert_equal(actual, 0, msg='Column contains NULL')

def test_types():
    # e.g. that no numbers are in speaker_label fields, etc.
    pass
"""