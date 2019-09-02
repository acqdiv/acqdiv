from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.qaqet.session_parser \
    import QaqetSessionParser


class QaqetCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        temp = session_path.replace(self.cfg['paths']['sessions_dir'],
                                    self.cfg['paths']['metadata_dir'])

        # remove the session number '_\d'
        metadata_path = temp[:-6] + '.imdi'

        return QaqetSessionParser(session_path, metadata_path)
