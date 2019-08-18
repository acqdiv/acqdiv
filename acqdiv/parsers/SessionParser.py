"""Abstract class for session parsing."""

from abc import ABC, abstractmethod


class SessionParser(ABC):

    @abstractmethod
    def parse(self):
        """Return an instance of a Session.

        Returns:
            acqdiv.model.Session.Session: The Session instance.
        """
        pass

    @staticmethod
    def align_words_morphemes(utt):
        """Align words and morphemes of an utterance.

        Sets the word of the morpheme that it belongs to when there are
        no misalignments. Also, copies the POS and POS UD to the word.
        """
        link_to_word = len(utt.morphemes) == len(utt.words)
        for i, mword in enumerate(utt.morphemes):
            for morpheme in mword:
                if link_to_word:
                    morpheme.word = utt.words[i]
                    if morpheme.pos not in ['sfx', 'pfx']:
                        utt.words[i].pos = morpheme.pos
                        utt.words[i].pos_ud = morpheme.pos_ud
