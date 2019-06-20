
from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner
from acqdiv.parsers.chat.cleaners.JapaneseMiiProCleaner import \
    JapaneseMiiProCleaner


class JapaneseMiyataCleaner(CHATCleaner):

    # ---------- morphology tier cleaning ----------

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        morph_tier = cls.remove_terminator(morph_tier)
        return morph_tier

    # ---------- morphology tier cleaning ----------

    @classmethod
    def replace_colon_by_dot_pos(cls, pos):
        """Replace the colons in the POS tag by a dot."""
        return pos.replace(':', '.')

    @classmethod
    def clean_pos(cls, pos):
        pos = cls.replace_colon_by_dot_pos(pos)
        return pos

    # ---------- utterance cross clean ----------

    @classmethod
    def utterance_cross_clean(
            cls, raw_utt, actual_utt, target_utt,
            seg_tier, gloss_tier, pos_tier):

        return JapaneseMiiProCleaner.utterance_cross_clean(
            raw_utt,
            actual_utt,
            target_utt,
            seg_tier,
            gloss_tier,
            pos_tier)

    # ---------- speaker metadata cleaning ----------

    @classmethod
    def clean_speaker_metadata(
            cls, session_filename, label, name, role,
            age, gender, language, birth_date, target_child):
        """Correct label, role and name of speaker."""

        _, tc_name = target_child
        name = cls.correct_speaker_name(tc_name, name, label)
        role = cls.correct_role(role, session_filename, label)

        return label, name, role, age, gender, language, birth_date

    @classmethod
    def correct_role(cls, role, session_filename, speaker_label):
        if session_filename.startswith('tai') and speaker_label == 'TAI':
            return 'Target_Child'

        return role

    @classmethod
    def correct_speaker_name(cls, tc_name, name, label):
        if tc_name == 'Akifumi' and name == 'Okaasan':
            return 'Mother_of_AKI'
        elif tc_name == 'Ryookun':
            if name == 'Okaasan':
                return 'Mother_of_RYO'
            elif name == 'Papa':
                return 'Father_of_RYO'

        if label == 'REE':
            return 'Ree'

        if label == 'TOS':
            return 'Miyatanopapa'

        return name

    # ---------- session metadata cleaning ----------

    @classmethod
    def clean_session_metadata(cls, session_filename, date, media_filename):
        """Correct the session date."""
        return date, media_filename
