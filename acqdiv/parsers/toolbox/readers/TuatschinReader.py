import re

from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader


class TuatschinReader(ToolboxReader):

    @classmethod
    def get_source_id(cls, rec_dict):
        return rec_dict.get('ref', 'u_id')

    @classmethod
    def get_utterance_raw(cls, rec_dict):
        return rec_dict.get('token', '')

    @classmethod
    def get_sentence_type(cls, rec_dict):
        """Get sentence type.

        There are only explicit question (?) and exclamation (!) markers. If
        they are missing, declarative (default) sentence type is assumed.
        """
        utterance = cls.get_utterance_raw(rec_dict)
        # remove the typical trailing whitespaces
        utterance = utterance.rstrip()
        if utterance.endswith('?'):
            return 'question'
        elif utterance.endswith('!'):
            return 'exclamation'
        else:
            return 'default'

    @classmethod
    def get_translation(cls, rec_dict):
        """Get translation.

        There is no free english translation, only a lemmatized translation
        is available.
        """
        return rec_dict.get('lemma_en', '')

    @classmethod
    def get_comment(cls, rec_dict):
        return rec_dict.get('com', '')

    @classmethod
    def get_seg_tier(cls, rec_dict):
        """Get segment tier.

        No segment, but only lemmas are available.
        """
        return rec_dict.get('lemma', '')

    @classmethod
    def get_gloss_tier(cls, rec_dict):
        """Get the gloss tier.

        Only morphsyntactical glosses (no lexical glosses) are available.
        """
        return rec_dict.get('morphosyn', '')

    @classmethod
    def get_pos_tier(cls, rec_dict):
        return rec_dict.get('pos', '')

    @classmethod
    def get_morphemes(cls, morpheme_word):
        """Get morphemes.

        There is no segmentation of words into morphemes.
        """
        return [morpheme_word]

    @classmethod
    def remove_pos_punctuation(cls, pos_tier):
        """Remove POS tag 'PUNCT' in POS tier."""
        pos_tier = pos_tier.replace('PUNCT', '')
        return cls.remove_redundant_whitespaces(pos_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        return cls.remove_pos_punctuation(pos_tier)

    @classmethod
    def remove_punctuation_utterance(cls, utterance):
        """Remove '...' or '....' in utterances."""
        utterance = re.sub(r'[.?!,]', '', utterance)
        return cls.remove_redundant_whitespaces(utterance)

    @classmethod
    def clean_utterance(cls, utterance):
        return cls.remove_punctuation_utterance(utterance)

    @classmethod
    def remove_dot_repetitions_seg_tier(cls, seg_tier):
        """Remove '. . .' or '. . . .' in segment tier."""
        seg_tier = re.sub(r'\. \. \.( \.)?', '', seg_tier)
        return cls.remove_redundant_whitespaces(seg_tier)

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        return cls.remove_dot_repetitions_seg_tier(seg_tier)
