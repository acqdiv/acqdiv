import re

from acqdiv.parsers.chat.cleaners.cleaner import CHATCleaner
from acqdiv.parsers.chat.cleaners.utterance_cleaner \
    import CHATUtteranceCleaner
from acqdiv.parsers.corpora.main.sesotho.gloss_mapper \
    import SesothoGlossMapper
from acqdiv.parsers.corpora.main.sesotho.pos_mapper \
    import SesothoPOSMapper


class SesothoCleaner(CHATCleaner):

    @staticmethod
    def correct_birthdate(date):
        if date == '1984-01-01':
            return ''

        return date

    @staticmethod
    def correct_speaker_name(name, speaker_label):
        if name == 'Khetheng':
            return 'Khethang'

        if name == 'child':
            return 'Unidentified_child'

        if name == 'MantSo':
            return 'Mantso'

        if name == 'NtsoakiCousin':
            return 'Ntsoaki_Cousin'

        if name == 'TlalaneCousin':
            return 'Tlalane_Cousin'

        if speaker_label == 'MAN':
            return 'Mathoto'

        if speaker_label == 'JUL':
            return 'Julia'

        if speaker_label == 'LIN':
            return 'Lineo'

        if speaker_label == 'NEU':
            return 'Neuoe_Cousin'

        return name

    @classmethod
    def clean_speaker_metadata(
            cls, session_filename, label, name, role,
            age, gender, language, birth_date, target_child):
        """Correct label, role and name of speaker."""
        birth_date = cls.correct_birthdate(birth_date)
        name = cls.correct_speaker_name(name, label)

        return label, name, role, age, gender, language, birth_date

    # ---------- utterance cleaning ----------

    @classmethod
    def clean_utterance(cls, utterance):
        utterance = cls.remove_words_in_parentheses(utterance)
        utterance = cls.remove_parentheses(utterance)
        return super().clean_utterance(utterance)

    @staticmethod
    def remove_words_in_parentheses(utterance):
        """Remove words in parentheses.

        In Sesotho, these are only used to mark contractions of the
        verb 'go' which are conventional in both child and adult
        speech.
        """
        if utterance.startswith('('):
            return re.sub(r'\(\w+\) ', '', utterance)

        return re.sub(r' \(\w+\) ', ' ', utterance)

    @staticmethod
    def remove_parentheses(utterance):
        """Remove parentheses.

        Because words that are entirely surrounded by parentheses are
        already removed, this method should just remove parentheses,
        that only surround a part of a word.

        Such parentheses are leftovers from the morpheme joining.
        """
        return re.sub(r'[()]', '', utterance)

    @classmethod
    def clean_translation(cls, translation):
        """Clean the Sesotho translation tier."""
        return cls.remove_timestamp(translation)

    @classmethod
    def remove_timestamp(cls, translation):
        """Remove timestamps in the Sesotho translation tier."""
        translation = re.sub(r'[0-9]+_[0-9]+', '', translation)
        return CHATUtteranceCleaner.remove_redundant_whitespaces(translation)

    # ---------- cross cleaning ----------

    @classmethod
    def utterance_cross_clean(
            cls, raw_utt, actual_utt, target_utt,
            seg_tier, gloss_tier, pos_tier):
        """Clean seg_tier, gloss_tier and pos_tier from contractions."""
        seg_tier, gloss_tier, pos_tier = cls.remove_contractions(
            seg_tier, gloss_tier, pos_tier)
        return actual_utt, target_utt, seg_tier, gloss_tier, pos_tier

    @classmethod
    def remove_contractions(cls, seg_tier, gloss_tier, pos_tier):
        """Remove contractions

        Remove words on the morpheme tiers, that are fully surrounded
        by parentheses. These parentheses can be used in Sesotho to mark
        contractions of the verb go.

        Since such contractions are only marked on the segment tier and
        misalignments should be avoided, the pos-words and gloss-words
        at the same index are also deleted.
        """
        gloss_tier = re.sub(r'\s+,\s+', ',', gloss_tier)
        pos_tier = re.sub(r'\s+,\s+', ',', pos_tier)
        seg_words = seg_tier.split(' ')
        gloss_words = gloss_tier.split(' ')
        pos_words = pos_tier.split(' ')
        seg_words_clean = []
        gloss_words_clean = []
        pos_words_clean = []
        slen = len(seg_words)
        glen = len(gloss_words)
        plen = len(pos_words)

        for i in range(glen):
            # Check if i is in range of seg_words to then check if there
            # is a contraction.
            if i < slen:
                if not re.search(r'^\(.*\)$', seg_words[i]):
                    # i must be in range for gloss_words and seg_words,
                    # but check if i is in range for pos_words.
                    gloss_words_clean.append(gloss_words[i])
                    seg_words_clean.append(seg_words[i])
                    if i < plen:
                        pos_words_clean.append(pos_words[i])
            else:
                # If i not in range for seg_words, check and append for
                # the other tiers, since there could be a misalignment.
                gloss_words_clean.append(gloss_words[i])
                if i < plen:
                    pos_words_clean.append(pos_words[i])

        seg_tier = ' '.join(seg_words_clean)
        gloss_tier = ' '.join(gloss_words_clean)
        pos_tier = ' '.join(pos_words_clean)

        return seg_tier, gloss_tier, pos_tier

    # ---------- morpheme cleaning ----------

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        """Clean the segment tier by removing the terminator."""
        return CHATUtteranceCleaner.remove_terminator(seg_tier)

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        """Clean the gloss tier."""
        for method in [CHATUtteranceCleaner.remove_terminator,
                       cls.remove_spaces_noun_class_parentheses,
                       cls.replace_noun_class_separator]:
            gloss_tier = method(gloss_tier)

        return gloss_tier

    @staticmethod
    def remove_spaces_noun_class_parentheses(gloss_tier):
        """Remove spaces in noun class parentheses.

        Noun classes in Sesotho are indicated as '(x , y)'. The spaces
        around the comma are removed so that word splitting by space
        doesn't split noun classes.
        """
        return re.sub(r'\s+,\s+', ',', gloss_tier)

    @staticmethod
    def replace_noun_class_separator(gloss_tier):
        """Replace '/' as noun class separator with '|'.

        This is to ensure that '/' can't be confused with '/' as a
        morpheme separator.
        """
        return re.sub(r'(\d+a?)/(\d+a?)', r'\1|\2', gloss_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        """Clean pos_tier with same methods as gloss_tier."""
        return cls.clean_gloss_tier(pos_tier)

    @classmethod
    def clean_seg_word(cls, seg_word):
        """Remove parentheses."""
        return re.sub(r'[()]', '', seg_word)

    @classmethod
    def replace_concatenators(cls, gloss_word):
        """Replace '_' as concatenator of glosses with '.'.

        But don't replace '_' as concatenator of
        verb-multi-word-expressions.
        """
        glosses_raw = gloss_word.split('-')
        glosses_clean = []
        pos = ''
        passed_stem = False
        len_raw = len(glosses_raw)
        for gloss in glosses_raw:
            if len_raw == 1 or (re.search(r'(v|id)\^|\(\d', gloss)
                                       or re.match(r'(aj$|nm$|ps\d+)', gloss)):
                passed_stem = True
            elif not passed_stem:
                pos = 'pfx'
            elif passed_stem:
                pos = 'sfx'
            if pos == 'sfx' or pos == 'pfx':
                if not re.search(r'[vs]\^', gloss):
                    if not re.search(r'\(\d+', gloss):
                        glosses_clean.append(re.sub(r'_', r'.', gloss))
                    else:
                        glosses_clean.append(gloss)
                else:
                    glosses_clean.append(gloss)
            else:
                glosses_clean.append(gloss)

        gloss_word = '-'.join(glosses_clean)
        return gloss_word

    @staticmethod
    def remove_parentheses_inf(gloss_word):
        """Remove parentheses from infinitives.

        In Sesotho some infinitives are partially surrounded by
        parentheses. Remove those parentheses.
        """
        if not re.search(r'^\(.*\)$', gloss_word):
            return re.sub(r'\(([a-zA-Z]\S+)\)', r'\1', gloss_word)

        return gloss_word

    @classmethod
    def clean_gloss_word(cls, gloss_word):
        """Clean a Sesotho gloss word."""
        gloss_word = cls.replace_concatenators(gloss_word)
        gloss_word = cls.remove_parentheses_inf(gloss_word)
        return super().clean_gloss_word(gloss_word)

    @classmethod
    def clean_gloss(cls, gloss):
        return SesothoGlossMapper.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return SesothoPOSMapper.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return SesothoPOSMapper.map(pos_ud, ud=True)
