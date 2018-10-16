from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader


class QuaqetReader(ToolboxReader):

    @classmethod
    def get_addressee(cls, rec_dict):
        return rec_dict.get('add', '')

    @classmethod
    def get_utterance_raw(cls, rec_dict):
        return cls.get_actual_utterance(rec_dict)

    @classmethod
    def get_actual_utterance(cls, rec_dict):
        return rec_dict.get('tx', '')

    @classmethod
    def get_target_utterance(cls, rec_dict):
        return rec_dict.get('trs-i', '')

    @classmethod
    def get_words_data(cls, rec_dict):
        result = []
        actual_utterance = cls.clean_utterance(cls.get_utterance_raw(rec_dict))
        target_utterance = cls.clean_utterance(
            cls.get_target_utterance(rec_dict))

        actual_words = cls.get_words(actual_utterance)
        target_words = cls.get_words(target_utterance)

        if len(actual_words) != len(target_words):
            target_words = len(actual_words)*['']

        for actual, target in zip(actual_words, target_words):
            actual_clean = cls.clean_word(actual)
            target_clean = cls.clean_word(target)

            d = {
                'word': actual_clean,
                'word_actual': actual_clean,
                'word_target': target_clean if target_clean else None
            }
            result.append(d)
        return result

    @classmethod
    def get_translation(cls, rec_dict):
        return rec_dict.get('ft', '')

    @classmethod
    def get_comment(cls, rec_dict):
        return rec_dict.get('nt', '')

    @classmethod
    def get_sentence_type(cls, rec_dict):
        """Get sentence type.

        Usually, there are no terminators in the transcriptions. In this case,
        the default value used. Only questions are explicitly marked,
        exclamations not.
        """
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
    def get_lang_tier(cls, rec_dict):
        return rec_dict.get('lg', '')