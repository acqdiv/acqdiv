import glob

from acqdiv.processors.processors import SessionProcessor


class CorpusParser:
    """ Handler for processing each session file in particular corpus.
    """
    def __init__(self, cfg, engine):
        """ Initializes a CorpusParser object then calls a SessionProcessor for each session input file.

        Args:
            cfg: CorpusConfigParser
            engine: sqlalchemy database engine
        """
        self.cfg = cfg
        self.engine = engine

    def get_session_parser(self, session_path):
        pass

    def process_corpus(self, catch_errors=False, test=False):
        """Process corpus files.

        Args:
            catch_errors (bool): Catch errors.
            test (bool): Only process the first file.
        """
        for session_file in sorted(glob.glob(self.cfg['paths']['sessions'])):
            print("\t", session_file)

            session_parser = self.get_session_parser(session_file)

            s = SessionProcessor(
                self.cfg, session_file, session_parser, self.engine)
            s.process_session()

            if test:
                break
