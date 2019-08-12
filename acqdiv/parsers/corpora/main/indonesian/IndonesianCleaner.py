import re

from acqdiv.parsers.toolbox.cleaners.ToolboxCleaner import ToolboxCleaner


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
    def unify_unknown(morpheme_tier):
        return re.sub('xxx?|www', '???', morpheme_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        for cleaning_method in [
                cls.remove_morph_tier_punctuation, cls.unify_unknown]:
            morph_tier = cleaning_method(morph_tier)
        return morph_tier

    @staticmethod
    def infer_pos(pos):
        """Infer POS from the gloss.

        There is no POS tier in Indonesian, but the macro categories
        `sfx`, `pfx`, `stem` can be inferred from the gloss.
        """
        if pos.startswith('-'):
            return 'sfx'
        elif pos.endswith('-'):
            return 'pfx'
        elif pos in ['', '???']:
            return pos
        else:
            return 'stem'

    @classmethod
    def clean_pos_raw(cls, pos):
        return cls.infer_pos(pos)
