""" Post-processing processes for ACQDIV corpora
"""

# TODO: implement postprocessing tasks:
#  - metadata label unification
#  - date reformatting from the all the various input formats...
#  - additionally calculated stuff like AgeInDays?
#  - morphological label unification
#  - BB's wish for MorphemeID+MorphemeID, WordID+WordID, etc.
#  - deal with age conversion, etc.
#  - add additional inferred info, e.g. Russian ends_at time stamps
#  - should we do unique word, morpheme, etc., id assignment in post-processing?

# TODO: identify body parsing errors and fixes

# TODO: infer blank cells from the (non-existent input data) existing data?
#  e.g. in Russian Alja is gender x; Sabine is role y...

from sqlalchemy.orm import sessionmaker
from database_backend import *
from parsers import CorpusConfigParser as ccp
import age

def db_apply(func):
    def update_session(config):
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            func(session, config)
            session.commit()
        except Exception as e:
            session.rollback()
            print("Error {0}: {1}".format(type(e), e))
        finally:
            session.close()
    return update_session

# Post processing of Toolbox Utterance data?

# Russian & Indonesian: garbage imported from CHAT
#  SM: i think this is done in the parser
#content = re.sub('xxx?|www', '???', content)

# example call (why is it so $^*%@* slow?)
#for instance in session.query(Utterance).order_by(Utterance.id):
#    print(instance.word)


def update_xml_age(session):
    for row in session.query(Speaker).filter(Speaker.age != None):
        nage = age.format_xml_age(row.age)
        if nage != 0:
            row.age = nage

def update_imdi_age(session):
    for row in session.query(Speaker).filter(Speaker.age.like("Un%"), ~Speaker.birthdate.like("Un%")):
        srow = session.query(Session).filter(Session.session_id == row.parent_id).one()
        try:
            recdate = age.numerize_date(srow.date)
            bdate = age.numerize_date(row.birthdate)
            agelist = age.format_imdi_age(bdate, recdate)
            row.age = agelist[0]
            row.age_in_days = agelist[1]
        except Exception as e:
                print("Couldn't calculate age of speaker {0}".format(row.id))
                print("Error: {0}".format(e))

@db_apply
def update_age(session, config):
    if config["metadata"]["type"] == "IMDI":
        update_imdi_age(session)
    else:
        update_xml_age(session)


@db_apply
def unify_glosses(session, config):
    for row in session.query(Morpheme):
        old_gloss = row.gloss
        if old_gloss in config["gloss"]:
            new_gloss = config["gloss"][old_gloss]
            row.gloss = new_gloss

if __name__ == "__main__":
    cfg = ccp()
    cfg.read("Russian.ini")

    update_age(cfg)
    unify_glosses(cfg)
