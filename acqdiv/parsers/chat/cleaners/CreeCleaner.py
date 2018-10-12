import re

from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner


class CreeCleaner(CHATCleaner):

    # ---------- utterance cleaning ----------

    @staticmethod
    def remove_angle_brackets(utterance):
        """Remove the small angle brackets.

        The angle brackets are smaller than the standard angle brackets: ‹›
        (vs. <>). They occur around the utterance, but the closing bracket
        occurs before the utterance terminator. In CHAT, they are used for
        marking special alignment with the %pho tier.
        """
        return utterance.replace('‹', '').replace('›', '')

    @classmethod
    def clean_utterance(cls, utterance):
        utterance = cls.remove_angle_brackets(utterance)
        return super().clean_utterance(utterance)

    # ---------- word cleaning ----------

    @staticmethod
    def remove_morph_separators(word):
        """Remove morpheme separators in a word.

        An underscore is used as a morpheme separator (e.g. 'giddy_up').
        """
        morph_sep_regex = re.compile(r'(\S+?)_(\S+?)')
        return morph_sep_regex.sub(r'\1\2', word)

    @staticmethod
    def replace_zero(word):
        """Replace zéro morphemes in a word.

        'zéro' stands for zero morphemes and is replaced by 'Ø'.
        """
        return word.replace('zéro', 'Ø')

    @staticmethod
    def replace_morpheme_separator(word):
        """Replace morpheme separators in a word.

        Morphemes are separated by a tilde.
        """
        return word.replace('~', '')

    @classmethod
    def clean_word(cls, word):
        word = super().clean_word(word)
        for cleaning_method in [cls.remove_morph_separators, cls.replace_zero,
                                cls.replace_morpheme_separator]:
            word = cleaning_method(word)

        return word

    # ---------- morphology tier cleaning ----------

    @staticmethod
    def remove_square_brackets(morph_tier):
        """Remove redundant square brackets around morphology tiers.

        Morphology tiers have square brackets at their edges which can be
        removed. It is unclear what their purpose is.
        """
        return morph_tier.lstrip('[').rstrip(']')

    @classmethod
    def null_untranscribed_morph_tier(cls, morph_tier):
        """Null untranscribed morphology tier.

        Note:
            Nulling means here, an empty string is returned.
        """
        if morph_tier == '*':
            return ''

        return morph_tier

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        morph_tier = cls.remove_square_brackets(morph_tier)
        morph_tier = cls.null_untranscribed_morph_tier(morph_tier)
        return morph_tier

    # ---------- tier cross cleaning ----------

    @staticmethod
    def replace_eng(gloss_tier, utterance):
        """Replace the 'Eng' glosses by the actual words in the gloss tier.

        Returns:
            str: The gloss tier with all its 'Eng' glosses replaced.
        """
        gloss_words = gloss_tier.split(' ')
        utterance_words = utterance.split(' ')

        # check if the words are correctly aligned
        if len(gloss_words) != len(utterance_words):
            return gloss_tier
        else:
            new_gloss_words = []
            for gloss_word, actual_word in zip(gloss_words, utterance_words):
                if 'Eng' in gloss_word:
                    new_gloss_words.append(actual_word)
                else:
                    new_gloss_words.append(gloss_word)
            return ' '.join(new_gloss_words)

    @classmethod
    def cross_clean(cls, actual_utt, target_utt, seg_tier, gloss_tier,
                    pos_tier):
        gloss_tier = cls.replace_eng(gloss_tier, actual_utt)
        return actual_utt, target_utt, seg_tier, gloss_tier, pos_tier

    # ---------- morpheme word cleaning ----------

    @staticmethod
    def replace_percentages(word):
        """Replace words consisting of percentages.

        '%%%' stand for untranscribed words. They are replaced by '???'.
        """
        if word == '%%%':
            return '???'
        else:
            return word

    @staticmethod
    def replace_hashtag(morph_element):
        """Replace words and morphemes consisting of a hashtag.

        '#' stands for unglossed words and morphemes. It is replaced by
        '???'
        """
        if morph_element == '#':
            return '???'
        else:
            return morph_element

    @staticmethod
    def handle_question_mark(morph_element):
        """Handle question marks in words and morphemes.

        '?' stands for unclear meanings of a morpheme and word. If it only
        consists of '?', it is replaced by '???'. If there is a form followed
        by '?', it is removed.
        """
        if morph_element == '?':
            return '???'

        return morph_element.replace('?', '')

    @classmethod
    def replace_star(cls, morph_element):
        """Replace words or morphemes consisting of a star.

        The star marks an element that does not correspond to an element on
        another morphology tier. It is replaced by a '???'.
        """
        if morph_element == '*':
            return '???'
        else:
            return morph_element

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        for cleaning_method in [
                cls.replace_percentages, cls.replace_hashtag,
                cls.handle_question_mark, cls.replace_star]:
            morpheme_word = cleaning_method(morpheme_word)

        return morpheme_word

    # ---------- morpheme cleaning ----------

    @classmethod
    def clean_morpheme(cls, morpheme):
        for cleaning_method in [
                cls.replace_hashtag, cls.handle_question_mark,
                cls.replace_star]:
            morpheme = cleaning_method(morpheme)

        return morpheme

    @staticmethod
    def replace_gloss_connector(gloss):
        """Replace the gloss connectors.

        There are three different gloss connectors: '.', '+', ','
        ',' adds an additional specification to a gloss, e.g.
        'p,quest” (question particle)'. '+' and ',' are replaced by a dot.
        """
        return gloss.replace(',', '.').replace('+', '.')

    @classmethod
    def clean_gloss(cls, gloss):
        gloss = cls.clean_morpheme(gloss)
        return cls.replace_gloss_connector(gloss)

    @staticmethod
    def uppercase_pos_in_parentheses(pos):
        """Uppercase POS tags in parentheses.

        Parentheses indicate covert grammatical categories.
        """
        pos_in_parentheses_regex = re.compile(r'(\()(\S+)(\))')
        # extract POS in parentheses
        match = pos_in_parentheses_regex.search(pos)
        if not match:
            return pos
        else:
            # replace by uppercased version
            up_pos = match.group(2).upper()
            return pos_in_parentheses_regex.sub(r'\1{}\3'.format(up_pos), pos)

    @classmethod
    def clean_pos(cls, pos):
        pos = cls.clean_morpheme(pos)
        return cls.uppercase_pos_in_parentheses(pos)
