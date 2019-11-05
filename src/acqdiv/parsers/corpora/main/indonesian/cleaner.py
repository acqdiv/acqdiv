import re

from acqdiv.parsers.toolbox.cleaners.cleaner import ToolboxCleaner
from acqdiv.parsers.corpora.main.indonesian.gloss_mapper \
    import IndonesianGlossMapper
from acqdiv.parsers.corpora.main.indonesian.pos_mapper \
    import IndonesianPOSMapper


class IndonesianCleaner(ToolboxCleaner):

    @classmethod
    def remove_utterance_punctuation(cls, utterance):
        utterance = re.sub('[‘’\'“”\".!,;:+/]|\?$|<|>', '', utterance)
        return cls.remove_redundant_whitespaces(utterance)

    @classmethod
    def remove_insecure_transcription_marker(cls, utterance):
        return re.sub('\[\?\]', '', utterance)

    @classmethod
    def clean_utterance(cls, utterance):
        for cleaning_method in [
                super().clean_utterance, cls.remove_utterance_punctuation,
                cls.remove_insecure_transcription_marker]:
            utterance = cleaning_method(utterance)

        return utterance

    @staticmethod
    def remove_morph_tier_punctuation(morpheme_tier):
        return re.sub('[‘’\'“”\".!,:?+/]', '', morpheme_tier)

    @staticmethod
    def unify_unknown(utterance):
        return re.sub('xxx?|www|0', '???', utterance)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        for cleaning_method in [
                cls.remove_morph_tier_punctuation, cls.unify_unknown]:
            morph_tier = cleaning_method(morph_tier)
        return morph_tier

    @classmethod
    def clean_gloss(cls, gloss):
        return IndonesianGlossMapper.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return IndonesianPOSMapper.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return IndonesianPOSMapper.map(pos_ud, ud=True)
