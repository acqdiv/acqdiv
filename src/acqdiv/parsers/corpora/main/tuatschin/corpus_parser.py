from pathlib import Path

from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.tuatschin.session_parser \
    import TuatschinSessionParser


class TuatschinCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):
        metadata_filename = Path(session_path).with_suffix('.imdi').name
        metadata_filepath = Path(self.cfg['metadata_dir']) / metadata_filename

        # TODO: remove this check once we have all the metadata
        if metadata_filepath.is_file():
            return TuatschinSessionParser(session_path, str(metadata_filepath))

        return None
