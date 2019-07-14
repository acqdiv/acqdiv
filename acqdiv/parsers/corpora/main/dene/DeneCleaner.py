from acqdiv.parsers.toolbox.cleaners.ToolboxCleaner import ToolboxCleaner


class DeneCleaner(ToolboxCleaner):

    @classmethod
    def unify_unknown(cls, utterance):
        return utterance.replace('xxx', '???')
