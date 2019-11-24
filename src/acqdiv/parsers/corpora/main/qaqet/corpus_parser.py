from pathlib import Path

from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.qaqet.session_parser \
    import QaqetSessionParser


class QaqetCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        metadata_filename = Path(session_path).stem[:-2] + '.imdi'
        metadata_filepath = Path(self.cfg['metadata_dir']) / metadata_filename

        return QaqetSessionParser(session_path, str(metadata_filepath))
