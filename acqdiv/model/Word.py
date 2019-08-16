from acqdiv.model.Utterance import Utterance


class Word:

    def __init__(self):
        """Initialize the variables representing a word.

        utterance (acqdiv.model.Utterance.Utterance): The utterance that the
            word belongs to.
        word_language (str): The language of the word.
        word (str): The word itself.
        word_actual (str): The actual form of the word.
        word_target (str): The target form of the word.
        pos (str): The POS tag of the word.
        pos_ud (str): The Universal Dependency POS tag of the word.
        """
        self.utterance = Utterance()
        self.word_language = ''
        self.word = ''
        self.word_actual = ''
        self.word_target = ''
        self.pos = ''
        self.pos_ud = ''
        self.warning = ''
