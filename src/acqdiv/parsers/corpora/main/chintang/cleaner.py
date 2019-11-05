import re

from acqdiv.parsers.toolbox.cleaners.cleaner import ToolboxCleaner
from acqdiv.parsers.toolbox.cleaners.morpheme_cleaner \
    import ToolboxMorphemeCleaner
from acqdiv.parsers.corpora.main.chintang.gloss_mapper \
    import ChintangGlossMapper
from acqdiv.parsers.corpora.main.chintang.pos_mapper \
    import ChintangPOSMapper


class ChintangCleaner(ToolboxCleaner):

    @staticmethod
    def remove_punctuation(seg_tier):
        return re.sub('[‘’\'“”\".!,:?+/]', '', seg_tier)

    @staticmethod
    def unify_unknown_seg_tier(seg_tier):
        return re.sub('\*\*\*', '???', seg_tier)

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        for cleaning_method in [
            cls.remove_punctuation,
            cls.unify_unknown_seg_tier
        ]:
            seg_tier = cleaning_method(seg_tier)

        return seg_tier

    @staticmethod
    def remove_floating_clitic(morpheme_word):
        # TODO: double check this logic is correct with Robert
        return morpheme_word.replace(" - ", " ")

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        return cls.remove_floating_clitic(morpheme_word)

    @classmethod
    def clean_lang(cls, lang):
        languages = {
            'C': 'Chintang',
            'N': 'Nepali',
            'E': 'English',
            'C/N': 'Nepali',
            'N/E': 'Nepali',
            'C/N/E': 'English',
            'B': 'Bantawa',
            'C/B': 'Chintang/Bantawa',
            'C(M)': 'Chintang',
            'C(S)': 'Chintang',
            'C/E': 'English',
            'C/E/N': 'English',
            'C/N/H': 'Hindi',
            'C+N': 'Chintang/Nepali',
            'H': 'Hindi',
            'N/Arabic': 'Arabic',
            'N/H': 'Hindi',
            '***': 'Chintang'
        }

        lang = lang.strip('-')
        if lang in languages:
            return languages[lang]
        else:
            return 'Chintang'

    @staticmethod
    def unify_unknown_morpheme(id_):
        return id_.replace('***', '???')

    @classmethod
    def clean_id(cls, id_):
        id_ = ToolboxMorphemeCleaner.remove_morpheme_delimiters(id_)
        id_ = cls.unify_unknown_morpheme(id_)

        return id_

    @classmethod
    def clean_gloss(cls, gloss):
        return ChintangGlossMapper.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return ChintangPOSMapper.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return ChintangPOSMapper.map(pos_ud, ud=True)
