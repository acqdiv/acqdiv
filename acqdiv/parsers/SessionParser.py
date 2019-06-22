"""Abstract class for session parsing."""

from abc import ABC, abstractmethod


class SessionParser(ABC):

    @abstractmethod
    def get_session_metadata(self):
        """Get the metadata of a session.

        Returns:
            dict: The session metadata.
        """
        pass

    @abstractmethod
    def next_speaker(self):
        """Yield participants metadata for the Speaker table in the DB.

        Returns:
            OrderedDict: Speaker (participant) metadata.
        """
        pass

    @abstractmethod
    def next_utterance(self):
        """Yield session level utterance data.

        Returns:
             OrderedDict: Utterance data.
        """
        pass
