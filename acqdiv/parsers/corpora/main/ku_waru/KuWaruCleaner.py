import re

from acqdiv.parsers.toolbox.cleaners.ToolboxCleaner import ToolboxCleaner


class KuWaruCleaner(ToolboxCleaner):

    @classmethod
    def unify_unknown(cls, utterance):
        return utterance.replace('***', '???')

    @classmethod
    def remove_punctuation(cls, utterance):
        utterance = re.sub(r'[?.]', '', utterance)
        return cls.remove_redundant_whitespaces(utterance)

    @classmethod
    def clean_utterance(cls, utterance):
        utterance = cls.remove_punctuation(utterance)
        utterance = cls.unify_unknown(utterance)
        return utterance
