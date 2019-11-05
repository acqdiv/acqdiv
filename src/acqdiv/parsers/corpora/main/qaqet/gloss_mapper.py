from acqdiv.parsers.toolbox.cleaners.morpheme_cleaner \
    import ToolboxMorphemeCleaner
from acqdiv.util.csvparser import parse_csv
from acqdiv.util.path import get_full_path


class QaqetGlossMapper:

    gloss_dict = parse_csv(get_full_path(
        'parsers/corpora/main/qaqet/resources/gloss.csv'))

    @classmethod
    def map(cls, gloss):
        gloss = ToolboxMorphemeCleaner.remove_morpheme_delimiters(gloss)
        return cls.infer_gloss(gloss)

    @classmethod
    def infer_gloss(cls, gloss):
        if gloss:
            atms_gloss_raw = gloss.split('.')
            gloss = []
            for atm_gl_raw in atms_gloss_raw:
                if atm_gl_raw not in cls.gloss_dict:
                    atm_gl = '???'
                else:
                    atm_gl = cls.gloss_dict[atm_gl_raw]
                gloss.append(atm_gl)
            # If all atm_poses are '', set to None.
            for atm_gloss in gloss:
                if atm_gloss != '???':
                    gloss = '.'.join(gloss)
                    break
            else:
                gloss = ''
        else:
            gloss = ''

        return gloss
