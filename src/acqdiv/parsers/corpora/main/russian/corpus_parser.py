from pathlib import Path

from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.russian.session_parser \
    import RussianSessionParser


class RussianCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        metadata_filename = Path(session_path).with_suffix('.imdi').name
        metadata_filepath = Path(self.cfg['metadata_dir']) / metadata_filename

        return RussianSessionParser(session_path, str(metadata_filepath))
