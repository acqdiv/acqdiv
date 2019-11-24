from pathlib import Path

from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.indonesian.session_parser \
    import IndonesianSessionParser


class IndonesianCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        metadata_filename = Path(session_path).with_suffix('.xml').name
        metadata_filepath = Path(self.cfg['metadata_dir']) / metadata_filename

        return IndonesianSessionParser(session_path, str(metadata_filepath))
