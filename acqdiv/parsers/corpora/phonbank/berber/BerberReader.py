from acqdiv.parsers.corpora.phonbank.PhonbankReader import PhonbankReader


class BerberReader(PhonbankReader):

    def get_utterance(self):
        phon_tier = self.get_phon_tier()
        phon_words = self.get_phon_words(phon_tier)
        return ' '.join('xxx' for _ in phon_words)

    def get_actual_utterance(self):
        return self.get_utterance()

    def get_target_utterance(self):
        return self.get_utterance()

    def get_translation(self):
        return self.get_mainline_utterance(self._main_line_fields)

    def get_phon_tier(self):
        return self._dependent_tiers.get('xpho', '')

    @classmethod
    def get_phon_words(cls, phon_tier):
        return phon_tier.split(' # ')

    @classmethod
    def get_word_length(cls, word):
        # number of whitespaces + 1 (safer than counting the letters as some
        # phons consist of more letters)
        return word.count(' ') + 1
