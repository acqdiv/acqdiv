from pathlib import Path

from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.ku_waru.session_parser \
    import KuWaruSessionParser


class KuWaruCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        metadata_filename = Path(session_path).with_suffix('.imdi').name
        metadata_filepath = Path(self.cfg['metadata_dir']) / metadata_filename

        return KuWaruSessionParser(session_path, str(metadata_filepath))
