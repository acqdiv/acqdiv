import re


class ToolboxMorphemeCleaner:

    @classmethod
    def clean(cls, morpheme):
        morpheme = cls.remove_morpheme_delimiters(morpheme)
        morpheme = cls.null_unknown(morpheme)

        return morpheme

    @staticmethod
    def remove_morpheme_delimiters(morpheme):
        """Remove morpheme delimiters.

        Morpheme delimiters are `-` and `=`.
        """
        return morpheme.strip('-').strip('=')

    @staticmethod
    def null_unknown(morpheme):
        """Return empty string for unknown values.

        Unknown values: ***, ???
        """
        return re.sub(r'\*{3}|\?{3}', '', morpheme)
