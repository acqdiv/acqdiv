from acqdiv.parsers.corpora.main.russian.RussianReader import RussianReader
from acqdiv.parsers.corpora.main.russian.RussianCleaner import RussianCleaner
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser
from acqdiv.parsers.metadata.IMDIParser import IMDIParser
from acqdiv.model.Speaker import Speaker


class RussianSessionParser(ToolboxParser):

    def get_record_reader(self):
        return RussianReader()

    def get_metadata_reader(self):
        return IMDIParser(self.metadata_path)

    def get_cleaner(self):
        return RussianCleaner()

    def add_speakers(self):
        for speaker_dict in self.metadata_reader.metadata['participants']:
            speaker = Speaker()
            speaker.session = self.session
            speaker.birth_date = speaker_dict.get('birthdate', None)
            speaker.gender_raw = speaker_dict.get('sex', None)
            speaker.code = speaker_dict.get('code', None)
            speaker.age_raw = speaker_dict.get('age', None)
            speaker.role_raw = speaker_dict.get('familysocialrole', None)
            speaker.name = speaker_dict.get('name', None)
            speaker.languages_spoken = speaker_dict.get('language', None)

            self.session.speakers.append(speaker)
