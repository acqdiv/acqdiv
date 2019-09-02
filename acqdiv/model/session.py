from typing import List

from acqdiv.model.utterance import Utterance
from acqdiv.model.speaker import Speaker


class Session:
    """Data class representing a session.

    source_id (str): The session name.
    date (str): The session date.
    media_filename (str): The media file name of the session.
    duration (str): The duration of the session.
    speakers (List[Speaker]): The session speakers.
    utterances (List[Utterance]): The session utterances.
    """

    source_id: str
    date: str
    media_filename: str
    duration: str
    speakers: List[Speaker]
    utterances: List[Utterance]

    def __init__(self):
        """Initialize variables representing a session."""
        self.source_id = ''
        self.date = ''
        self.media_filename = ''
        self.duration = ''
        self.speakers = []
        self.utterances = []
