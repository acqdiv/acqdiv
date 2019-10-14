from typing import Iterable

from acqdiv.model.session import Session


class Corpus:
    """Data class representing a corpus.

    corpus (str): The corpus name.
    language (str): The corpus language.
    iso_639_3 (str): The ISO language code.
    glottolog_code (str): The Glottolog language code.
    owner (str): The name of corpus owner.
    sessions (Iterable[Session]): The sessions of the corpus.
    """

    corpus: str
    language: str
    iso_639_3: str
    glottolog_code: str
    owner: str
    sessions: Iterable[Session]

    def __init__(self):
        """Initialize the variables representing a corpus."""
        self.corpus = ''
        self.language = ''
        self.iso_639_3 = ''
        self.glottolog_code = ''
        self.owner = ''
        self.acronym = ''
        self.name = ''
        self.sessions = []
