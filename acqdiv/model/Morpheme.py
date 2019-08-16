from acqdiv.model.Utterance import Utterance


class Morpheme:

    def __init__(self):
        """Initialize the variables representing a morpheme.

        utterance (acqdiv.model.Utterance.Utterance): The utterance that
            the morpheme belongs to.
        word (acqdiv.model.Word.Word): The word that the morpheme belongs to.
        morpheme_language (str): The language that word is in.
        type (str): Whether the morpheme is an actual or target form.
        morpheme (str): The morpheme itself.
        gloss_raw (str): The original gloss of the morpheme.
        pos_raw (str): The original POS tag of the morpheme.
        pos (str): The POS tag mapped from `pos_raw`.
        pos_ud (str): The Universal Dependency POS tag mapped from `pos_raw`.
        lemma_id (str): The ID of the lemma.
        warning (str): Warnings regarding morpheme.
        """
        self.utterance = Utterance()
        self.word = None
        self.morpheme_language = ''
        self.type = ''
        self.morpheme = ''
        self.gloss_raw = ''
        self.gloss = ''
        self.pos_raw = ''
        self.pos = ''
        self.pos_ud = ''
        self.lemma_id = ''
        self.warning = ''
