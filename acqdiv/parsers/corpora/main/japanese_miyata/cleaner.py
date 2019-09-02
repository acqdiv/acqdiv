
from acqdiv.parsers.chat.cleaners.cleaner import CHATCleaner
from acqdiv.parsers.corpora.main.japanese_miipro.cleaner import \
    JapaneseMiiProCleaner
from acqdiv.parsers.chat.cleaners.utterance_cleaner \
    import CHATUtteranceCleaner
from acqdiv.parsers.corpora.main.japanese_miyata.gloss_mapper \
    import JapaneseMiyataGlossMapper as GMp
from acqdiv.parsers.corpora.main.japanese_miyata.pos_mapper \
    import JapaneseMiyataPOSMapper as PMp


class JapaneseMiyataCleaner(CHATCleaner):

    # ---------- morphology tier cleaning ----------

    @classmethod
    def remove_dloc(cls, morph_tier):
        """Remove dloc|dloc=DISLOC words on the morphology tier.

        dloc|dloc=DISLOC stands for `„` on the utterance.
        """
        morph_tier = morph_tier.replace('dloc|dloc=DISLOC', '')
        return CHATUtteranceCleaner.remove_redundant_whitespaces(morph_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        morph_tier = CHATUtteranceCleaner.remove_terminator(morph_tier)
        morph_tier = cls.remove_dloc(morph_tier)
        return morph_tier

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
        if session_filename.startswith('Tai') and speaker_label == 'TAI':
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

    # ---------- morpheme cleaning ----------

    @classmethod
    def clean_gloss(cls, gloss):
        return GMp.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return PMp.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return PMp.map(pos_ud, ud=True)
