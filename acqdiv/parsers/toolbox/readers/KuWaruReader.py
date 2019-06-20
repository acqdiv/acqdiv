import re

from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader


class KuWaruReader(ToolboxReader):

    language = 'Ku Waru'

    @classmethod
    def get_speaker_label(cls, rec_dict):
        return rec_dict.get('ELANParticipant', '')

    @classmethod
    def get_utterance_raw(cls, rec_dict):
        return rec_dict.get('tx', '')

    @classmethod
    def get_sentence_type(cls, rec_dict):
        utterance = cls.get_utterance_raw(rec_dict)

        if utterance.endswith('?'):
            return 'question'
        else:
            return 'default'

    @classmethod
    def get_seg_tier(cls, rec_dict):
        return rec_dict.get('mb', '')

    @classmethod
    def get_gloss_tier(cls, rec_dict):
        return rec_dict.get('ge', '')

    @classmethod
    def get_pos_tier(cls, rec_dict):
        return rec_dict.get('ps', '')

    @classmethod
    def get_translation(cls, rec_dict):
        return rec_dict.get('ft', '')

    @classmethod
    def get_lang_tier(cls, rec_dict):
        return cls.get_pos_tier(rec_dict)

    @classmethod
    def get_langs(cls, morpheme_lang_word):
        langs = []
        for lang in cls.get_poses(morpheme_lang_word):
            if '(TP)' in lang:
                langs.append('Tok Pisin')
            else:
                langs.append('Ku Waru')

        return langs

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
