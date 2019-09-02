"""Abstract class for session parsing."""

from abc import ABC, abstractmethod


class SessionParser(ABC):

    @abstractmethod
    def parse(self):
        """Return an instance of a Session.

        Returns:
            acqdiv.model.session.Session: The Session instance.
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

    @classmethod
    def fix_misalignments(cls, entities):
        """Fix misalignments.

        Example1:
            [['seg1', 'seg2'], ['gloss1'], ['pos1', 'pos2']]
            => [['seg1', 'seg2'], ['', ''], ['pos1', 'pos2']]
        """
        n = cls.get_number_of_entities(entities)
        cls.adjust_misaligned_entities(n, entities)

        return entities

    @staticmethod
    def get_number_of_entities(entities):
        """Get number of entities.

        Args:
            entities (List[List[Any]]]): The entities

        These entities may be words or morphemes. The number of entities is
        calculated based on:
         - The order of the lists of entities.
         - Whether the lists are empty or not.
        """
        for entities_set in entities:
            if len(entities_set):
                return len(entities_set)

        return 0

    @staticmethod
    def adjust_misaligned_entities(n, entities):
        """Adjust misaligned entities.

        Lists diverging from `n` in terms of the number of entities that
        they contain will be adjusted in such a way that they have
        the same number of entities which are empty.
        """
        for i, entity_list in enumerate(entities):
            if n != len(entity_list):
                entities[i] = n * ['']
