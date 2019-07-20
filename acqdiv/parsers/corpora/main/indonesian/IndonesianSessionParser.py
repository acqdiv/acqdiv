import os
import re

from acqdiv.parsers.corpora.main.indonesian.IndonesianReader import \
    IndonesianReader
from acqdiv.parsers.corpora.main.indonesian.IndonesianCleaner \
    import IndonesianCleaner
from acqdiv.parsers.metadata.CHATParser import CHATParser
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser
from acqdiv.model.Speaker import Speaker
from acqdiv.model.Word import Word


class IndonesianSessionParser(ToolboxParser):

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
            speaker.birth_date = speaker_dict.get('birthday', None)
            speaker.gender_raw = speaker_dict.get('sex', None)
            speaker.code = speaker_dict.get('id', None)
            speaker.age_raw = speaker_dict.get('age', None)
            speaker.role_raw = speaker_dict.get('role', None)
            speaker.name = speaker_dict.get('name', None)
            speaker.languages_spoken = speaker_dict.get('language', None)

            self.session.speakers.append(speaker)

    def get_record_reader(self):
        return IndonesianReader()

    def get_cleaner(self):
        return IndonesianCleaner()

    def add_words(self, actual_utterance, target_utterance):
        utt = self.session.utterances[-1]

        for word in self.record_reader.get_words(actual_utterance):
            w = Word()
            w.utterance = utt
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
