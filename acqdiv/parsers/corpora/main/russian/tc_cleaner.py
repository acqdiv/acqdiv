
def clean(session):
    """Correct multiple target children in session.

    Args:
        session (acqdiv.model.session.Session): The session.
    """
    tcs = [speaker for speaker in session.speakers
           if speaker.macro_role == 'Target_Child']

    if len(tcs) > 1:
        # the session code's first letter matches that of speaker label
        letter = session.source_id[0]
        for tc in tcs:
            if not tc.code.startswith(letter):
                tc.role = 'Child'
                tc.macro_role = 'Child'
