import re

from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader


class TuatschinReader(ToolboxReader):

    language = 'Tuatschin'

    @staticmethod
    def get_record_marker():
        return br'\\u_id'

    @classmethod
    def get_source_id(cls, rec_dict):
        return rec_dict.get('u_id')

    @classmethod
    def get_utterance_raw(cls, rec_dict):
        """Get the raw utterance.

        \token is the normalized/tokenized tier of \text which is the very
        original transcription. \token is taken as the raw utterance.
        """
        return rec_dict.get('token', '')

    @classmethod
    def get_sentence_type(cls, rec_dict):
        """Get sentence type.

        There are only explicit question ('?'), exclamation ('!') and trail
        off ('. . .') markers. If they are missing, declarative (default)
        sentence type is assumed.
        """
        utterance = cls.get_utterance_raw(rec_dict)
        # remove the typical trailing whitespaces
        utterance = utterance.rstrip()
        if utterance.endswith('?'):
            return 'question'
        elif utterance.endswith('!'):
            return 'exclamation'
        elif utterance.endswith('. . .'):
            return 'trail off'
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
    def remove_punctuation_utterance(cls, utterance):
        """Remove punctuation in the utterance.

        Utterances can contain the following punctuation: '?', '!', ',' and
        dot repetitions '. . .'.
        """
        utterance = re.sub(r'[.?!,]', '', utterance)
        return cls.remove_redundant_whitespaces(utterance)

    @staticmethod
    def unify_unknown_utterance(pos_tier):
        """Unify unknowns in the utterance.

        'xxx' stands for incomprehensible forms and is standardized to '???'.
        """
        return pos_tier.replace('xxx', '???')

    @classmethod
    def clean_utterance(cls, utterance):
        utterance = cls.remove_punctuation_utterance(utterance)
        utterance = cls.unify_unknown_utterance(utterance)
        return utterance

    # ---------- cross cleaners ----------

    @classmethod
    def unify_unknown_gloss_tier(cls, gloss_tier, seg_tier):
        """Unify unknowns on the gloss tier.

        Annotated with 'inv'. Since 'inv' (=invariable forms) is also used
        in other cases (such as ADP, ADV, etc.), the segment tier has to be
        used for inference.

        Returns:
            str: The cleaned gloss tier.
        """
        gloss_words = cls.get_gloss_words(gloss_tier)
        seg_words = cls.get_seg_words(seg_tier)

        if len(gloss_words) == len(seg_words):
            for i, seg_word in enumerate(seg_words):
                if seg_word == 'XXX':
                    gloss_words[i] = '???'

            return ' '.join(gloss_words)

        return gloss_tier

    @classmethod
    def remove_punct_inv(cls, gloss_tier, pos_tier):
        """Remove punctuation inv's on the gloss tier.

        Punctuation receives on the gloss tier the 'inv' value. Since
        'inv' (=invariable forms) is also used in other cases
        (such as ADP, ADV, etc.), the POS tier has to be used for inference.

        Returns:
            str: The cleaned gloss tier.
        """
        gloss_words = cls.get_gloss_words(gloss_tier)
        pos_words = cls.get_pos_words(pos_tier)

        if len(gloss_words) == len(pos_words):
            for i, pos_word in enumerate(pos_words):
                if pos_word == 'PUNCT':
                    gloss_words[i] = ''

            return ' '.join((w for w in gloss_words if w))

        return gloss_tier

    @classmethod
    def cross_clean(cls, rec_dict):
        gloss_tier = cls.get_gloss_tier(rec_dict)
        seg_tier = cls.get_seg_tier(rec_dict)
        pos_tier = cls.get_pos_tier(rec_dict)
        gloss_tier = cls.remove_punct_inv(gloss_tier, pos_tier)
        gloss_tier = cls.unify_unknown_gloss_tier(gloss_tier, seg_tier)
        rec_dict['morphosyn'] = gloss_tier

        return rec_dict

    # ---------- seg tier cleaners ----------

    @staticmethod
    def unify_unknown_seg_tier(seg_tier):
        """Unify unknowns on the segment tier.

        'XXX' stands for unknown/incomprehensible forms and is standardized
        to '???'.
        """
        return seg_tier.replace('XXX', '???')

    @classmethod
    def remove_dot_repetitions_seg_tier(cls, seg_tier):
        """Remove trail offs on the segment tier.

        Trail offs are marked with dot repetitions (3 or 4 times).
        """
        seg_tier = re.sub(r'\. \. \.( \.)?', '', seg_tier)
        return cls.remove_redundant_whitespaces(seg_tier)

    @classmethod
    def remove_punctuation_seg_tier(cls, seg_tier):
        """Remove punctuation on the segment tier.

        The segment tier can contain the following punctuation: '?', '!', ','.
        """
        utterance = re.sub(r'[?!,]', '', seg_tier)
        return cls.remove_redundant_whitespaces(utterance)

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        for cleaning_method in [
                cls.remove_dot_repetitions_seg_tier,
                cls.remove_punctuation_seg_tier,
                cls.unify_unknown_seg_tier]:
            seg_tier = cleaning_method(seg_tier)

        return seg_tier

    # ---------- POS tier cleaners ----------

    @classmethod
    def remove_punct_pos_tier(cls, pos_tier):
        """Remove PUNCT on the POS tier.

        Punctuation receives the POS tag 'PUNCT'.
        """
        pos_tier = pos_tier.replace('PUNCT', '')
        return cls.remove_redundant_whitespaces(pos_tier)

    @staticmethod
    def unify_unknown_pos_tier(pos_tier):
        """Unify unknowns on the POS tier.

        `X` stands either for child words that have an unclear POS tag or
        incomprehensible/unknown forms (see XXX on the segment tier) and is
        standardized to '???'. Sometimes, specifications (such as `_Chld`) are
        suffixed to `X`.
        """
        rgx = re.compile(r'\bX(_\S+)?\b')
        return rgx.sub('???', pos_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        for cleaning_method in [
                cls.remove_punct_pos_tier,
                cls.unify_unknown_pos_tier]:
            pos_tier = cleaning_method(pos_tier)

        return pos_tier

    # ---------- POS tag cleaners ----------

    @classmethod
    def clean_pos(cls, pos):
        for cleaning_method in [
                cls.remove_specifications
        ]:
            pos = cleaning_method(pos)
        return pos

    @staticmethod
    def remove_specifications(pos):
        """Remove specifications of POS tags.

        Specifications start with `_`.

        Examples:
        - words erroneously written apart: _cont
        - child forms: _Chld
        - discourse particles: _Discpart
        ...
        """
        regex = re.compile(r'_[^_]+')
        pos = regex.sub('', pos)
        return pos
