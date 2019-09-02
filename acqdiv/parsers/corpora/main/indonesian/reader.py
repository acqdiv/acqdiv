import re

from acqdiv.parsers.toolbox.readers.reader import ToolboxReader


class IndonesianReader(ToolboxReader):

    @classmethod
    def get_source_id(cls, rec):
        return rec.get('id', '')

    @classmethod
    def get_speaker_label(cls, rec):
        return rec.get('sp', '')

    @classmethod
    def get_start_raw(cls, rec):
        return rec.get('begin', '')

    @classmethod
    def get_actual_utterance(cls, rec):
        return rec.get('tx', '')

    @classmethod
    def get_translation(cls, rec):
        return rec.get('ft', '')

    @classmethod
    def get_comment(cls, rec):
        return rec.get('nt', '')

    @classmethod
    def get_seg_tier(cls, rec):
        return rec.get('mb', '')

    @classmethod
    def get_gloss_tier(cls, rec):
        return rec.get('ge', '')

    @classmethod
    def get_pos_tier(cls, rec):
        """Get the POS tier.

        There is no POS tier in Indonesian, but the macro categories
        `sfx`, `pfx`, `stem` for the morpheme can be inferred from the gloss.
        """
        return cls.get_gloss_tier(rec)

    @classmethod
    def is_record(cls, rec):
        if not super().is_record(rec):
            return False

        speaker_label = cls.get_speaker_label(rec)

        if speaker_label == '@PAR':
            return False

        if speaker_label == 'AUX':
            return False

        return True

    @classmethod
    def get_sentence_type(cls, rec):
        utterance_raw = cls.get_actual_utterance(rec)
        if re.search('\.', utterance_raw):
            return 'default'
        elif re.search('\?\s*$', utterance_raw):
            return 'question'
        elif re.search('!', utterance_raw):
            return 'imperative'
        else:
            return ''

    @classmethod
    def get_lang_tier(cls, rec):
        return cls.get_gloss_tier(rec)

    @classmethod
    def get_langs(cls, morpheme_lang_word):
        return ['Indonesian' for _ in cls.get_morphemes(morpheme_lang_word)]