from acqdiv.parsers.ParserMapper import ParserMapper


class SessionParser(object):
    """Create a new parser instance based on session format type."""

    def __init__(self, config, file_path):
        """Initialize config and session file.

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
        fmat = config['corpus']['format']
        corpus = config['corpus']['corpus']

        parser = ParserMapper.map(corpus)

        if fmat == "cha":
            return parser
        elif fmat == "toolbox":
            return lambda file_path: parser(config, file_path)
        else:
            assert 0, "Unknown format type: " + fmat

    def get_sha1(self):
        pass

    def get_session_metadata(self):
        """Get session metadata for the Sessions table in the db."""
        pass

    def next_speaker(self):
        """Yield speakers for the Speaker table in the db."""
        pass

    def next_utterance(self):
        """Yield utterances for the Utterance table in the db."""
        pass
