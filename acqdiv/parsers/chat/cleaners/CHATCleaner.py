import re

from acqdiv.parsers.chat.cleaners.CHATCleanerInterface import \
    CHATCleanerInterface


class CHATCleaner(CHATCleanerInterface):
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
    def remove_commas(cls, utterance):
        """Remove commas from utterance."""
        return re.sub(r',', '', utterance)

    @classmethod
    def clean_utterance(cls, utterance):
        for cleaning_method in [
                cls.unify_untranscribed, cls.handle_repetitions,
                cls.remove_terminator, cls.remove_events,
                cls.remove_omissions, cls.remove_linkers,
                cls.remove_separators, cls.remove_ca,
                cls.remove_pauses_between_words, cls.remove_scoped_symbols,
                cls.remove_commas, cls.null_untranscribed_utterances,
                cls.null_event_utterances]:
            utterance = cleaning_method(utterance)

        return utterance

    @staticmethod
    def clean_translation(translation):
        """No cleaning by default."""
        return translation

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
        pause_regex = re.compile(r'(\S+?)\^')
        return pause_regex.sub(r'\1', word)

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
    def cross_clean(actual_utt, target_utt, seg_tier, gloss_tier, pos_tier):
        """No cleaning by default."""
        return actual_utt, target_utt, seg_tier, gloss_tier, pos_tier

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
