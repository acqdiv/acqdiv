import glob

from acqdiv.processors.processors import SessionProcessor


class CorpusParser:
    """Parses all sessions of a corpus."""

    def __init__(self, cfg, engine):
        """Initialize config and engine.

        Args:
            cfg (CorpusConfigParser): A config instance.
            engine (Engine): A SQLAlchemy database engine.
        """
        self.cfg = cfg
        self.engine = engine

    def get_session_parser(self, session_path):
        """Get a session parser.

        Returns:
            SessionParser: The session parser.
        """
        raise NotImplementedError

    def process_corpus(self, test=False):
        """Parse all sessions of a corpus.

        Args:
            test (bool): Only process the first file.
        """
        for session_path in sorted(glob.glob(self.cfg['paths']['sessions'])):
            print("\t", session_path)

            session_parser = self.get_session_parser(session_path)

            s = SessionProcessor(
                self.cfg, session_path, session_parser, self.engine)
            s.process_session()

            if test:
                break
