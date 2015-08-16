""" Post-processing processes for acqdiv corpora
"""

# TODO: implement postprocessing tasks:
#  - metadata label unification
#  - date reformatting from the all the various input formats...
#  - additionally calculated stuff like AgeInDays?
#  - morphological label unification
#  - BB's wish for MorphemeID+MorphemeID, WordID+WordID, etc.

# TODO: identify body parsing errors and fixes

from sqlalchemy.orm import sessionmaker
from database_backend import *

engine = db_connect()
Session = sessionmaker(bind=engine)
session = Session()

for instance in session.query(Utterance).order_by(Utterance.id):
    print(instance.word)