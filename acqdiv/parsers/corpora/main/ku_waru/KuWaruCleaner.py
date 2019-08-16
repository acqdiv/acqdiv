import re

from acqdiv.parsers.toolbox.cleaners.ToolboxCleaner import ToolboxCleaner
from acqdiv.parsers.corpora.main.ku_waru.KuWaruPOSMapper import KuWaruPOSMapper
from acqdiv.parsers.corpora.main.ku_waru.KuWaruGlossMapper \
    import KuWaruGlossMapper


class KuWaruCleaner(ToolboxCleaner):

    @classmethod
    def unify_unknown(cls, utterance):
        return utterance.replace('***', '???')

    @classmethod
    def remove_punctuation(cls, utterance):
        utterance = re.sub(r'[?.,]', '', utterance)
        return cls.remove_redundant_whitespaces(utterance)

    @classmethod
    def clean_utterance(cls, utterance):
        utterance = cls.remove_punctuation(utterance)
        utterance = cls.unify_unknown(utterance)
        return utterance

    @classmethod
    def clean_gloss(cls, gloss):
        return KuWaruGlossMapper.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return KuWaruPOSMapper.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return KuWaruPOSMapper.map(pos_ud, ud=True)
