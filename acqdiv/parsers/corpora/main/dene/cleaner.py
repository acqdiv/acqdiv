from acqdiv.parsers.toolbox.cleaners.cleaner import ToolboxCleaner


class DeneCleaner(ToolboxCleaner):

    @classmethod
    def unify_unknown(cls, utterance):
        return utterance.replace('xxx', '???')
