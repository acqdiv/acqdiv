
def clean(session):
    """Correct multiple target children in session.

    Args:
        session (acqdiv.model.session.Session): The session.
    """
    tcs = [speaker for speaker in session.speakers
           if speaker.macro_role == 'Target_Child']

    if len(tcs) > 1:
        label = session.source_id[:3]
        for tc in tcs:
            if tc.code != label:
                tc.role = 'Child'
                tc.macro_role = 'Child'
