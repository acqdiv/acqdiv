class CHATParserInterface:
    """Interface for parsing the ACQDIV (CHAT) corpora."""

    @staticmethod
    def get_reader():
        """Get a reader instance.

        Returns: ACQDIVCHATReader
        """
        raise NotImplementedError

    @staticmethod
    def get_cleaner():
        """Get a cleaner instance.

        Returns: CHATCleaner
        """
        raise NotImplementedError
