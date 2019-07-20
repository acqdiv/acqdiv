from acqdiv.model.Session import Session


class Utterance:

    def __init__(self):
        """Initialize the variables representing an utterance.

        session (acqdiv.model.Session.Session): The session that the utterance
            belongs to.
        source_id (str): The ID of the utterance.
        speaker_label (str): The label of the speaker that makes the utterance.
        addressee (str): The label of the speaker whom the utterance is
            addressed at.
        utterance_raw (str): The original utterance.
        utterance (str): The cleaned utterance.
        translation (str): The translation of the utterance.
        morpheme (str): The original morpheme tier.
        gloss_raw (str): The original gloss tier.
        pos_raw (str): The original POS tag tier.
        sentence_type: The type of the utterance.
        childdirected (bool): Whether the utterance is child directed.
        start_raw (str): The original start time of the utterance.
        end_raw (str): The original end time of the utterance.
        comment (str): Any comments about the utterance.
        warning (str): Warnings concering the utterance.
        words (List[acqdiv.model.Word.Word]): The words of the utterance.
        morphemes (List[List[acqdiv.model.Morpheme.Morpheme]]): The morphemes
            of the utterance.
        """
        self.session = Session()
        self.source_id = ''
        self.speaker_label = ''
        self.addressee = ''
        self.utterance_raw = ''
        self.utterance = ''
        self.translation = ''
        self.morpheme = ''
        self.gloss_raw = ''
        self.pos_raw = ''
        self.sentence_type = ''
        self.childdirected = ''
        self.start_raw = ''
        self.end_raw = ''
        self.comment = ''
        self.warning = ''
        self.words = []
        self.morphemes = []
