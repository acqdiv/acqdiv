import glob
import sys

from acqdiv.parsers.SessionParser import SessionParser
from acqdiv.processors.processors import SessionProcessor, logger


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
        self.parser_factory = SessionParser.create_parser(self.cfg)

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
            s = SessionProcessor(self.cfg, session_file,
                    self.parser_factory, self.engine)

            try:
                s.process_session()
            except Exception as e:
                logger.warning("Aborted processing of file {}: "
                               "exception: {}".format(session_file, type(e)),
                               exc_info=sys.exc_info())

                if not catch_errors:
                    raise

            if test:
                break