

class IndonesianSpeakerLabelCorrector:

    name2label = {
        'Bety': 'BET',
        'Okki': 'OKK',
        'Liana': 'LIA',
        'Widya': 'WID',
        'Dalan': 'DAL',
        'Yanti': 'YAN',
        'Lanny': 'LAN',
        'Like': 'LIK',
        'Dini': 'DIN',
        'Erni': 'ERN',
        'Uri': 'URI'
    }

    @classmethod
    def correct(cls, session):
        """Correct the speaker labels.

        Speaker label `EXP` is replaced based on the speaker's name both
        in the record and speaker data.

        Args:
            session (acqdiv.model.session.Session): The session instance.

        Returns:
            session (acqdiv.model.Session.Session): The session instance.
        """
        for utt in session.utterances:
            if 'EXP' in utt.speaker_label:
                utt.speaker_label = utt.speaker_label[3:]
            else:
                utt.speaker_label = utt.speaker_label[0:3]

        for speaker in session.speakers:
            if speaker.code == 'EXP':
                speaker.code = cls.name2label[speaker.name]
