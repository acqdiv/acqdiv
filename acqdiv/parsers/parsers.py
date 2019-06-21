""" Parsers for ACQDIV corpora, e.g. CHAT XML, Toolbox files
"""

import logging
from acqdiv.parsers.ParserMapper import ParserMapper


logger = logging.getLogger('pipeline.' + __name__)


class SessionParser(object):
    """ Static class-level method to create a new parser instance based on session format type.
    """

    def __init__(self, config, file_path):
        """ Session parser initializer

        Args:
            config: corpus config ini file
            file_path: path to a corpus session file
        """
        self.config = config
        self.file_path = file_path

    @staticmethod
    def create_parser_factory(config):
        """Create a corpus session parser based on input format type.

        Args:
            config: CorpusConfigParser

        Returns:
            A corpus-type-specific parser
        """
        format = config['corpus']['format']
        corpus = config['corpus']['corpus']

        parser = ParserMapper.map(corpus)

        if format == "cha":
            return parser
        elif format == "toolbox":
            return lambda file_path: parser(config, file_path)
        else:
            assert 0, "Unknown format type: " + format

    def get_sha1(self):
        # TODO: get SHA1 fingerprint for each session file and write to the sessions table.
        pass

    def get_session_metadata(self):
        """ Gets session metadata for the Sessions table in the db
        """
        pass

    def next_speaker(self):
        """ Yield speakers for the Speaker table in the db
        """
        pass

    def next_utterance(self):
        """ Yield utterances for the Utterance table in the db
        """
        pass
