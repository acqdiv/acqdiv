"""Abstract class for corpus parsing."""

import glob

from abc import ABC, abstractmethod
from acqdiv.model.Corpus import Corpus


class CorpusParser(ABC):
    """Methods for constructing a corpus instance."""

    def __init__(self, cfg):
        """Initialize config.

        Args:
            cfg (CorpusConfigParser): A config instance.
        """
        self.cfg = cfg

    def parse(self):
        """Construct a Corpus instance."""
        corpus = Corpus()
        corpus.iso_639_3 = self.cfg['corpus']['iso639-3']
        corpus.glottolog_code = self.cfg['corpus']['glottolog_code']
        corpus.corpus = self.cfg['corpus']['corpus']
        corpus.language = self.cfg['corpus']['language']
        corpus.owner = self.cfg['corpus']['owner']
        corpus.sessions = self.iter_sessions()
        corpus.morpheme_type = self.cfg['morphemes']['type']

        return corpus

    @abstractmethod
    def get_session_parser(self, session_path):
        """Get a session parser.

        Returns:
            acqdiv.parsers.SessionParser: The session parser.
        """
        pass

    def iter_sessions(self):
        """Iter the session of the corpus.

        Yields:
            acqdiv.parsers.SessionParser: The session parser.
        """
        for session_path in sorted(glob.glob(self.cfg['paths']['sessions'])):
            print("\t", session_path)

            session_parser = self.get_session_parser(session_path)

            if session_parser is not None:
                yield session_parser
