""" Post-processing processes for acqdiv corpora
"""

# TODO: implement postprocessing tasks:
#  - metadata label unification
#  - date reformatting from the all the various input formats...
#  - additionally calculated stuff like AgeInDays?
#  - morphological label unification
#  - BB's wish for MorphemeID+MorphemeID, WordID+WordID, etc.
#  - deal with age conversion, etc.
#  - add additional inferred info, e.g. Russian ends_at time stamps

# TODO: identify body parsing errors and fixes

# TODO: infer blank cells from the (non-existent input data) existing data?
#  e.g. in Russian Alja is gender x; Sabine is role y...

from sqlalchemy.orm import sessionmaker
from database_backend import *

engine = db_connect()
Session = sessionmaker(bind=engine)
session = Session()

# Post processing of Toolbox Utterance data

# Russian & Indonesian: garbage imported from CHAT
content = re.sub('xxx?|www', '???', content)

for instance in session.query(Utterance).order_by(Utterance.id):
    print(instance.word)

session.close()