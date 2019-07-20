from acqdiv.parsers.corpora.main.qaqet.QaqetIMDIParser import QaqetIMDI
from acqdiv.parsers.corpora.main.qaqet.QaqetReader import QaqetReader
from acqdiv.parsers.corpora.main.qaqet.QaqetCleaner import QaqetCleaner
from acqdiv.parsers.toolbox.ToolboxParser import ToolboxParser
from acqdiv.model.Word import Word


class QaqetSessionParser(ToolboxParser):

    def get_record_reader(self):
        return QaqetReader()

    def get_metadata_reader(self):
        return QaqetIMDI(self.metadata_path)

    def get_cleaner(self):
        return QaqetCleaner()

    def add_words(self, actual_utterance, target_utterance):
        utt = self.session.utterances[-1]

        actual_words = self.record_reader.get_words(actual_utterance)
        target_words = self.record_reader.get_words(target_utterance)

        if len(actual_words) != len(target_words):
            target_words = len(actual_words)*['']

        for actual, target in zip(actual_words, target_words):
            w = Word()
            w.utterance = utt
            utt.words.append(w)

            actual_clean = self.cleaner.clean_word(actual)
            target_clean = self.cleaner.clean_word(target)

            w.word = actual_clean
            w.word_actual = actual_clean
            w.word_target = target_clean
