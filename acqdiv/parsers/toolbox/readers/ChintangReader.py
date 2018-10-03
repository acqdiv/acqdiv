import re

from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader


class ChintangReader(ToolboxReader):

    language = 'Chintang'

    @classmethod
    def get_utterance_raw(cls, rec_dict):
        return rec_dict.get('gw', '')

    @classmethod
    def get_seg_tier(cls, rec_dict):
        return rec_dict.get('mph', '')

    @classmethod
    def get_gloss_tier(cls, rec_dict):
        return rec_dict.get('mgl', '')

    @classmethod
    def get_pos_tier(cls, rec_dict):
        return rec_dict.get('ps', '')

    @classmethod
    def get_lang_tier(cls, rec_dict):
        return rec_dict.get('lg', '')

    @classmethod
    def get_childdirected(cls, rec_dict):
        for tier in ['TOS', 'tos']:
            if tier in rec_dict:
                tos_raw = rec_dict[tier]
                if 'directed' in tos_raw:
                    if 'child' in tos_raw:
                        return True
                    else:
                        return False

        return None

    @classmethod
    def get_id_tier(cls, rec_dict):
        return rec_dict.get('id', '')

    @classmethod
    def get_utterance(cls, rec_dict):
        """Get utterance with lemma IDs."""
        utterance = super().get_utterance(rec_dict)
        lemma_id = cls.get_id_tier(rec_dict)
        utterance['lemma_id'] = lemma_id
        return utterance

    @classmethod
    def get_sentence_type(cls, rec_dict):
        # https://github.com/uzling/acqdiv/issues/253
        # \eng: . = default, ? = question, ! = exclamation
        # \nep: । = default, rest identical.
        # Note this is not a "pipe" but the so-called danda at U+0964
        if 'nep' in rec_dict.keys() and rec_dict['nep']:
            match_punctuation = re.search('([।?!])$', rec_dict['nep'])
            if match_punctuation is not None:
                sentence_type = None
                if match_punctuation.group(1) == '।':
                    sentence_type = 'default'
                if match_punctuation.group(1) == '?':
                    sentence_type = 'question'
                if match_punctuation.group(1) == '!':
                    sentence_type = 'exclamation'
                return sentence_type
        elif 'eng' in rec_dict and rec_dict['translation']:
            match_punctuation = re.search('([।?!])$',
                                          rec_dict['translation'])
            if match_punctuation is not None:
                sentence_type = None
                if match_punctuation.group(1) == '.':
                    sentence_type = 'default'
                if match_punctuation.group(1) == '?':
                    sentence_type = 'question'
                if match_punctuation.group(1) == '!':
                    sentence_type = 'exclamation'
                return sentence_type
        else:
            return ''

    @staticmethod
    def remove_punctuation(seg_tier):
        return re.sub('[‘’\'“”\".!,:?+/]', '', seg_tier)

    @staticmethod
    def unify_unknown(seg_tier):
        return re.sub('\*\*\*', '???', seg_tier)

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        for cleaning_method in [cls.remove_punctuation, cls.unify_unknown]:
            seg_tier = cleaning_method(seg_tier)

        return seg_tier

    @staticmethod
    def remove_floating_clitic(morpheme_word):
        # TODO: double check this logic is correct with Robert
        return morpheme_word.replace(" - ", " ")

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        return cls.remove_floating_clitic(morpheme_word)

    def clean_lang(self, lang):
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
            return self.language