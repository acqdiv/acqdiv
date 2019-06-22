from acqdiv.parsers.SessionParser import SessionParser
from abc import abstractmethod


class CHATParser(SessionParser):
    """Interface for parsing the ACQDIV (CHAT) corpora."""

    @staticmethod
    @abstractmethod
    def get_reader():
        """Get a reader instance.

        Returns: BaseCHATReader
        """
        pass

    @staticmethod
    @abstractmethod
    def get_cleaner():
        """Get a cleaner instance.

        Returns: BaseCHATCleaner
        """
        pass
