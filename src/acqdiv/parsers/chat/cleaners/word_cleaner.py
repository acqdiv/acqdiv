import re


class CHATWordCleaner:

    @classmethod
    def clean(cls, word):
        for cleaning_method in [
                cls.remove_form_markers, cls.remove_drawls,
                cls.remove_pauses_within_words, cls.remove_blocking,
                cls.remove_filler]:
            word = cleaning_method(word)

        return word

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
