import re

from acqdiv.parsers.toolbox.cleaners.cleaner import ToolboxCleaner
from acqdiv.parsers.corpora.main.russian.gloss_mapper \
    import RussianGlossMapper
from acqdiv.parsers.corpora.main.russian.pos_mapper \
    import RussianPOSMapper


class RussianCleaner(ToolboxCleaner):

    @classmethod
    def remove_punctuation(cls, utterance):
        utterance = re.sub(
            '[‘’\'“”\".!,:+/]+|(&lt; )|(?<=\\s)\?(?=\\s|$)', '', utterance)
        return cls.remove_redundant_whitespaces(utterance)

    @classmethod
    def remove_dashes(cls, utterance):
        return re.sub('\\s-\\s', ' ', utterance)

    @classmethod
    def remove_insecure_transcription_markers(cls, utterance):
        """Remove insecure transcription markers.

        Insecure transcription markers: [?], [=( )?], [xxx].
        Note that [xxx] usually replaces a complete utterance and is
        non-aligned, in contrast to xxx without brackets, which can be
        counted as a word.
        """
        # TODO: Get warnings on utterance level
        if re.search('\[(\s*=?.*?|\s*xxx\s*)\]', utterance):
            utterance = re.sub('\[\s*=?.*?\]', '', utterance)
            return cls.remove_redundant_whitespaces(utterance)

        return utterance

    @classmethod
    def remove_equal_signs(cls, utterance):
        utterance = utterance.replace('=', '')
        return cls.remove_redundant_whitespaces(utterance)

    @classmethod
    def clean_utterance(cls, utterance):
        for cleaning_method in [
                super().clean_utterance, cls.remove_punctuation,
                cls.remove_dashes, cls.remove_insecure_transcription_markers,
                cls.remove_equal_signs]:
            utterance = cleaning_method(utterance)

        return utterance

    @staticmethod
    def remove_seg_punctuation(seg_tier):
        return re.sub('[‘’\'“”\".!,:\-?+/]', '', seg_tier)

    @staticmethod
    def unify_unknown(seg_tier):
        return re.sub('xxx?|www', '???', seg_tier)

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        for cleaning_method in [cls.remove_seg_punctuation, cls.unify_unknown]:
            seg_tier = cleaning_method(seg_tier)

        return seg_tier

    @staticmethod
    def clean_gloss_pos_punctuation(gloss_pos_tier):
        return gloss_pos_tier.replace('PUNCT', '').replace('ANNOT', '').\
            replace('<NA: lt;> ', '')

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        return cls.clean_gloss_pos_punctuation(gloss_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        return cls.clean_gloss_pos_punctuation(pos_tier)

    @classmethod
    def clean_lang_tier(cls, lang_tier):
        return cls.clean_gloss_pos_punctuation(lang_tier)

    @classmethod
    def clean_gloss(cls, gloss):
        return RussianGlossMapper.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return RussianPOSMapper.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return RussianPOSMapper.map(pos_ud, ud=True)
