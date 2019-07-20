"""Abstract class for session parsing."""

from abc import ABC, abstractmethod


class SessionParser(ABC):

    @abstractmethod
    def parse(self):
        """Return an instance of a Session.

        Returns:
            acqdiv.model.Session.Session: The Session instance.
        """
        pass
