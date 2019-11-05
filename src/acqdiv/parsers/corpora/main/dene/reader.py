from acqdiv.parsers.toolbox.readers.reader import ToolboxReader


class DeneReader(ToolboxReader):

    @classmethod
    def get_actual_utterance(cls, rec):
        return rec.get('full', '')

    @classmethod
    def get_seg_tier(cls, rec):
        return rec.get('seg', '')

    @classmethod
    def get_gloss_tier(cls, rec):
        return rec.get('glo', '')

    @classmethod
    def get_sentence_type(cls, rec):
        utt = rec.get('full_orig')
        if utt.endswith('?'):
            return 'question'
        else:
            return 'default'

    @classmethod
    def get_translation(cls, rec):
        return rec.get('eng_u', '')

    @classmethod
    def get_comment(cls, rec):
        return rec.get('com', '')
