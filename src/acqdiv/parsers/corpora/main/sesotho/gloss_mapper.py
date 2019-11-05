import re

from acqdiv.util.csvparser import parse_csv
from acqdiv.util.path import get_full_path


class SesothoGlossMapper:

    gloss_dict = parse_csv(get_full_path(
        'parsers/corpora/main/sesotho/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        gloss = cls.clean_gloss(gloss)
        return cls.gloss_dict.get(gloss, '')

    @classmethod
    def clean_gloss(cls, gloss):
        """Clean a Sesotho gloss."""
        for method in [cls.remove_markers,
                       cls.clean_proper_names_gloss_words,
                       cls.remove_nominal_concord_markers,
                       cls.unify_untranscribed_glosses]:
            gloss = method(gloss)
        return gloss

    @classmethod
    def remove_markers(cls, gloss):
        """Remove noun and verb markers."""
        gloss = cls.remove_noun_markers(gloss)
        gloss = cls.remove_verb_markers(gloss)
        return gloss

    @staticmethod
    def remove_noun_markers(gloss):
        """Remove noun markers."""
        return re.sub(r'[nN]\^(?=\d)', '', gloss)

    @staticmethod
    def remove_verb_markers(gloss):
        """Remove verb markers."""
        return re.sub(r'[vs]\^', '', gloss)

    @staticmethod
    def clean_proper_names_gloss_words(gloss):
        """Clean glosses of proper names.

        In proper names substitute 'n^' marker with 'a_'.
        Lowercase the labels of propernames.
        """
        gloss = re.sub(r'[nN]\^([gG]ame|[nN]ame|[pP]lace|[sS]ong)',
                            r'a_\1', gloss)
        if re.search(r'a_(Game|Name|Place|Song)', gloss):
            gloss = gloss.lower()
        return gloss

    @staticmethod
    def remove_nominal_concord_markers(gloss):
        """Remove markers for nominal concord."""
        match = re.search(r'^(d|lr|obr|or|pn|ps)\d+', gloss)
        if match:
            pos = match.group(1)
            return re.sub(pos, '', gloss)

        return gloss

    @staticmethod
    def unify_untranscribed_glosses(gloss):
        """Unify untranscribed glosses.

        In Sesotho glossing for words which are not understood or
        couldn't be analyzed are marked by 'word' or by 'xxx'. Turn
        both into the standart '???'.
        """
        if gloss == 'word' or gloss == 'xxx':
            return '???'

        return gloss
