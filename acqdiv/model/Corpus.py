
class Corpus:

    def __init__(self):
        self.corpus = ''
        self.language = ''
        self.iso_639_3 = ''
        self.glottolog_code = ''
        self.owner = ''
        self.sessions = None

        # TODO: move them to right place
        self.morpheme_type = ''
        self.session_labels = None
        self.speaker_labels = None
