"""Abstract class for session parsing."""

from abc import ABC, abstractmethod


class SessionParser(ABC):

    @abstractmethod
    def parse(self):
        """Return an instance of a Session.

        Returns:
            acqdiv.model.session.Session: The Session instance.
        """
        pass
