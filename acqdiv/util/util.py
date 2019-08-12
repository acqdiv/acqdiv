import glob
import os

import acqdiv


def get_path_of_most_recent_database():
    pattern = get_full_path('database/acqdiv_corpus_*.sqlite3')

    for path in sorted(glob.glob(pattern), reverse=True):
        return 'sqlite:///{}'.format(path)

    print('Database not found!')

    return None


def get_acqdiv_path():
    return os.path.abspath(os.path.dirname(acqdiv.__file__))


def get_full_path(path_within_acqdiv_package):
    return os.path.join(get_acqdiv_path(), path_within_acqdiv_package)
