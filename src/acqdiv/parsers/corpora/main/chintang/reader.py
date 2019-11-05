import re

from acqdiv.parsers.toolbox.readers.reader import ToolboxReader


class ChintangReader(ToolboxReader):

    @classmethod
    def get_actual_utterance(cls, rec):
        return rec.get('gw', '')

    @classmethod
    def get_seg_tier(cls, rec):
        return rec.get('mph', '')

    @classmethod
    def get_gloss_tier(cls, rec):
        return rec.get('mgl', '')

    @classmethod
    def get_pos_tier(cls, rec):
        return rec.get('ps', '')

    @classmethod
    def get_lang_tier(cls, rec):
        return rec.get('lg', '')

    @classmethod
    def get_id_tier(cls, rec):
        return rec.get('id', '')

    @classmethod
    def get_childdirected(cls, rec):
        for tier in ['TOS', 'tos']:
            if tier in rec:
                tos_raw = rec[tier]
                if 'directed' in tos_raw:
                    if 'child' in tos_raw:
                        return True
                    else:
                        return False

        return None

    @classmethod
    def get_sentence_type(cls, rec):
        # https://github.com/uzling/acqdiv/issues/253
        # \eng: . = default, ? = question, ! = exclamation
        # \nep: । = default, rest identical.
        # Note this is not a "pipe" but the so-called danda at U+0964
        if 'nep' in rec and rec['nep']:
            match_punctuation = re.search('([।?!])$', rec['nep'])
            if match_punctuation is not None:
                sentence_type = None
                if match_punctuation.group(1) == '।':
                    sentence_type = 'default'
                if match_punctuation.group(1) == '?':
                    sentence_type = 'question'
                if match_punctuation.group(1) == '!':
                    sentence_type = 'exclamation'
                return sentence_type
        elif cls.get_translation(rec):
            match_punctuation = re.search('([।?!])$',
                                          cls.get_translation(rec))
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
