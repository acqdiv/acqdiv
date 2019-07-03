import re


class CHATUtteranceCleaner:
    """Cleaners for CHAT utterances."""

    @classmethod
    def clean(cls, utterance):
        for cleaning_method in [
                cls.remove_terminator,
                cls.unify_untranscribed,
                cls.handle_repetitions,
                cls.remove_events,
                cls.remove_omissions,
                cls.remove_linkers,
                cls.remove_separators,
                cls.remove_ca,
                cls.remove_pauses_between_words,
                cls.remove_scoped_symbols,
                cls.remove_commas,
                # cls.null_untranscribed_utterances,
                cls.null_event_utterances]:
            utterance = cleaning_method(utterance)

        return utterance

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

    # TODO: check for removal

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

    # TODO: move to word level

    @classmethod
    def null_event_utterances(cls, utterance):
        """Remove zeros coding events.

        CHAT coding: 0
        """
        regex = re.compile(r'\b0\b')
        utterance = regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(utterance)

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
        repetition_regex = re.compile(
            r'(?:<([^<]*?)>|(\S+))( \[.*?\])? ?\[x (\d+)\]')
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

            # append preceding scoped symbol
            if match.group(3):
                words += match.group(3)

            # repeat the word
            repetitions = int(match.group(4))
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
        # if not a null utterance
        if not utterance.startswith('0['):
            omission_regex = re.compile(r'0\S+[^\]](?=\s|$)')
            clean = omission_regex.sub('', utterance)
            return cls.remove_redundant_whitespaces(clean)

        return utterance

    # TODO: move to word level

    @staticmethod
    def unify_untranscribed(utterance):
        """Unify untranscribed material as ???.

        Coding in CHAT: xxx, yyy, www   .

        Note:
            This type of cleaning is done on the utterance level rather than
            on the word level because `null_untranscribed_utterances` depends
            on it.
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
