from acqdiv.parsers.corpora.main.russian.RussianReader import RussianReader
from acqdiv.parsers.corpora.main.russian.RussianCleaner import RussianCleaner
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser
from acqdiv.parsers.metadata.IMDIParser import IMDIParser
from acqdiv.parsers.toolbox.readers.ToolboxAgeUpdater import ToolboxAgeUpdater
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
            speaker.birth_date = speaker_dict.get('birthdate', '')
            speaker.gender_raw = speaker_dict.get('sex', '')
            speaker.code = speaker_dict.get('code', '')
            speaker.age_raw = speaker_dict.get('age', '')
            speaker.role_raw = speaker_dict.get('familysocialrole', '')
            speaker.name = speaker_dict.get('name', '')
            speaker.languages_spoken = speaker_dict.get('language', '')

            ToolboxAgeUpdater.update(speaker, self.session.date)

            self.session.speakers.append(speaker)

    def add_record(self, rec):
        super().add_record(rec)
        self.delete_morphemes()

    def delete_morphemes(self):
        utt = self.session.utterances[-1]
        utt.morpheme_raw = ''
        utt.gloss_raw = ''
        utt.pos_raw = ''
        utt.morphemes = []
