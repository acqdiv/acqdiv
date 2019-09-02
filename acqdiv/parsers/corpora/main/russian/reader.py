import re

from acqdiv.parsers.toolbox.readers.reader import ToolboxReader


class RussianReader(ToolboxReader):

    @classmethod
    def get_actual_utterance(cls, rec):
        return rec.get('text', '')

    @classmethod
    def get_speaker_label(cls, rec):
        return rec.get('EUDICOp', '')

    @classmethod
    def get_seg_tier(cls, rec):
        return rec.get('lem', '')

    @classmethod
    def get_gloss_tier(cls, rec):
        return rec.get('mor', '')

    @classmethod
    def get_pos_tier(cls, rec):
        return rec.get('mor', '')

    @staticmethod
    def get_morpheme_type():
        return 'actual'

    # ---------- tier ----------

    @classmethod
    def get_lang_tier(cls, rec):
        return cls.get_pos_tier(rec)

    # ---------- morpheme words ----------

    @classmethod
    def get_morpheme_words(cls, morpheme_tier):
        return morpheme_tier.split()

    @classmethod
    def iter_gloss_pos_words(cls, gloss_pos_tier):
        """Iter gloss and POS tag of a word.

        Tier \mor contains both glosses and POS, # separated by "-" or ":".
        """
        if gloss_pos_tier:
            words = cls.get_morpheme_words(gloss_pos_tier)
            for word in words:
                # 1) If there is no ":" in a word string, gloss and POS are
                # identical (most frequently the case with PCL 'particle').
                if ':' not in word:
                    gloss_word = word
                    pos_word = word
                # 2) Sub-POS are always separated by "-" (e.g. PRO-DEM-NOUN),
                # subglosses are always separated by ":" (e.g. PST:SG:F).
                # What varies, though, is the character that separates POS from
                # glosses in the word: If the POS is V ('verb') or ADJ
                # ('adjective'), the glosses start behind the first "-", e.g.
                # V-PST:SG:F:IRREFL:IPFV -> POS V, gloss PST.SG.F.IRREFL.IPFV
                elif word.startswith('V') or word.startswith('ADJ'):
                    match_verb_adj = re.search('(V|ADJ)-(.*$)', word)
                    if match_verb_adj:
                        gloss_word = match_verb_adj.group(2)
                        pos_word = match_verb_adj.group(1)
                    else:
                        continue
                # 3) For all other POS, the glosses start behind the first ":",
                # e.g. PRO-DEM-NOUN:NOM:SG -> POS PRO.DEM.NOUN, gloss NOM.SG
                else:
                    match_gloss_pos = re.search('(^[^(V|ADJ)].*?):(.*$)', word)
                    if match_gloss_pos:
                        gloss_word = match_gloss_pos.group(2)
                        pos_word = match_gloss_pos.group(1)
                    else:
                        continue

                yield gloss_word, pos_word

    @classmethod
    def get_gloss_words(cls, gloss_tier):
        return [gloss_w for gloss_w, _ in cls.iter_gloss_pos_words(gloss_tier)]

    @classmethod
    def get_pos_words(cls, pos_tier):
        return [pos_w for _, pos_w in cls.iter_gloss_pos_words(pos_tier)]

    # ---------- morpheme ----------

    @classmethod
    def get_morphemes(cls, morpheme_word):
        return [morpheme_word]

    @classmethod
    def get_langs(cls, morpheme_lang_word):
        if 'FOREIGN' in morpheme_lang_word:
            return ['FOREIGN']
        else:
            return ['Russian']
