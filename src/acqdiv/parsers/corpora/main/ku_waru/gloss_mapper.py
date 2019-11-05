import re
from acqdiv.parsers.toolbox.cleaners.morpheme_cleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.csvparser import parse_csv
from acqdiv.util.path import get_full_path


class KuWaruGlossMapper:

    gloss_dict = parse_csv(get_full_path(
        'parsers/corpora/main/ku_waru/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        return cls.infer_gloss(gloss)

    @classmethod
    def infer_gloss(cls, gloss):
        gloss = ToolboxMorphemeCleaner.clean(gloss)

        gloss = cls.replace_colons(gloss)
        gloss = cls.remove_bt_tp(gloss)
        gloss = cls.replace_many_to_one(gloss)

        number_person_rgx = re.compile(r'[1-3/]+(SG|DU|PL)')

        # case 1: direct mapping
        if gloss in cls.gloss_dict:
            return cls.gloss_dict[gloss]

        # case 2: number-person combinations
        if number_person_rgx.fullmatch(gloss):
            return gloss

        # case 3: lexical gloss
        if gloss.islower():
            return ''

        # case 4: NER
        if gloss in ['PERSON', 'PLACE', 'TRIBE']:
            return ''

        # case 5: multi-category morpheme
        if '.' in gloss:
            categories = gloss.split('.')

            mapped_categories = []

            for category in categories:
                if number_person_rgx.fullmatch(category):
                    mapped_category = category
                elif category.islower():
                    return ''
                else:
                    mapped_category = cls.gloss_dict.get(category, '???')

                mapped_categories.append(mapped_category)

            return '.'.join(mapped_categories)

        # other
        return ''

    @staticmethod
    def replace_colons(gloss):
        """Replace colons by dots.

        Args:
            gloss (str): The gloss.

        Example:
            IMP:2/3DU => IMP.2/3DU
        """
        return gloss.replace(':', '.')

    @staticmethod
    def remove_bt_tp(gloss):
        """Remove TP and BT categories.

        `BT` denotes baby talk
        `TP` denotes Tok Pisin

        Args:
            gloss (str): The gloss.

        Example:
            banana.BT => banana
        """
        return re.sub(r'\.(BT|TP)', '', gloss)

    @staticmethod
    def replace_many_to_one(gloss):
        """Replace multi-word gloss by one-word gloss.

        Args:
            gloss (str): The gloss.

        Current multi-word glosses mapping to one-word glosses are:
            TAG.Q
            that.ABK
            that.ABU
            that.ANA
            that.END
            this.DEF
            this.IP

        Example:
            this.DEF => PROX
        """
        gloss = gloss.replace('TAG.Q', 'Q')
        gloss = re.sub(r'that\.AB[KU]', 'DEM', gloss)
        gloss = re.sub(r'that\.(ANA|END)', 'DIST', gloss)
        gloss = re.sub(r'this\.(DEF|IP)', 'PROX', gloss)

        return gloss
