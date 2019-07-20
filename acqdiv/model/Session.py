from acqdiv.model.Corpus import Corpus


class Session:

    def __init__(self):
        """Set variables representing a session.

        corpus (acqdiv.model.Corpus.Corpus): The corpus that the session
            belongs to.
        source_id (str): The session name.
        date (str): The session date.
        media_filename (str): The media file name of the session.
        speakers (List[acqdiv.model.Speaker.Speaker]): The session speakers.
        utterances (List[acqdiv.model.Utterance.Utterance]):
            The session utterances.
        """
        self.corpus = Corpus()
        self.source_id = ''
        self.date = ''
        self.media_filename = ''
        self.speakers = []
        self.utterances = []
