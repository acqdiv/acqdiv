

def align_words_morphemes(utt):
    """Align words and morphemes of an utterance.

    Sets the word of the morpheme that it belongs to when there are
    no misalignments. Also, copies the POS and POS UD to the word.

    Args:
        utt (acqdiv.model.utterance.Utterance): The utterance.
    """
    link_to_word = len(utt.morphemes) == len(utt.words)
    for i, mword in enumerate(utt.morphemes):
        for morpheme in mword:
            if link_to_word:
                morpheme.word = utt.words[i]
                if morpheme.pos not in ['sfx', 'pfx']:
                    utt.words[i].pos = morpheme.pos
                    utt.words[i].pos_ud = morpheme.pos_ud


def fix_misalignments(entities):
    """Fix misalignments.

    Correct mismatches in the number of entities.

    Example:
        fix_misalignments([['seg1', 'seg2'], ['gloss1'], ['pos1', 'pos2']])
        => [['seg1', 'seg2'], ['', ''], ['pos1', 'pos2']]

    Args:
        entities (List[List[Any]]): The entities.

    Returns:
        List[List[Any]]: The aligned entities.
    """
    n = _get_number_of_entities(entities)
    _adjust_misaligned_entities(n, entities)

    return entities


def _get_number_of_entities(entities):
    """Get number of entities.

    Args:
        entities (List[List[Any]]]): The entities

    These entities may be words or morphemes. The number of entities is
    calculated based on:
     - The order of the lists of entities.
     - Whether the lists are empty or not.

     Returns: int
    """
    for entities_set in entities:
        if len(entities_set):
            return len(entities_set)

    return 0


def _adjust_misaligned_entities(n, entities):
    """Adjust misaligned entities.

    Lists diverging from `n` in terms of the number of entities that
    they contain will be adjusted in such a way that they have
    the same number of entities which are empty.

    Args:
        n (int): The number of entities to be considered.
        entities (List[List[Any]]]): The entities.
    """
    for i, entity_list in enumerate(entities):
        if n != len(entity_list):
            entities[i] = n * ['']
