import re


class CHATCleaner:
    """Perform cleaning on the tiers of CHAT.

    Note:
        The order of calling the cleaning methods has great impact on the final
        result.
    """

    def _remove_redundant_whitespaces(self, utterance):
        """Remove redundant whitespaces in utterances.

        This method is routinely called by most of the cleaning methods.
        """
        whitespace_regex = re.compile(r'\s+')
        return whitespace_regex.sub(' ', utterance)

    def remove_terminator(self, utterance):
        """Remove the terminator from the utterance.

        There are 13 different terminators in CHAT. Coding: [+/.!?"]*[!?.]  .
        """
        # postcodes or nothing may follow terminators
        terminator_regex = re.compile(r'[+/.!?"]*[!?.](?=( \[\+|$))')
        clean1 = terminator_regex.sub('', utterance)
        clean2 = self._remove_redundant_whitespaces(clean1)
        return clean2

    def null_untranscribed_utterances(self, utterance):
        """Null utterances containing only untranscribed material.

        Note:
            Nulling means here the utterance is returned as an empty string.
        """
        if utterance == 'xxx':
            return ''
        else:
            return utterance

    def null_event_utterances(self, utterance):
        """Null utterances that are events.

        CHAT coding: 0
        """
        if utterance == '0':
            return ''
        else:
            return utterance

    def remove_events(self, utterance):
        """Remove events from the utterance.

        Coding in CHAT: &=\w+   .
        """
        event_regex = re.compile(r'&=\w+')
        clean1 = event_regex.sub('', utterance)
        clean2 = self._remove_redundant_whitespaces(clean1)
        return clean2

    # TODO: does not work correctly for multiple instances
    def handle_repetitions(self, utterance):
        """Write out repeated words in the utterance.

        Coding in CHAT: [x \d]  .
        """
        repetition_regex = re.compile(r'(?:<(.*?)>|(\S)) \[x (\d)\]')
        match = repetition_regex.search(utterance)
        if match:
            if match.group(1):  # several words
                words = match.group(1)
            else:
                words = match.group(2)  # one word
            repetitions = int(match.group(3))
            written_out = ' '.join([words]*repetitions)
            clean1 = repetition_regex.sub(written_out, utterance)
            clean2 = self._remove_redundant_whitespaces(clean1)
            return clean2
        else:
            return utterance

    def remove_omissions(self, utterance):
        """Remove omissions in the utterance.

        Coding in CHAT: 0\w+    .
        """
        omission_regex = re.compile(r'0\w+')
        clean1 = omission_regex.sub('', utterance)
        clean2 = self._remove_redundant_whitespaces(clean1)
        return clean2

    def unify_untranscribed(self, utterance):
        """Unify untranscribed material as xxx.

        Coding in CHAT: xxx, yyy, www   .
        """
        untranscribed_regex = re.compile(r'yyy|www')
        clean1 = untranscribed_regex.sub('xxx', utterance)
        clean2 = self._remove_redundant_whitespaces(clean1)
        return clean2

    def get_shortening_actual(self, utterance):
        """Get the actual form of shortenings.

        Coding in CHAT: \w+(\w+)\w+   .
        The part with parentheses is removed.
        """
        shortening_regex = re.compile(r'(\S*)\(\w+\)(\S*)')
        clean = ''
        match_end = 0
        for i, match in enumerate(shortening_regex.finditer(utterance)):
            match_start = match.start()
            clean += utterance[match_end:match_start]

            if match.group(1):
                clean += match.group(1)
            if match.group(2):
                clean += match.group(2)

            match_end = match.end()
        else:
            clean += utterance[match_end:]

        if clean:
            return clean
        else:
            return utterance

    def get_shortening_target(self, utterance):
        """Get the target form of shortenings.

        Coding in CHAT: \w+(\w+)\w+ .
        The part in parentheses is kept, parentheses are removed.
        """
        shortening_regex = re.compile(r'(\S*)\((\w+)\)(\S*)')
        clean1 = shortening_regex.sub(r'\1\2\3', utterance)
        clean2 = self._remove_redundant_whitespaces(clean1)
        return clean2

    def get_replacement_actual(self, utterance):
        """Get the actual form of replacements.

        Coding in CHAT: [: <words>] .
        Keeps replaced words, removes replacing words with brackets.
        """
        pass

    def get_replacement_target(self, utterance):
        """Get the target form of replacements.

        Coding in CHAT: [: <words>] .
        Removes replaced words, keeps replacing words with brackets.
        """
        pass

    def get_fragment_actual(self, utterance):
        """Get the actual form of fragments.

        Coding in CHAT: &\w+    .
        Keeps the fragment, removes the & from the word.
        """
        pass

    def get_fragment_target(self, utterance):
        """Get the target form of fragments.

        Coding in CHAT: &\w+    .
        The fragment is marked as untranscribed (xxx).
        """
        pass

    def remove_form_markers(self, utterance):
        """Remove form markers from the utterance.

        Coding in CHAT: \w+@\w+(:*|$n|:xxx) .
        The @ and the part after it are removed.
        """
        pass

    def remove_linkers(self, utterance):
        """Remove linkers from the utterance.

        Coding in CHAT: +["^,+<] (always in the beginning of utterance).
        """
        pass

    def remove_separators(self, utterance):
        """Remove separators from the utterance.

        Separators are commas, colons or semi-colons.
        """
        pass

    def remove_ca(self, utterance):
        """Remove elements from Conversational Analysis.

        Note:
            At the moment only ↓ and ↑ are attested in our corpora.
        """
        pass

    def remove_disfluency_markers(self, utterance):
        """Remove disfluency markers from the utterance.

        Coding in CHAT:
            :   lengthened sound
            ^   blocking (at beginning of word) or pause within word
            &   fragments
            &-  fillers
        """
        pass

    def remove_pauses(self, utterance):
        """Remove pauses between words from utterance..

        Coding in CHAT: (.{1,3})    .
        """
        pass

    def remove_scoped_symbols(self, utterance):
        """Remove scoped symbols from utterance.

        Coding in CHAT: < > [.*]    .
        """
        pass


if __name__ == '__main__':
    cleaner = CHATCleaner()
    print(repr(cleaner._remove_redundant_whitespaces('Das   ist zu  viel.')))
    print(repr(cleaner.remove_terminator('doa to: (.) mado to: +... [+ bch]')))
    print(repr(cleaner.null_untranscribed_utterances('xxx')))
    print(repr(cleaner.null_event_utterances('0')))
    print(repr(cleaner.remove_events('I know &=laugh what that &=laugh means .')))
    print(repr(cleaner.handle_repetitions('This <is a> [x 3] sentence [x 2].')))
    print(repr(cleaner.remove_omissions('This is 0not 0good .')))
    print(repr(cleaner.unify_untranscribed('This www I yyy is done .')))
    print(repr(cleaner.get_shortening_actual('This (i)s a short(e)ned senten(ce)')))
    print(repr(cleaner.get_shortening_target('This (i)s a short(e)ned senten(ce)')))

