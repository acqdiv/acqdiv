from acqdiv.parsers.corpora.main.russian.RussianReader import RussianReader
from acqdiv.parsers.corpora.main.russian.RussianCleaner import RussianCleaner
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser
from acqdiv.parsers.metadata.IMDIParser import IMDIParser
from acqdiv.parsers.corpora.main.russian.RussianIMDICleaner \
    import RussianIMDICleaner as ICl
from acqdiv.parsers.toolbox.readers.ToolboxAgeUpdater import ToolboxAgeUpdater
from acqdiv.model.Speaker import Speaker
from acqdiv.util.RoleMapper import RoleMapper
from acqdiv.util.util import get_full_path


class RussianSessionParser(ToolboxParser):

    role_mapper = RoleMapper(get_full_path(
        'parsers/corpora/main/russian/resources/speaker_label2macro_role.csv'
    ))

    def get_record_reader(self):
        return RussianReader()

    def get_metadata_reader(self):
        return IMDIParser(self.metadata_path)

    def get_cleaner(self):
        return RussianCleaner()

    def add_speakers(self):
        for speaker_dict in self.metadata_reader.metadata['participants']:
            speaker = Speaker()
            speaker.birth_date = ICl.clean_date(
                speaker_dict.get('birthdate', ''))
            speaker.code = ICl.clean_label(speaker_dict.get('code', ''))
            speaker.role_raw = speaker_dict.get('familysocialrole', '')
            speaker.name = ICl.clean_name(speaker_dict.get('name', ''))
            speaker.languages_spoken = speaker_dict.get('language', '')

            speaker.age_raw = speaker_dict.get('age', '')
            ToolboxAgeUpdater.update(speaker, self.session.date)

            speaker.role_raw = speaker_dict.get('familysocialrole', '')
            speaker.role = self.role_mapper.role_raw2role(speaker.role_raw)
            speaker.macro_role = self.role_mapper.infer_macro_role(
                speaker.role_raw, speaker.age_in_days, speaker.code)

            speaker.gender_raw = speaker_dict.get('sex', '')
            speaker.gender = ICl.clean_gender(speaker.gender_raw)
            if not speaker.gender:
                speaker.gender = self.role_mapper.role_raw2gender(
                    speaker.role_raw)

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
