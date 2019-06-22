from acqdiv.parsers.ParserMapper import ParserMapper


class SessionParser:
    """Create a new parser instance based on session format type."""

    @staticmethod
    def create_parser(config):
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
