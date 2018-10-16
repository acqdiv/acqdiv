from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader

class QuaqetReader(ToolboxReader):

    @classmethod
    def get_addressee(cls, rec_dict):
        return rec_dict.get('add', '')

    @classmethod
    def get_utterance_raw(cls, rec_dict):
        return rec_dict('trs', '')

    @classmethod
    def get_actual_utterance(cls, rec_dict):
        return rec_dict.get('tx', '')

    @classmethod
    def get_target_utterance(cls, rec_dict):
        return rec_dict.get('trs-i', '')

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