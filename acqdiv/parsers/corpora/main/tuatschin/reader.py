from acqdiv.parsers.toolbox.readers.reader import ToolboxReader


class TuatschinReader(ToolboxReader):

    @staticmethod
    def get_rec_separator():
        return br'\\u_id'

    @classmethod
    def get_source_id(cls, rec):
        return rec.get('u_id')

    @classmethod
    def get_actual_utterance(cls, rec):
        """Get the raw utterance.

        \token is the normalized/tokenized tier of \text which is the very
        original transcription. \token is taken as the raw utterance.
        """
        return rec.get('token', '')

    @classmethod
    def get_sentence_type(cls, rec):
        """Get sentence type.

        There are only explicit question ('?'), exclamation ('!') and trail
        off ('. . .') markers. If they are missing, declarative (default)
        sentence type is assumed.
        """
        utterance = cls.get_actual_utterance(rec)
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
    def get_translation(cls, rec):
        """Get translation.

        There is no free english translation, only a lemmatized translation
        is available.
        """
        return rec.get('lemma_en', '')

    @classmethod
    def get_comment(cls, rec):
        return rec.get('com', '')

    @classmethod
    def get_seg_tier(cls, rec):
        """Get segment tier.

        No segment, but only lemmas are available.
        """
        return rec.get('lemma', '')

    @classmethod
    def get_gloss_tier(cls, rec):
        """Get the gloss tier.

        Only morphsyntactical glosses (no lexical glosses) are available.
        """
        return rec.get('morphosyn', '')

    @classmethod
    def get_pos_tier(cls, rec):
        return rec.get('pos', '')

    @classmethod
    def get_morphemes(cls, morpheme_word):
        """Get morphemes.

        There is no segmentation of words into morphemes.
        """
        return [morpheme_word]

    @staticmethod
    def get_morpheme_type():
        return 'actual'
