import os
import re

from acqdiv.parsers.corpora.main.indonesian.reader import \
    IndonesianReader
from acqdiv.parsers.corpora.main.indonesian.cleaner \
    import IndonesianCleaner
from acqdiv.parsers.corpora.main.indonesian.label_corrector \
    import IndonesianSpeakerLabelCorrector as Lc
from acqdiv.parsers.corpora.main.indonesian.age_updater \
    import IndonesianAgeUpdater
from acqdiv.util.role import RoleMapper
from acqdiv.util.path import get_full_path
from acqdiv.parsers.metadata.chat_parser import CHATParser
from acqdiv.parsers.toolbox.parser import ToolboxParser
from acqdiv.model.speaker import Speaker
from acqdiv.model.word import Word


class IndonesianSessionParser(ToolboxParser):

    role_mapper = RoleMapper(get_full_path(
        'parsers/corpora/main/indonesian/resources/'
        'speaker_label2macro_role.csv'
    ))

    def get_metadata_reader(self):
        return CHATParser(self.metadata_path)

    def add_session_metadata(self):
        self.session.source_id = os.path.splitext(os.path.basename(
            self.toolbox_path))[0]
        metadata = self.metadata_reader.metadata['__attrs__']
        self.session.date = metadata.get('Date', None)

        return self.session

    def add_speakers(self):
        for speaker_dict in self.metadata_reader.metadata['participants']:
            speaker = Speaker()
            speaker.birth_date = speaker_dict.get('birthday', '')
            speaker.code = speaker_dict.get('id', '')
            speaker.name = speaker_dict.get('name', '')
            speaker.code = Lc.correct_speaker_label(speaker.code, speaker.name)
            speaker.languages_spoken = speaker_dict.get('language', '')

            speaker.age_raw = speaker_dict.get('age', '')
            IndonesianAgeUpdater.update(speaker, self.session.date)

            speaker.role_raw = speaker_dict.get('role', '')
            speaker.role = self.role_mapper.role_raw2role(speaker.role_raw)
            speaker.macro_role = self.role_mapper.infer_macro_role(
                speaker.role_raw, speaker.age_in_days, speaker.code)

            speaker.gender_raw = speaker_dict.get('sex', '')
            speaker.gender = speaker.gender_raw.title()
            if not speaker.gender:
                speaker.gender = self.role_mapper.role_raw2gender(
                    speaker.role_raw)

            if self.is_speaker(speaker):
                self.session.speakers.append(speaker)

    def add_utterance(self, rec):
        utt = super().add_utterance(rec)
        speaker_label = self.record_reader.get_speaker_label(rec)
        speaker_label = Lc.correct_rec_label(speaker_label)
        utt.speaker = self._get_speaker(speaker_label, self.session.speakers)

        return utt

    @staticmethod
    def is_speaker(speaker):
        """Check whether the speaker is a real speaker.

        Skip `AUX` participants.

        Args:
            speaker (Speaker): The `Speaker` instance.
        """
        return speaker.code != 'AUX'

    def get_record_reader(self):
        return IndonesianReader()

    def get_cleaner(self):
        return IndonesianCleaner()

    def add_words(self, actual_utterance, target_utterance):
        utt = self.session.utterances[-1]

        for word in self.record_reader.get_words(actual_utterance):
            w = Word()
            utt.words.append(w)

            w.word_language = ''

            # Distinguish between word and word_target;
            # otherwise the target word is identical to the actual word
            if re.search('\(', word):
                w.word_target = re.sub('[()]', '', word)
                w.word = re.sub('\([^)]+\)', '', word)
                w.word_actual = w.word
            else:
                w.word_target = re.sub('xxx?|www', '???', word)
                w.word = re.sub('xxx?', '???', word)
                w.word_actual = w.word
