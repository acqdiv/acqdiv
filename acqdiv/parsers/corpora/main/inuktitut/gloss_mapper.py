from acqdiv.util.csvparser import parse_csv
from acqdiv.util.path import get_full_path


class InuktitutGlossMapper:

    gloss_dict = parse_csv(get_full_path(
        'parsers/corpora/main/inuktitut/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        gloss = cls.clean_gloss(gloss)
        return cls.gloss_dict.get(gloss, '')

    @classmethod
    def clean_gloss(cls, gloss):
        """Replace the stem and grammatical gloss connector."""
        return cls.replace_stem_gram_gloss_connector(gloss)

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
