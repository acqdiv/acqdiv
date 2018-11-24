from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader


class DeneReader(ToolboxReader):

    @classmethod
    def get_utterance_raw(cls, rec_dict):
        return rec_dict.get('full', '')

    @classmethod
    def get_seg_tier(cls, rec_dict):
        return rec_dict.get('seg', '')

    @classmethod
    def get_gloss_tier(cls, rec_dict):
        return rec_dict.get('glo', '')

    @classmethod
    def get_sentence_type(cls, rec_dict):
        utt = rec_dict.get('full_orig')
        if utt.endswith('?'):
            return 'question'
        else:
            return 'default'

    @classmethod
    def unify_unknown(cls, utterance):
        return utterance.replace('xxx', '???')
