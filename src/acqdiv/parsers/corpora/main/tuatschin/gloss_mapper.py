import re

from acqdiv.util.csvparser import parse_csv
from acqdiv.util.path import get_full_path


class TuatschinGlossMapper:

    gloss_dict = parse_csv(get_full_path(
        'parsers/corpora/main/tuatschin/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        gloss = cls.clean_gloss(gloss)

        if gloss:
            # replace person/number combinations first
            pnum_regex = re.compile(r'([0123])\.(Sing)')
            gloss = pnum_regex.sub(r'\1SG', gloss)
            pnum_regex = re.compile(r'([0123])\.(Plur)')
            gloss = pnum_regex.sub(r'\1PL', gloss)

            parts = []
            is_null = False
            for part in gloss.split('.'):
                if re.search(r'[0123](SG|PL)', part):
                    parts.append(part)
                else:
                    if part in cls.gloss_dict:
                        part = cls.gloss_dict[part]

                        if part != '???':
                            parts.append(part)
                        else:
                            is_null = True
                            break
                    else:
                        is_null = True
                        break

            if is_null:
                gloss = ''
            else:
                gloss = '.'.join(parts)

        else:
            gloss = ''

        return gloss

    @classmethod
    def clean_gloss(cls, gloss):
        for cleaning_method in [
            cls.remove_pos
        ]:
            gloss = cleaning_method(gloss)
        return gloss

    @staticmethod
    def remove_pos(gloss):
        """Remove the POS tag.

        Morpho-syntactic annotations start with the POS tag:
        [POS].[SUB-GlOSS1].[SUB-GLOSS2]

        Example:
            ADJ.Fem.Sing => Fem.Sing
        """
        regex = re.compile(r'^[^.]+\.')
        gloss = regex.sub('', gloss)

        return gloss
