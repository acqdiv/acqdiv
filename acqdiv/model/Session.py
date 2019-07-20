

class Session:

    def __init__(self):
        """Set variables representing a session.

        source_id (str): The session name.
        date (str): The session date.
        media_filename (str): The media file name of the session.
        speakers (List[acqdiv.model.Speaker.Speaker]): The session speakers.
        utterances (List[acqdiv.model.Utterance.Utterance]):
            The session utterances.
        """
        self.source_id = ''
        self.date = ''
        self.media_filename = ''
        self.speakers = []
        self.utterances = []
