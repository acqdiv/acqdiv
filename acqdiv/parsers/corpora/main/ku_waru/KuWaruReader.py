import re

from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader


class KuWaruReader(ToolboxReader):

    @classmethod
    def get_speaker_label(cls, rec):
        return rec.get('ELANParticipant', '')

    @classmethod
    def get_actual_utterance(cls, rec):
        return rec.get('tx', '')

    @classmethod
    def get_sentence_type(cls, rec):
        utterance = cls.get_actual_utterance(rec)

        if utterance.endswith('?'):
            return 'question'
        else:
            return 'default'

    @classmethod
    def get_seg_tier(cls, rec):
        return rec.get('mb', '')

    @classmethod
    def get_gloss_tier(cls, rec):
        return rec.get('ge', '')

    @classmethod
    def get_pos_tier(cls, rec):
        return rec.get('ps', '')

    @classmethod
    def get_translation(cls, rec):
        return rec.get('ft', '')

    @classmethod
    def get_lang_tier(cls, rec):
        return cls.get_pos_tier(rec)

    @classmethod
    def get_langs(cls, morpheme_lang_word):
        langs = []
        for lang in cls.get_poses(morpheme_lang_word):
            if '(TP)' in lang:
                langs.append('Tok Pisin')
            else:
                langs.append('Ku Waru')

        return langs
