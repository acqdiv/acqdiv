from acqdiv.parsers.CorpusParser import CorpusParser
from acqdiv.parsers.corpora.main.inuktitut.InuktitutSessionParser \
    import InuktitutSessionParser


class InuktitutCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        return InuktitutSessionParser(session_path)
