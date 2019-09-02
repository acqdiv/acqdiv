import re


class ToolboxReader(object):
    """Methods for reading Toolbox."""

    # ---------- record ----------

    @classmethod
    def is_record(cls, rec_dict):
        """Is the record really a record or just metadata?"""
        for tier in rec_dict:
            content = rec_dict[tier]

            if content.startswith('@'):
                return False

        return True

    @staticmethod
    def get_rec_separator():
        return br'\\ref'

    # ---------- tiers ----------

    @classmethod
    def get_source_id(cls, rec):
        return rec.get('ref', '')

    @classmethod
    def get_speaker_label(cls, rec):
        return rec.get('ELANParticipant', '')

    @classmethod
    def get_addressee(cls, rec):
        return rec.get('add', '')

    @classmethod
    def get_start_raw(cls, rec):
        return rec.get('ELANBegin', '')

    @classmethod
    def get_end_raw(cls, rec):
        return rec.get('ELANEnd', '')

    @classmethod
    def get_actual_utterance(cls, rec):
        return rec.get('tx', '')

    @classmethod
    def get_target_utterance(cls, rec):
        return rec.get('target', '')

    @classmethod
    def get_sentence_type(cls, rec):
        """Get utterance type (aka sentence type) of an utterance.

        Possible values:
            - default (.)
            - question (?)
            - imperative or exclamation (!)

        Args:
            rec (acqdiv.parsers.toolbox.model.record.Record): The record.

        Returns:
            str: The sentence type.
        """
        utterance_raw = cls.get_actual_utterance(rec)
        match_punctuation = re.search('([.?!])$', utterance_raw)
        if match_punctuation is not None:
            if match_punctuation.group(1) == '.':
                return 'default'
            elif match_punctuation.group(1) == '?':
                return 'question'
            elif match_punctuation.group(1) == '!':
                return 'imperative'

        return ''

    @classmethod
    def get_childdirected(cls, rec):
        """Not coded per default.

        Args:
            rec (acqdiv.parsers.toolbox.model.record.Record): The record.
        """
        return ''

    @classmethod
    def get_translation(cls, rec):
        return rec.get('eng', '')

    @classmethod
    def get_comment(cls, rec):
        return rec.get('comment', '')

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
    def get_lang_tier(cls, rec):
        return rec.get('lg', '')

    @classmethod
    def get_id_tier(cls, rec):
        return rec.get('lemma_id', '')

    # ---------- words ----------

    @classmethod
    def get_words(cls, utterance):
        return utterance.split()

    @classmethod
    def get_morpheme_words(cls, morpheme_tier):
        _word_boundary = re.compile(r'(?<![\-=\s])\s+(?![\-=\s])')

        if morpheme_tier:
            return re.split(_word_boundary, morpheme_tier)
        else:
            return []

    @classmethod
    def get_seg_words(cls, segment_tier):
        return cls.get_morpheme_words(segment_tier)

    @classmethod
    def get_gloss_words(cls, gloss_tier):
        return cls.get_morpheme_words(gloss_tier)

    @classmethod
    def get_pos_words(cls, pos_tier):
        return cls.get_morpheme_words(pos_tier)

    @classmethod
    def get_lang_words(cls, morpheme_lang_tier):
        return cls.get_morpheme_words(morpheme_lang_tier)

    @classmethod
    def get_id_words(cls, id_tier):
        return cls.get_morpheme_words(id_tier)

    # ---------- morphemes ----------

    @classmethod
    def get_morphemes(cls, morpheme_word):
        if morpheme_word:
            return morpheme_word.split()
        else:
            return []

    @classmethod
    def get_segs(cls, segment_word):
        return cls.get_morphemes(segment_word)

    @classmethod
    def get_glosses(cls, gloss_word):
        return cls.get_morphemes(gloss_word)

    @classmethod
    def get_poses(cls, pos_word):
        return cls.get_morphemes(pos_word)

    @classmethod
    def get_langs(cls, morpheme_lang_word):
        return cls.get_morphemes(morpheme_lang_word)

    @classmethod
    def get_ids(cls, id_word):
        return cls.get_morphemes(id_word)

    @staticmethod
    def get_morpheme_type():
        return 'target'

    @staticmethod
    def get_main_morpheme():
        return 'gloss'
