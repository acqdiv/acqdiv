from typing import List, Optional

from acqdiv.model.Word import Word
from acqdiv.model.Morpheme import Morpheme


class Utterance:
    """Data class representing an utterance.

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
    words (List[Word]): The words of the utterance.
    morphemes (List[Morpheme]]): The morphemes of the utterance.
    """

    source_id: str
    speaker_label: str
    addressee: str
    utterance_raw: str
    utterance: str
    translation: str
    morpheme: str
    gloss_raw: str
    pos_raw: str
    sentence_type: str
    childdirected: str
    start_raw = str
    end_raw: str
    comment: str
    warning: str
    words: List[Word]
    morphemes: List[Morpheme]

    def __init__(self):
        """Initialize the variables representing an utterance."""
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
