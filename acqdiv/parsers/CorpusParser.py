"""Abstract class for corpus parsing."""

import glob

from abc import ABC, abstractmethod


class CorpusParser(ABC):
    """Parses all sessions of a corpus."""

    def __init__(self, cfg):
        """Initialize config.

        Args:
            cfg (CorpusConfigParser): A config instance.
        """
        self.cfg = cfg

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
