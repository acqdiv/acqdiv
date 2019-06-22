from acqdiv.parsers.chat.BaseCHATParser import BaseCHATParser


class PhonbankParser(BaseCHATParser):

    def get_words_dict(self, actual_utt, target_utt):
        actual_words = self.reader.get_utterance_words(actual_utt)
        target_words = self.reader.get_utterance_words(target_utt)

        phon_tier = self.reader.get_phon_tier()
        phon_words = self.reader.get_phon_words(phon_tier)

        words = []
        for word_actual, word_target, phon_word in zip(
                actual_words, target_words, phon_words):

            if self.reader.get_standard_form() == 'actual':
                word = word_actual
            else:
                word = word_target

            word_language = self.reader.get_word_language(word)

            word = self.cleaner.clean_word(word)
            word_actual = self.cleaner.clean_word(word_actual)
            word_target = self.cleaner.clean_word(word_target)

            if not self.consistent_actual_target:
                if word_actual == word_target:
                    word_target = None

            word_dict = {
                'word_language': word_language if word_language else None,
                'word': word,
                'word_actual': phon_word,
                'word_target': word_target,
                'warning': None
            }
            words.append(word_dict)

        return words