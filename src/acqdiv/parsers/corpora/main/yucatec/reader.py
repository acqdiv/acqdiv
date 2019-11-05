import re

from acqdiv.parsers.chat.readers.reader import CHATReader


class YucatecReader(CHATReader):

    @staticmethod
    def get_utterance_words(utterance):
        """Get utterance words.

        Also treats `&` as a word separator.
        """
        if utterance:
            return re.split(r'\s+|&', utterance)
        else:
            return []

    def get_morph_tier(self):
        return self.record.dependent_tiers.get('xmor', '')

    @classmethod
    def get_morpheme_words(cls, morph_tier):
        """Get morpheme words.

        Words are separated by blank spaces as well as & and + in the case of
        clitics.
        """
        if morph_tier:
            return re.split(r'\s+|&|\+', morph_tier)
        else:
            return []

    @staticmethod
    def iter_morphemes(word):
        """Iter morphemes of a word.

        Morphemes are separated by '#' (prefixes), ':' (suffixes) and '-'
        (unstructured morpheme).

        Glosses and POS tags may have sub glosses and POS tags with are
        separated from the main gloss/POS tag by ':'. This use can be
        distinguished from the morpheme-separating use by checking the strings
        to the left and right of the ':' – when they consist of nothing but
        uppercase letters and digits, they are sub glosses or POS tags;
        otherwise they belong to different morphemes.

        Morphemes containing a '|' are structured, whereas those not containing
        one are unstructured. The part to the left is either the gloss or the
        POS tag, while the part to the right is the segment. A word can be
        completely or partially unstructured. The rules are as follows:
        - Word completely unstructured: The morphemes are separated by dashes.
          The segment is filled, while the gloss and POS tag remain unfilled.
        - Prefixes:
            - structured: segment is right block, gloss is left block, POS tag
              is 'pfx'
            - unstructured (NOT ATTESTED!): segment is unfilled, morpheme is
              gloss, POS tag is 'pfx'
        - Stem:
            - structured: segment is right block, left block is POS tag if it
              is in the list `stem_poses`, otherwise it is a gloss
            - unstructured: if morpheme only consists of uppercase letters and
              digits, it is a gloss, otherwise it is a segment
        - Suffixes:
            - structured: segment is right block, gloss is left block, POS tag
              is 'sfx'
            - unstructured: segment is unfilled, morpheme is gloss, POS tag is
              'sfx'
        """
        # untranscribed word
        if word == 'xxx':
            yield '', '', ''
        # completely unstructured word
        elif not re.search(r'[:|]', word) and '-' in word:
            for morpheme in word.split('-'):
                seg = morpheme
                gloss = ''
                pos = ''
                yield seg, gloss, pos
        # fully or partially structured word
        else:
            morph_regex = re.compile(
                r'(?P<prefixes>.*#)?'
                r'((?P<stemleft>[0-9A-Z.:]+)\|-?)?(?P<stemright>[^:\-]+)'
                r'(?P<suffixes>[:\-].+)?')

            match = morph_regex.fullmatch(word)

            # ----- prefixes -----

            # if there are prefixes
            if match.group('prefixes'):
                prefix_string = match.group('prefixes').rstrip('#')
                # iter prefixes
                for pfx in prefix_string.split('#'):
                    pfx_structured = re.search(r'(.*)\|(.+)', pfx)
                    # structured prefixes
                    if pfx_structured is not None:
                        seg = pfx_structured.group(2)
                        gloss = pfx_structured.group(1)
                        pos = 'pfx'
                    # unstructured prefixes, tends to be gloss
                    else:
                        seg = ''
                        gloss = pfx
                        pos = 'pfx'
                    yield seg, gloss, pos

            # ----- stem -----

            # structured stems
            if match.group('stemleft'):
                seg = match.group('stemright')
                stem_left = match.group('stemleft')
                # stems with lexical meaning with the following POS tags
                # TODO: recheck this list
                stem_poses = {
                    '3PRON', 'ADJ', 'ADV', 'AUX',
                    'CLFR', 'CLFR.INAN', 'CLFR:INAN',
                    'CONJ', 'DEICT', 'DEM', 'DET', 'INT', 'INTERJ',
                    'N', 'N.PROP', 'N:PROP',
                    'NUM', 'PREP', 'PTL', 'QUANT', 'S',
                    'V', 'V.AUX', 'V:AUX', 'VI', 'V.INTRANS', 'V:INTRANS',
                    'VT', 'V.TRANS', 'V:TRANS'}
                if stem_left in stem_poses:
                    gloss = ''
                    pos = stem_left
                else:
                    gloss = stem_left
                    pos = ''
            # unstructured stems
            else:
                stem_right = match.group('stemright')
                if re.fullmatch(r'[A-Z0-9]+', stem_right):
                    seg = ''
                    gloss = stem_right
                    pos = ''
                else:
                    seg = stem_right
                    gloss = ''
                    pos = ''

            yield seg, gloss, pos

            # ----- suffixes -----

            # if there are suffixes
            if match.group('suffixes'):
                suffix_string = match.group('suffixes').lstrip(':').lstrip('-')
                # iter suffixes
                for sfx in re.split(r'(?<![A-Z1-9]):|(?<!\|)-', suffix_string):
                    sfx_structured = re.search(r'(.*)\|-?(.+)', sfx)
                    # structured suffixes
                    if sfx_structured is not None:
                        seg = sfx_structured.group(2)
                        gloss = sfx_structured.group(1)
                        pos = 'sfx'
                    # unstructured suffixes: tends to be gloss
                    else:
                        seg = ''
                        gloss = sfx
                        pos = 'sfx'
                    yield seg, gloss, pos

    def get_translation(self):
        return self.record.dependent_tiers.get('xspn', '')

    @classmethod
    def get_segments(cls, seg_word):
        return [seg for seg, _, _ in cls.iter_morphemes(seg_word)]

    @classmethod
    def get_glosses(cls, gloss_word):
        return [gloss for _, gloss, _ in cls.iter_morphemes(gloss_word)]

    @classmethod
    def get_poses(cls, pos_word):
        return [pos for _, _, pos in cls.iter_morphemes(pos_word)]
