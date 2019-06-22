from acqdiv.parsers.chat.readers.BaseCHATReader import BaseCHATReader


class PhonbankReader(BaseCHATReader):

    def get_phon_tier(self):
        return self._dependent_tiers.get('pho', '')

    @classmethod
    def get_phon_words(cls, phon_tier):
        return cls.get_utterance_words(phon_tier)

    @staticmethod
    def iter_phons(word):
        wlen = len(word)

        skip = False

        for i, char in enumerate(word):

            if skip:
                skip = False
                continue

            if i+1 < wlen:
                next_char = word[i+1]
                if next_char == 'ː':
                    skip = True
                    yield char + next_char
                else:
                    yield char
            else:
                yield char

    @classmethod
    def get_phons(cls, word):
        """Return the phoneme string."""
        return ' '.join(phon for phon in cls.iter_phons(word))

    @classmethod
    def get_word_length(cls, word):
        """Return the number of letters in a word."""
        return sum(1 for _ in cls.iter_phons(word))
