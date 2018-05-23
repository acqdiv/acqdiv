
class CHATCleaner:
    """Perform cleaning on the tiers of CHAT.

    Note:
        The order of calling the cleaning methods has great impact on the final
        result.
    """

    def remove_terminator(self, utterance):
        """Remove the terminator from the utterance.

        There are 13 different terminators in CHAT. Coding: [+/.!?"]*[!?.]  .
        """
        pass

    def null_untranscribed_utterances(self, utterance):
        """Null utterances containing only untranscribed material.

        Note:
            Nulling means here the utterance is returned as an empty string.
        """
        pass

    def null_event_utterances(self, utterance):
        """Null utterances that are events.

        CHAT coding: 0
        """
        pass

    def remove_events(self, utterance):
        """Remove events from the utterance.

        Coding in CHAT: &=\w+   .
        """
        pass

    def handle_repetitions(self, utterance):
        """Write out repeated words in the utterance.

        Coding in CHAT: [x \d]  .
        """
        pass

    def remove_omissions(self, utterance):
        """Remove omissions in the utterance.

        Coding in CHAT: 0\w+    .
        """

    def unify_untranscribed(self, utterance):
        """Unify untranscribed material as xxx.

        Coding in CHAT: xxx, yyy, www   .
        """
        pass

    def get_shortening_actual(self, utterance):
        """Get the actual form of shortenings.

        Coding in CHAT: \w+(\w+)\w+   .
        The part with parentheses is removed.
        """
        pass

    def get_shortening_target(self, utterance):
        """Get the target form of shortenings.

        Coding in CHAT: \w+(\w+)\w+ .
        The part in parentheses is kept, parentheses are removed.
        """
        pass

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
