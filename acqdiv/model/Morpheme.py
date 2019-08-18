

class Morpheme:
    """Data class representing a morpheme.

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

    morpheme_language: str
    type: str
    morpheme: str
    gloss_raw: str
    gloss: str
    pos_raw: str
    pos: str
    pos_ud: str
    lemma_id: str
    warning: str

    def __init__(self):
        """Initialize the variables representing a morpheme."""
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
