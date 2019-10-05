from acqdiv.parsers.corpora.main.russian.reader import RussianReader
from acqdiv.parsers.corpora.main.russian.cleaner import RussianCleaner
from acqdiv.parsers.toolbox.parser import ToolboxParser
from acqdiv.parsers.metadata.imdi_parser import IMDIParser
from acqdiv.parsers.corpora.main.russian.imdi_cleaner \
    import RussianIMDICleaner as ICl
from acqdiv.parsers.toolbox.readers.age_updater import ToolboxAgeUpdater
from acqdiv.parsers.corpora.main.russian import tc_cleaner
from acqdiv.model.speaker import Speaker
from acqdiv.util.role import RoleMapper
from acqdiv.util.path import get_full_path


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

    def parse(self):
        session = super().parse()
        tc_cleaner.clean(session)
        return session

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
