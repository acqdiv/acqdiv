from acqdiv.parsers.corpus_parser import CorpusParser
from acqdiv.parsers.corpora.main.tuatschin.session_parser \
    import TuatschinSessionParser

import os


class TuatschinCorpusParser(CorpusParser):

    def get_session_parser(self, session_path):

        temp = session_path.replace(self.cfg['paths']['sessions_dir'],
                                    self.cfg['paths']['metadata_dir'])
        metadata_path = temp.replace('.tbt', '.imdi')

        # TODO: remove this check once we have all the metadata
        if os.path.isfile(metadata_path):
            return TuatschinSessionParser(session_path, metadata_path)

        return None
