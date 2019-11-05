def infer_childdirected(utt):
    """Infer child directedness.

    Args:
        utt (acqdiv.model.utterance.Utterance): The utterance.
    """
    if utt.childdirected == '':
        if utt.addressee:
            if (utt.addressee.macro_role == 'Target_Child'
                    and utt.addressee != utt.speaker):
                return True
            else:
                return False

    return utt.childdirected
