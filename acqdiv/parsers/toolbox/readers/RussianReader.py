import re

from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader


class RussianReader(ToolboxReader):

    language = 'Russian'

    @classmethod
    def get_utterance_raw(cls, rec_dict):
        return rec_dict.get('text', '')

    @classmethod
    def get_speaker_label(cls, rec_dict):
        return rec_dict.get('EUDICOp', '')

    @classmethod
    def get_seg_tier(cls, rec_dict):
        return rec_dict.get('lem', '')

    @classmethod
    def get_gloss_tier(cls, rec_dict):
        return rec_dict.get('mor', '')

    @classmethod
    def get_pos_tier(cls, rec_dict):
        return rec_dict.get('mor', '')

    @staticmethod
    def get_morpheme_type():
        return 'actual'

    @classmethod
    def add_utterance_warnings(cls, utterance):
        if re.search('\[(\s*=?.*?|\s*xxx\s*)\]', utterance):
            for target in re.findall('\[=\?\s+[^\]]+\]', utterance):
                target_clean = re.sub('["\[\]?=]', '', target)
                transcription_warning = (
                    'transcription insecure (intended '
                    'form might have been "' + target_clean + '")')
                cls.warnings.append(transcription_warning)

    def make_rec(self, record):
        utterance, words, morphemes = super().make_rec(record)
        utterance['gloss_raw'] = ' '.join(
            mor['gloss_raw'] for mword in morphemes for mor in mword)

        return utterance, words, morphemes

    @classmethod
    def clean_utterance(cls, utterance):
        utterance = super().clean_utterance(utterance)

        # TODO: incorporate Russian \pho and \text tiers
        # https://github.com/uzling/acqdiv/blob/master/extraction/
        # parsing/corpus_parser_functions.py#L1586-L1599
        if utterance is not None:
            utterance = re.sub(
                '[‘’\'“”\".!,:+/]+|(&lt; )|(?<=\\s)\?(?=\\s|$)',
                '',
                utterance)
            utterance = re.sub('\\s-\\s', ' ', utterance)

            # TODO: Get warnings that are on utterance
            # (and not word/morpheme) level
            # Insecure transcriptions [?], [=( )?], [xxx]:
            # add warning, delete marker
            # Note that [xxx] usually replaces a complete utterance
            # and is non-aligned, in contrast to xxx without brackets,
            # which can be counted as a word
            if re.search('\[(\s*=?.*?|\s*xxx\s*)\]', utterance):
                utterance = re.sub('\[\s*=?.*?\]', '', utterance)

            utterance = re.sub('\s+', ' ', utterance).replace('=', '')
            utterance = utterance.strip()

        return utterance

    # ---------- tier ----------

    @staticmethod
    def remove_seg_punctuation(seg_tier):
        return re.sub('[‘’\'“”\".!,:\-?+/]', '', seg_tier)

    @staticmethod
    def unify_unknown(seg_tier):
        return re.sub('xxx?|www', '???', seg_tier)

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        for cleaning_method in [cls.remove_seg_punctuation, cls.unify_unknown]:
            seg_tier = cleaning_method(seg_tier)

        return seg_tier

    @staticmethod
    def clean_gloss_pos_punctuation(gloss_pos_tier):
        return gloss_pos_tier.replace('PUNCT', '').replace('ANNOT', '').\
            replace('<NA: lt;> ', '')

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        return cls.clean_gloss_pos_punctuation(gloss_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        return cls.clean_gloss_pos_punctuation(pos_tier)

    @classmethod
    def get_lang_tier(cls, rec_dict):
        return rec_dict.get('pos_raw', '')

    @classmethod
    def clean_lang_tier(cls, lang_tier):
        return cls.clean_gloss_pos_punctuation(lang_tier)

    # ---------- morpheme words ----------

    @classmethod
    def get_morpheme_words(cls, morpheme_tier):
        return morpheme_tier.split()

    @classmethod
    def iter_gloss_pos_words(cls, gloss_pos_tier):
        """Iter gloss and POS tag of a word.

        Tier \mor contains both glosses and POS, # separated by "-" or ":".
        """
        if not gloss_pos_tier:
            cls.warnings.append('not glossed')
        else:
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
            # TODO: does it make sense to NULL this?
            return [None]
        else:
            return ['Russian']