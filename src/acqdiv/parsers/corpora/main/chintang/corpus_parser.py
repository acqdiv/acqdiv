from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.chintang.session_parser \
    import ChintangSessionParser


class ChintangCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):

        temp = session_path.replace(
            self.cfg['sessions_dir'],
            self.cfg['metadata_dir'])

        metadata_path = temp.replace('.txt', '.imdi')

        return ChintangSessionParser(session_path, metadata_path)
