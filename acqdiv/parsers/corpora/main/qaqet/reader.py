from acqdiv.parsers.toolbox.readers.reader import ToolboxReader


class QaqetReader(ToolboxReader):

    @classmethod
    def get_addressee(cls, rec):
        add = rec.get('addr', '')

        if add == 'unknown':
            return ''

        return add

    @classmethod
    def get_actual_utterance(cls, rec):
        return rec.get('tx', '')

    @classmethod
    def get_target_utterance(cls, rec_dict):
        return rec_dict.get('trs-i', '')

    @classmethod
    def get_translation(cls, rec):
        return rec.get('ft', '')

    @classmethod
    def get_comment(cls, rec):
        return rec.get('nt', '')

    @classmethod
    def get_sentence_type(cls, rec):
        """Get sentence type.

        Usually, there are no terminators in the transcriptions. In this case,
        the default value used. Only questions are explicitly marked,
        exclamations not.
        """
        utterance = cls.get_actual_utterance(rec)
        if utterance.endswith('?'):
            return 'question'
        else:
            return 'default'

    @staticmethod
    def get_morpheme_type():
        return 'actual'
