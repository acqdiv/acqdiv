class IndonesianSpeakerLabelCorrector:
    """Class for correcting speaker labels.

    Speaker label `EXP` is replaced based on the speaker's name.
    """
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
    def correct_rec_label(cls, utt_label):
        """Correct the label in the utterance."""
        if 'EXP' in utt_label:
            return utt_label[3:]
        else:
            return utt_label[0:3]

    @classmethod
    def correct_speaker_label(cls, speaker_label, speaker_name):
        """Correct the label in the speaker data."""
        if speaker_label == 'EXP':
            return cls.name2label[speaker_name]

        return speaker_label
