

class IndonesianPOSMapper:

    @classmethod
    def map(cls, pos, ud=False):
        """Infer POS from the gloss.

        There is no POS tier in Indonesian, but the macro categories
        `sfx`, `pfx`, `stem` can be inferred from the gloss.
        """
        if ud:
            return ''
        else:
            if pos.startswith('-'):
                return 'sfx'
            elif pos.endswith('-'):
                return 'pfx'
            elif pos in ['', '???']:
                return pos
            else:
                pos = cls.substitute(pos)
                if pos:
                    return pos
                else:
                    return 'stem'

    @staticmethod
    def substitute(pos):
        labels = {'BO', 'DAH', 'DENG', 'DING', 'EH', 'NAH'}
        if pos in labels:
            return 'PTCL'
        else:
            return ''
