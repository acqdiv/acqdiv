import re

from acqdiv.util.csvparser import parse_csv
from acqdiv.util.path import get_full_path


class NungonGlossMapper:

    gloss_dict = parse_csv(get_full_path(
        'parsers/corpora/main/nungon/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        gloss = cls.clean_gloss(gloss)
        return cls.gloss_dict.get(gloss, '')

    @classmethod
    def clean_gloss(cls, gloss):
        for cleaning_method in [
                cls.remove_question_mark,
                cls.replace_slash,
                cls.replace_plus
        ]:
            gloss = cleaning_method(gloss)
        return gloss

    @staticmethod
    def remove_question_mark(morpheme):
        """Remove the question mark in the morpheme.

        Question marks might code insecure annotations. They are prefixed to
        the morpheme.
        """
        return morpheme.lstrip('?')

    @staticmethod
    def replace_slash(gloss):
        """Replace the slash by a dot between numbers."""
        return re.sub(r'(\d)/(\d)', r'\1.\2', gloss)

    @staticmethod
    def replace_plus(gloss):
        """Replace the plus by a dot."""
        return gloss.replace('+', '.')
