import glob
import os

import acqdiv


def get_path_of_most_recent_database():
    here = os.path.abspath(os.path.dirname(acqdiv.__file__))
    pattern = os.path.join(here, 'database/acqdiv_corpus_*.sqlite3')

    for path in sorted(glob.glob(pattern), reverse=True):
        return 'sqlite:///{}'.format(path)

    print('Database not found!')

    return None
