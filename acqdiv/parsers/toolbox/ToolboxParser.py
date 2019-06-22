"""Abstract class for toolbox parsing."""

from abc import abstractmethod
from acqdiv.parsers.SessionParser import SessionParser


class ToolboxParser(SessionParser):

    @abstractmethod
    def get_record_reader(self):
        """Get a record reader.

        Returns: ToolboxReader
        """
        pass

    @abstractmethod
    def get_metadata_reader(self):
        """Get a metadata reader.

        Returns: MetadataParser
        """
        pass
