from acqdiv.parsers.chat.readers.PhonbankReader import PhonbankReader


class QuichuaReader(PhonbankReader):

    def get_phon_tier(self):
        return self._dependent_tiers.get('xpho', '')

    @classmethod
    def get_phon_words(cls, phon_tier):
        return [phon_tier]

    @classmethod
    def get_word_length(cls, word):
        return word.count(' ') + 1
