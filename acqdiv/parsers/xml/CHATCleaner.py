import re

from acqdiv.parsers.xml.interfaces import CorpusCleanerInterface


class CHATCleaner(CorpusCleanerInterface):
    """Clean parts of a CHAT record.

    This class provides a range of cleaning methods that perform modifications,
    additions or removals to parts of a CHAT record. Redundant whitespaces that
    are left by a cleaning operation are always removed, too.

    The order of calling the cleaning methods has great impact on the final
    result, e.g. handling of repetitions has to be done first, before
    scoped symbols are removed.

    If the docstring of a cleaning method does not explicitly contain argument
    or return information, the method will only accept strings as arguments
    and return a cleaned version of the string.
    """
    # ---------- metadata cleaning ----------

    @staticmethod
    def clean_date(date):
        """Clean the date.

        CHAT date format:
            day-month-year
            \d\d-\w\w\w-\d\d\d\d
        """
        mapping = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
                   'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
                   'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
        if not date:
            return ''
        else:
            day, month, year = date.split('-')
            month_clean = mapping[month]
            return '-'.join([year, month_clean, day])

    # ---------- utterance cleaning ----------

    @staticmethod
    def remove_redundant_whitespaces(utterance):
        """Remove redundant whitespaces in utterances.

        Strips multiple whitespaces as well as leading and trailing
        whitespaces. This method is routinely called by various
        cleaning methods.
        """
        whitespace_regex = re.compile(r'\s+')
        return whitespace_regex.sub(' ', utterance).strip(' ')

    @classmethod
    def remove_terminator(cls, utterance):
        """Remove the terminator from the utterance.

        There are 13 different terminators in CHAT. Coding: [+/.!?"]*[!?.]  .
        """
        # postcodes or nothing may follow terminators
        terminator_regex = re.compile(r'[+/.!?"]*[!?.](?=( \[\+|$))')
        clean = terminator_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    @staticmethod
    def null_untranscribed_utterances(utterance):
        """Null utterances containing only untranscribed material.

        Note:
            Nulling means here the utterance is returned as an empty string.
        """
        if utterance == '???':
            return ''
        else:
            return utterance

    @staticmethod
    def null_event_utterances(utterance):
        """Null utterances that are events.

        CHAT coding: 0
        """
        if utterance == '0':
            return ''
        else:
            return utterance

    @classmethod
    def remove_events(cls, utterance):
        """Remove events from the utterance.

        Coding in CHAT: word starting with &=.
        """
        event_regex = re.compile(r'&=\S+')
        clean = event_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    @staticmethod
    def handle_repetitions(utterance):
        """Write out repeated words in the utterance.

        Words are repeated without modification.

        Coding in CHAT: [x <number>]  .
        """
        repetition_regex = re.compile(r'(?:<(.*?)>|(\S+)) \[x (\d)\]')
        # build cleaned utterance
        clean = ''
        match_end = 0
        for match in repetition_regex.finditer(utterance):
            # add material preceding match
            match_start = match.start()
            clean += utterance[match_end:match_start]

            # check whether it has scope over one or several words
            if match.group(1):
                words = match.group(1)
            else:
                words = match.group(2)

            # repeat the word
            repetitions = int(match.group(3))
            clean += ' '.join([words]*repetitions)

            match_end = match.end()

        # add material following last match
        clean += utterance[match_end:]

        if clean:
            return clean
        else:
            return utterance

    @classmethod
    def remove_omissions(cls, utterance):
        """Remove omissions in the utterance.

        Coding in CHAT: word starting with 0.

        Those occurring in square brackets are ignored.
        """
        omission_regex = re.compile(r'0\S+[^\]](?=\s|$)')
        clean = omission_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    @staticmethod
    def unify_untranscribed(utterance):
        """Unify untranscribed material as ???.

        Coding in CHAT: xxx, yyy, www   .
        """
        untranscribed_regex = re.compile(r'xxx|yyy|www')
        return untranscribed_regex.sub('???', utterance)

    @staticmethod
    def remove_linkers(utterance):
        """Remove linkers from the utterance.

        Coding in CHAT: +["^,+<] (always in the beginning of utterance).
        """
        linker_regex = re.compile(r'^\+["^,+<]')
        return linker_regex.sub('', utterance).lstrip(' ')

    @staticmethod
    def remove_separators(utterance):
        """Remove separators from the utterance.

        Separators are commas, colons or semi-colons which are surrounded
        by whitespaces.
        """
        separator_regex = re.compile(r' [,:;]( )')
        return separator_regex.sub(r'\1', utterance)

    @classmethod
    def remove_ca(cls, utterance):
        """Remove conversation analysis and satellite markers from utterance.

        Note:
            Only four markers (↓↑‡„“”) are attested in the corpora. Only those
            will be checked for removal.
        """
        ca_regex = re.compile(r'[↓↑‡„“”]')
        clean = ca_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    @classmethod
    def remove_pauses_between_words(cls, utterance):
        """Remove pauses between words from the utterance.

        Coding in CHAT: (.), (..), (...)
        """
        pause_regex = re.compile(r'\(\.{1,3}\)')
        clean = pause_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    @classmethod
    def remove_scoped_symbols(cls, utterance):
        """Remove scoped symbols from utterance.

        Coding in CHAT: < > [.*]    .

        Angle and square brackets as well as the content within the square
        brackets is removed.

        Note:
            Scoped symbols can be nested to any depth:
                - word [...][...]
                - <word [...] word> [...]
                - <<word word> [...] word> [...]
        """
        scope_regex = re.compile(r'<|>|\[.*?\]')
        clean = scope_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    @classmethod
    def clean_utterance(cls, utterance):
        for cleaning_method in [
                cls.null_event_utterances, cls.unify_untranscribed,
                cls.handle_repetitions, cls.remove_terminator,
                cls.remove_events, cls.remove_omissions,
                cls.remove_linkers, cls.remove_separators, cls.remove_ca,
                cls.remove_pauses_between_words, cls.remove_scoped_symbols,
                cls.null_untranscribed_utterances]:
            utterance = cleaning_method(utterance)

        return utterance

    # ---------- word cleaning ----------

    @staticmethod
    def remove_form_markers(word):
        """Remove form markers from the word.

        Coding in CHAT: word ending with @.
        The @ and the part after it are removed.
        """
        form_marker_regex = re.compile(r'@.*')
        return form_marker_regex.sub(r'', word)

    @staticmethod
    def remove_drawls(word):
        """Remove drawls in the word.

        Coding in CHAT: : within or after word
        """
        return word.replace(':', '')

    @staticmethod
    def remove_pauses_within_words(word):
        """Remove pauses within the word.

        Coding in CHAT: ^ within word
        """
        pause_regex = re.compile(r'(\S+?)\^(\S+?)')
        return pause_regex.sub(r'\1\2', word)

    @staticmethod
    def remove_blocking(word):
        """Remove blockings in the word.

        Coding in CHAT: ^ or ≠ at the beginning of the word.
        """
        return word.lstrip('^').lstrip('≠')

    @staticmethod
    def remove_filler(word):
        """Remove filler marker from the word.

        Coding in CHAT: word starts with & or &-
        """
        filler_regex = re.compile(r'&-|&(?!=)(\S+)')
        return filler_regex.sub(r'\1', word)

    @classmethod
    def clean_word(cls, word):
        for cleaning_method in [
                cls.remove_form_markers, cls.remove_drawls,
                cls.remove_pauses_within_words, cls.remove_blocking,
                cls.remove_filler]:
            word = cleaning_method(word)

        return word

    # ---------- morphology tier cleaning ----------
    @staticmethod
    def clean_morph_tier(morph_tier):
        """No cleaning by default."""
        return morph_tier

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        return cls.clean_morph_tier(seg_tier)

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        return cls.clean_morph_tier(gloss_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        return cls.clean_morph_tier(pos_tier)

    # ---------- tier cross cleaning ----------

    @staticmethod
    def cross_clean(utterance, seg_tier, gloss_tier, pos_tier):
        """No cleaning by default."""
        return utterance, seg_tier, gloss_tier, pos_tier

    # ---------- morpheme word cleaning ----------
    @staticmethod
    def clean_morpheme_word(morpheme_word):
        """No cleaning by default."""
        return morpheme_word

    @classmethod
    def clean_seg_word(cls, seg_word):
        """No cleaning by default."""
        return cls.clean_morpheme_word(seg_word)

    @classmethod
    def clean_gloss_word(cls, gloss_word):
        """No cleaning by default."""
        return cls.clean_morpheme_word(gloss_word)

    @classmethod
    def clean_pos_word(cls, pos_word):
        """No cleaning by default."""
        return cls.clean_morpheme_word(pos_word)

    # ---------- morpheme cleaning ----------

    @staticmethod
    def clean_morpheme(morpheme):
        """No cleaning by default."""
        return morpheme

    @classmethod
    def clean_segment(cls, segment):
        return cls.clean_morpheme(segment)

    @classmethod
    def clean_gloss(cls, gloss):
        return cls.clean_morpheme(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return cls.clean_morpheme(pos)


###############################################################################

class EnglishManchester1Cleaner(CHATCleaner):

    @classmethod
    def remove_non_words(cls, morph_tier):
        """Remove all non-words from the morphology tier.

        Non-words include:
            end|end („)
            cm|cm (,)
            bq|bq (“)
            eq|eq (”)
        """
        non_words_regex = re.compile(r'end\|end'
                                     r'|cm\|cm'
                                     r'|bq\|bq'
                                     r'|eq\|eq')

        morph_tier = non_words_regex.sub('', morph_tier)
        return cls.remove_redundant_whitespaces(morph_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        for cleaning_method in [
                cls.remove_terminator, cls.remove_non_words,
                cls.remove_omissions]:
            morph_tier = cleaning_method(morph_tier)

        return morph_tier

    # ---------- morpheme cleaning ----------

    # ---------- gloss cleaning ----------

    @classmethod
    def replace_ampersand(cls, gloss):
        """Replace the ampersand in glosses by a dot.

        Fusional suffixes are suffixed to the stem by an ampersand.
        Example: be&3S -> be.3S
        """
        return gloss.replace('&', '.')

    @classmethod
    def replace_zero(cls, gloss):
        """Replace ZERO in glosses by ∅."""
        return gloss.replace('ZERO', '∅')

    @classmethod
    def clean_gloss(cls, gloss):
        for cleaning_method in [cls.replace_ampersand, cls.replace_zero]:
            gloss = cleaning_method(gloss)

        return gloss

    # ---------- POS cleaning ----------

    @staticmethod
    def extract_first_pos(pos):
        """Extract the first POS tag.

        Several POS tags are separated by ':'.
        """
        return pos.split(':')[0]

    @classmethod
    def clean_pos(cls, pos):
        return cls.extract_first_pos(pos)


class InuktitutCleaner(CHATCleaner):

    # ---------- word cleaning ----------

    @staticmethod
    def remove_dashes(word):
        """Remove dashes before/after xxx."""
        dash_regex = re.compile(r'-?(xxx)-?')
        return dash_regex.sub(r'\1', word)

    @classmethod
    def clean_word(cls, word):
        word = cls.remove_dashes(word)
        return super().clean_word(word)

    # ---------- morphology tier cleaning ----------

    @classmethod
    def clean_morph_tier(cls, xmor):
        """Clean the morphology tier 'xmor'."""
        for cleaning_method in [cls.null_event_utterances,
                                cls.unify_untranscribed,
                                cls.remove_terminator,
                                cls.remove_separators,
                                cls.remove_scoped_symbols,
                                cls.null_untranscribed_utterances]:
            xmor = cleaning_method(xmor)

        return xmor

    # ---------- morpheme word cleaning ----------

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        return cls.remove_terminator(morpheme_word)

    # ---------- morpheme cleaning ----------

    @staticmethod
    def remove_english_marker(seg):
        """Remove the marker for english words.

        English segments are marked with the form marker '@e'.

        Args:
            seg (str): The segment.

        Returns:
            str: The segment without '@e'.
        """
        english_marker_regex = re.compile(r'(\S+)@e')
        return english_marker_regex.sub(r'\1', seg)

    @classmethod
    def clean_segment(cls, seg):
        """Remove english markers from the segment."""
        return cls.remove_english_marker(seg)

    @staticmethod
    def replace_stem_gram_gloss_connector(gloss):
        """Replace the stem and grammatical gloss connector.

        A stem gloss is connected with a grammatical gloss by an ampersand.
        The connector is replaced by a dot.

        Args:
            gloss (str): The gloss.

        Returns:
            str: The stem and grammatical connector replaced by a dot.
        """
        return gloss.replace('&', '.')

    @classmethod
    def clean_gloss(cls, gloss):
        """Replace the stem and grammatical gloss connector."""
        return cls.replace_stem_gram_gloss_connector(gloss)

    @staticmethod
    def replace_pos_separator(pos):
        """Replace the POS tag separator.

        A morpheme may have several POS tags separated by a pipe.
        POS tags to the right are subcategories of the POS tags to the left.
        The separator is replaced by a dot.

        Args:
            pos (str): The POS tag.

        Returns:
            str: POS tag separator replaced by a dot.
        """
        return pos.replace('|', '.')

    @classmethod
    def clean_pos(cls, pos):
        """Replace the POS tag separator."""
        return cls.replace_pos_separator(pos)


###############################################################################


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
    def cross_clean(cls, utterance, seg_tier, gloss_tier, pos_tier):
        gloss_tier = cls.replace_eng(gloss_tier, utterance)
        return utterance, seg_tier, gloss_tier, pos_tier

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

###############################################################################


class JapaneseMiiProCleaner(CHATCleaner):

    @classmethod
    def remove_non_words(cls, morph_tier):
        """Remove all non-words from the morphology tier.

        Non-words have the POS tag 'tag'.
        """
        non_words_regex = re.compile(r'tag\|\S+')
        morph_tier = non_words_regex.sub('', morph_tier)
        return cls.remove_redundant_whitespaces(morph_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        morph_tier = cls.remove_terminator(morph_tier)
        return cls.remove_non_words(morph_tier)


###############################################################################


class SesothoCleaner(CHATCleaner):
    pass

###############################################################################


class TurkishCleaner(CHATCleaner):

    # ---------- morphology tier cleaning ----------

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        return cls.remove_terminator(morph_tier)

    # ---------- cross tier cleaning ----------

    @staticmethod
    def single_morph_word(utterance, morph_tier):
        """Handle complexes consisting of a single morphological word.

        A complex consists of several stems that are either joined by + or _.

        A complex is a single morphological word, if it has a single POS tag.
        The orthographic word will be joined by an underscore. Example:
        POS|stem1_stem2-SFX
        word:
            seg = stem1_stem2   gloss = ??? pos = POS
            seg = ???           gloss = SFX pos = ???
        """
        wwords = utterance.split(' ')
        mwords = morph_tier.split(' ')

        if len(mwords) == len(wwords) - 1:
            i = 0
            while i < len(mwords):
                if '_' in mwords[i] or '+' in mwords[i]:
                    next_word = wwords.pop(i+1)
                    wwords[i] += '_' + next_word
                i += 1

            return ' '.join(wwords), morph_tier
        else:
            return utterance, morph_tier

    @staticmethod
    def separate_morph_word(utterance, morph_tier):
        """Handle complexes consisting of separate morphological words.

        A complex consists of several stems that are either joined by + or _.

        A complex consists of two morphological words, if it has separate
        POS tags and suffixes. The orthographic word as well as the
        morphological word is split in this case. The POS tag of the whole
        complex is discarded. Example:
        wholePOS|stem1POS|stem1-STEM1SFX_stem2POS|stem2-STEM2SFX
        word1:
            seg = stem1 gloss = ???         pos = stem1POS
            seg = ???   gloss = STEM1SFX    pos = sfx
        word2:
            seg = stem2 gloss = ???         pos = stem2POS
            seg = ???   gloss = STEM2SFX    pos = sfx
        """
        wwords = utterance.split(' ')
        mwords = morph_tier.split(' ')

        new_wwords = []
        new_mwords = []

        for wword, mword in zip(wwords, mwords):
            # check for double POS tag
            match = re.search(r'\w+\|(\w+\|.*)', mword)
            if match:
                # discard POS tag of whole complex
                mword = match.group(1)
                for wm in re.split(r'[+_]', mword):
                    new_mwords.append(wm)
                for ww in re.split(r'[+_]', wword):
                    new_wwords.append(ww)
            else:
                new_mwords.append(mword)
                new_wwords.append(wword)

        return ' '.join(new_wwords), ' '.join(new_mwords)

    @classmethod
    def cross_clean(cls, utterance, seg_tier, gloss_tier, pos_tier):
        # which morphology tier does not matter, they are all the same
        morph_tier = seg_tier
        utterance, morph_tier = cls.single_morph_word(utterance, morph_tier)
        utterance, morph_tier = cls.separate_morph_word(utterance, morph_tier)
        return utterance, morph_tier, morph_tier, morph_tier

    # ---------- morpheme cleaning ----------

    # ---------- segment cleaning ----------

    @staticmethod
    def replace_plus(segment):
        """Replace plus by an underscore in the segment."""
        return segment.replace('+', '_')

    @classmethod
    def clean_segment(cls, segment):
        return cls.replace_plus(segment)
