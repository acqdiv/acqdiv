from acqdiv.parsers.corpora.main.tuatschin.reader \
    import TuatschinReader
from acqdiv.parsers.corpora.main.tuatschin.cleaner \
    import TuatschinCleaner
from acqdiv.parsers.metadata.cmdi_parser import CMDIParser
from acqdiv.parsers.toolbox.parser import ToolboxParser


class TuatschinSessionParser(ToolboxParser):

    def get_metadata_reader(self):
        return CMDIParser(self.metadata_path)

    def get_record_reader(self):
        return TuatschinReader()

    def get_cleaner(self):
        return TuatschinCleaner()

    def add_record(self, rec):
        super().add_record(rec)
        self.delete_morphemes()

    def delete_morphemes(self):
        utt = self.session.utterances[-1]
        utt.morpheme_raw = ''
        utt.gloss_raw = ''
        utt.pos_raw = ''
        utt.morphemes = []
