from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.ku_waru.KuWaruSessionParser \
    import KuWaruSessionParser


class KuWaruCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return KuWaruSessionParser(self.cfg, session_path)
