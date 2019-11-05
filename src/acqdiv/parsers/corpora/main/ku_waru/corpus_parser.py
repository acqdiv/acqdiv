from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.ku_waru.session_parser \
    import KuWaruSessionParser


class KuWaruCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        temp = session_path.replace(self.cfg['paths']['sessions_dir'],
                                    self.cfg['paths']['metadata_dir'])
        metadata_path = temp.replace('.tbt', '.imdi')

        return KuWaruSessionParser(session_path, metadata_path)
