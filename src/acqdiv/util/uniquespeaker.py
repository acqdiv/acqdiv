from acqdiv.model.uniquespeaker import UniqueSpeaker

uniquespeakers = {}


def set_unique_speakers(corpus, speakers):
    """Set unique speakers.

    Args:
        corpus (str): The corpus name.
        speakers (List[acqdiv.model.speaker.Speaker]): The session speakers.
    """
    for speaker in speakers:
        key = (corpus, speaker.code, speaker.name, speaker.birth_date)

        if key in uniquespeakers:
            uspeaker = uniquespeakers[key]
        else:
            uspeaker = UniqueSpeaker()
            uspeaker.code = speaker.code
            uspeaker.name = speaker.name
            uspeaker.gender = speaker.gender
            uspeaker.gender_raw = speaker.gender_raw
            uspeaker.birth_date = speaker.birth_date
            uniquespeakers[key] = uspeaker

        speaker.uniquespeaker = uspeaker
