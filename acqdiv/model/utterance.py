from typing import List, Optional

from acqdiv.model.speaker import Speaker
from acqdiv.model.word import Word
from acqdiv.model.morpheme import Morpheme


class Utterance:
    """Data class representing an utterance.

    source_id (str): The ID of the utterance.
    speaker_label (str): The label of the speaker that makes the utterance.
    addressee (str): The label of the speaker whom the utterance is
        addressed at.
    utterance_raw (str): The original utterance.
    utterance (str): The cleaned utterance.
    actual_utterance (str): The actual utterance.
    target_utterance (str): The target utterance.
    translation (str): The translation of the utterance.
    morpheme_raw (str): The original morpheme tier.
    morpheme (str): The cleaned morpheme tier.
    gloss_raw (str): The original gloss tier.
    gloss (str): The cleaned gloss tier.
    pos_raw (str): The original POS tag tier.
    pos (str): The cleaned POS tag tier.
    sentence_type: The type of the utterance.
    childdirected (bool): Whether the utterance is child directed.
    start_raw (str): The original start time of the utterance.
    start (str): The cleaned start time of the utterance.
    end_raw (str): The original end time of the utterance.
    end (str): The cleaned end time of the utterance.
    comment (str): Any comments about the utterance.
    warning (str): Warnings concering the utterance.
    words (List[Word]): The words of the utterance.
    morphemes (List[Morpheme]]): The morphemes of the utterance.
    """

    source_id: str
    speaker: Optional[Speaker]
    addressee: Optional[Speaker]
    utterance_raw: str
    utterance: str
    actual_utterance: str
    target_utterance: str
    translation: str
    morpheme_raw: str
    morpheme: str
    gloss_raw: str
    gloss: str
    pos_raw: str
    pos: str
    sentence_type: str
    childdirected: str
    start_raw = str
    start = str
    end_raw: str
    end: str
    comment: str
    warning: str
    words: List[Word]
    morphemes: List[List[Morpheme]]

    def __init__(self):
        """Initialize the variables representing an utterance."""
        self.source_id = ''
        self.speaker = None
        self.addressee = None
        self.utterance_raw = ''
        self.utterance = ''
        self.actual_utterance = ''
        self.target_utterance = ''
        self.translation = ''
        self.morpheme_raw = ''
        self.morpheme = ''
        self.gloss_raw = ''
        self.gloss = ''
        self.pos_raw = ''
        self.pos = ''
        self.sentence_type = ''
        self.childdirected = ''
        self.start_raw = ''
        self.start = ''
        self.end_raw = ''
        self.end = ''
        self.comment = ''
        self.warning = ''
        self.words = []
        self.morphemes = []
