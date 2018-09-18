# -*- coding: utf-8 -*-
"""Parser for Toolbox files for the Russian, Chintang and Indonesian corpora"""

import re
import mmap
import logging
import contextlib
from itertools import zip_longest


@contextlib.contextmanager
def memorymapped(path, access=mmap.ACCESS_READ):
    """ Return a block context with path as memory-mapped file. """
    fd = open(path)
    try:
        m = mmap.mmap(fd.fileno(), 0, access=access)
    except Exception:
        fd.close()
        raise
    try:
        yield m
    finally:
        m.close()
        fd.close()


class ToolboxReader(object):
    """Toolbox Standard Format text file as iterable over records."""

    _separator = re.compile(b'\r?\n\r?\n(\r?\n)')
    _record_marker = re.compile(br'\\ref')
    _word_boundary = re.compile('(?<![\-\s])\s+(?![\-\s])')
    warnings = []

    def __init__(self, config, file_path):
        """ Initializes a Toolbox file object

        Args:
            config (CorpusConfigParser): The corpus config file.
            file_path (str): The path of the session file.
        """
        self.config = config
        self.path = file_path
        self.tier_separator = re.compile(b'\n')
        # logging.basicConfig(filename='toolbox.log', level=logging.INFO)
        self.logger = logging.getLogger('pipeline' + __name__)

        # get database column names
        self.field_markers = []
        for k, v in self.config['record_tiers'].items():
            self.field_markers.append(k)

    def __iter__(self):
        """Yield utterance, words, morphemes a session transcript file.

        This iterator directly extracts utterances for the DB column
        utterance_raw and calls various functions to extract information from
        the following levels:

        - get_sentence_type: Extract the sentence type.
        - clean_utterance: Clean up the utterance.
        - get_warnings: Get warnings like "transcription insecure".
        - get_words: Extract the words in an utterance for the words table.
        - get_morphemes: Extract the morphemes in a word for the morphemes
                         table.

        Note:
            The record marker needs to be updated if the corpus doesn't use
            "\ref" for record markers.

        Returns:
            tuple:
                utterance: {}
                words: [{},{}...]
                morphemes: [[{},{}...], [{},{}...]...]
        """
        with open(self.path, 'rb') as f:
            with contextlib.closing(
                    mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as data:
                ma = self._record_marker.search(data)
                # Skip the first rows that contain metadata information:
                # https://github.com/uzling/acqdiv/issues/154
                # TODO: what's that used for?
                # header = data[:ma.start()].decode()
                pos = ma.start()
                for ma in self._record_marker.finditer(data, ma.end()):
                    yield self.make_rec(data[pos:ma.start()])
                    pos = ma.start()
                if ma is None:
                    raise StopIteration
                else:
                    yield self.make_rec(data[pos:])

    def make_rec(self, record):
        """Parse and make utterance, words and morpheme structures.

        Args:
          record (bytestring): Toolbox record.

        Returns:
          tuple: (utterance, words, morphemes)
        """
        utterance = {}

        warnings = []
        tiers = self.tier_separator.split(record)
        for tier in tiers:
            tokens = re.split(b'\\s+', tier, maxsplit=1)
            field_marker = tokens[0].decode()
            field_marker = field_marker.replace("\\", "")
            content = None

            if len(tokens) > 1:
                content = tokens[1].decode()
                content = re.sub('\\s+', ' ', content)
                content = content.strip()
                if content.startswith('@'):
                    return None, None, None
                elif content == "":
                    # TODO: log
                    continue

            if field_marker in self.field_markers:
                utterance[self.config['record_tiers'][field_marker]] = content
                if content is None:
                    warnings.append(self.config['record_tiers'][field_marker])

        # Some records will not have an utterance, append None
        if 'utterance_raw' not in utterance:
            utterance['utterance_raw'] = None

        # Set sentence type
        if utterance['utterance_raw'] is None:
            utterance['sentence_type'] = None
        else:
            utterance['sentence_type'] = self.get_sentence_type(utterance)

        child_directed = self.get_childdirected(utterance)
        if child_directed is not None:
            utterance['childdirected'] = child_directed

        # Create clean utterance
        utterance['utterance'] = self.clean_utterance(
                                    utterance['utterance_raw'])

        # Append utterance warnings if data fields are missing in the input
        if utterance['utterance_raw'] is not None:
            if self.get_warnings(utterance['utterance_raw']) is not None:
                warnings.append(self.get_warnings(utterance['utterance_raw']))
        if len(warnings) > 0:
            utterance['warning'] = ("Empty value in the input for: "
                                    ", ".join(warnings))

        # Get words
        if utterance['utterance'] is None:
            words = []
        else:
            words = self.get_words(utterance['utterance'])

        # Get morphemes
        if utterance['utterance'] is None:
            morphemes = []
        else:
            morphemes = self.get_all_morphemes(utterance)

        for i in range(len(words)):
            try:
                words[i]['word_language'] = \
                    morphemes[i][0]['morpheme_language']
            except IndexError:
                break

        # Fix words less than morphemes misalignments
        if len(morphemes) - len(words) > 0:
            misalignment = len(morphemes) - len(words)
            for i in range(0, misalignment):
                words.append({})

        return utterance, words, morphemes

    def get_childdirected(self, record):
        """Not coded per default.

        Args:
            record (dictionary): The record.
        """
        return None

    def get_sentence_type(self, record):
        """Get utterance type (aka sentence type) of an utterance.

        Possible values:
            - default (.)
            - question (?)
            - imperative or exclamation (!)

        Args:
            record (dictionary): The record.

        Returns:
            str: The sentence type.
        """
        match_punctuation = re.search('([.?!])$', record['utterance_raw'])
        if match_punctuation is not None:
            sentence_type = None
            if match_punctuation.group(1) == '.':
                sentence_type = 'default'
            if match_punctuation.group(1) == '?':
                sentence_type = 'question'
            if match_punctuation.group(1) == '!':
                sentence_type = 'imperative'
            return sentence_type

    def get_warnings(self, utterance):
        """No warnings per default.

        Args:
            utterance (str): The utterance.
        """
        return None

    def get_words(self, utterance):
        """Get list of words from the utterance.

        Each word is a dictionary of key-value pairs.

        This function does Toolbox corpus-specific word processing and
        distinguishes between word and word_target if necessary.

        Args:
            utterance (str): The utterance.

        Returns:
            list: Dictionaries with word and
                  parent utterance id (utterance_id_fk).
        """
        result = []
        words = utterance.split()

        for word in words:
            d = {
                'word': re.sub('xxx?|www|\*\*\*', '???', word),
                'word_actual': word
            }
            result.append(d)
        return result

    # ---------- morpheme tier ----------

    @classmethod
    def get_seg_tier(cls, utterance):
        return utterance.get('morpheme', '')

    @classmethod
    def get_gloss_tier(cls, utterance):
        return utterance.get('gloss_raw', '')

    @classmethod
    def get_pos_tier(cls, utterance):
        return utterance.get('pos_raw', '')

    @classmethod
    def get_lang_tier(cls, utterance):
        return utterance.get('morpheme_lang', '')

    @classmethod
    def get_id_tier(cls, utterance):
        return utterance.get('lemma_id', '')

    # ---------- morpheme words ----------

    @classmethod
    def get_morpheme_words(cls, morpheme_tier):
        if morpheme_tier:
            return re.split(cls._word_boundary, morpheme_tier)
        else:
            return []

    @classmethod
    def get_seg_words(cls, segment_tier):
        return cls.get_morpheme_words(segment_tier)

    @classmethod
    def get_gloss_words(cls, gloss_tier):
        return cls.get_morpheme_words(gloss_tier)

    @classmethod
    def get_pos_words(cls, pos_tier):
        return cls.get_morpheme_words(pos_tier)

    @classmethod
    def get_lang_words(cls, morpheme_lang_tier):
        return cls.get_morpheme_words(morpheme_lang_tier)

    @classmethod
    def get_id_words(cls, id_tier):
        return cls.get_morpheme_words(id_tier)

    # ---------- morphemes ----------

    @classmethod
    def get_morphemes(cls, morpheme_word):
        if morpheme_word:
            return morpheme_word.split()
        else:
            return []

    @classmethod
    def get_segs(cls, segment_word):
        return cls.get_morphemes(segment_word)

    @classmethod
    def get_glosses(cls, gloss_word):
        return cls.get_morphemes(gloss_word)

    @classmethod
    def get_poses(cls, pos_word):
        return cls.get_morphemes(pos_word)

    @classmethod
    def get_langs(cls, morpheme_lang_word):
        return cls.get_morphemes(morpheme_lang_word)

    @classmethod
    def get_ids(cls, id_word):
        return cls.get_morphemes(id_word)

    @classmethod
    def get_list_of_list_morphemes(
            cls, utterance, tier_getter, words_getter, morphemes_getter,
            clean_tier=None, clean_word=None, clean_morpheme=None):
        """Get list of list of morphemes.

        Args:
            utterance (dict): The utterance dictionary containing the tiers.
            tier_getter (func): To get the correct tier.
            words_getter (func): To get the words of the tier.
            morphemes_getter(func): To get the morphemes of the word.
            clean_tier (func): To clean the tier.
            clean_word (func): To clean the word.
            clean_morpheme (func): To clean the morpheme.

        Returns:
            list(list): List of list of morphemes (= morpheme word).
        """
        lists = []
        # get the tier
        tier = tier_getter(utterance)
        # clean the tier
        if clean_tier is not None:
            tier = clean_tier(tier)
        # get the words
        words = words_getter(tier)
        for word in words:
            # clean the word
            if clean_word is not None:
                word = clean_word(word)
            # get the morphemes
            morphemes = []
            for morpheme in morphemes_getter(word):
                # clean the morpheme
                if clean_morpheme is not None:
                    morpheme = clean_morpheme(morpheme)
                morphemes.append(morpheme)

            lists.append(morphemes)

        return lists

    @staticmethod
    def struct_eqv(xs, ys):
        """Test whether two lists have the same nested structure."""
        if len(xs) == len(ys):
            for x, y in zip(xs, ys):
                if isinstance(x, list) or isinstance(y, list):
                    if not (isinstance(x, list) and isinstance(y, list)):
                        return False
                    else:
                        if not ToolboxReader.struct_eqv(x, y):
                            return False
            return True
        else:
            return False

    def get_all_morphemes(self, utt):
        """Get list of lists of morphemes.

        Each morpheme is a dict of key-value pairs.

        Args:
            utt (dict): The utterance.

        Returns:
            list: Lists that contain dictionary of morphemes.
        """
        result = []
        self.warnings = []

        # get segments
        segments = self.get_list_of_list_morphemes(
            utt, self.get_seg_tier, self.get_seg_words, self.get_segs,
            self.clean_seg_tier, self.clean_seg_word, self.clean_seg)
        # get glosses
        glosses = self.get_list_of_list_morphemes(
            utt, self.get_gloss_tier, self.get_gloss_words, self.get_glosses,
            self.clean_gloss_tier, self.clean_gloss_word, self.clean_gloss)
        # get parts-of-spech tags
        poses = self.get_list_of_list_morphemes(
            utt, self.get_pos_tier, self.get_pos_words, self.get_poses,
            self.clean_pos_tier, self.clean_pos_word, self.clean_pos)
        # get morpheme languages
        langs = self.get_list_of_list_morphemes(
            utt, self.get_lang_tier, self.get_lang_words, self.get_langs,
            self.clean_lang_tier, self.clean_lang_word, self.clean_lang)
        # get morpheme dict IDs
        morphids = self.get_list_of_list_morphemes(
            utt, self.get_id_tier, self.get_id_words, self.get_ids,
            self.clean_morph_tier, self.clean_morpheme_word,
            self.clean_morpheme)

        # remove morpheme language tier (as it is not part of the DB)
        if 'morpheme_lang' in utt:
            del utt['morpheme_lang']

        len_mw = len(glosses)
        # len_align = len([i for gw in glosses for i in gw])
        tiers = []
        for t in (segments, glosses, poses, langs, morphids):
            if self.struct_eqv(t, glosses):
                tiers.append(t)
            else:
                tiers.append([[] for _ in range(len_mw)])
                self.logger.info("Length of glosses and {} don't match in the "
                            "Toolbox file: {}".format(
                                t, utt['source_id']))
        # This bit adds None (NULL in the DB) for any mis-alignments
        # tiers = list(zip_longest(morphemes, glosses, poses, fillvalue=[]))
        # gls = [m for m in w for w in
        mwords = zip(*tiers)
        for mw in mwords:
            alignment = list(zip_longest(mw[0], mw[1], mw[2], mw[3], mw[4],
                                         fillvalue=None))
            word_morphemes = []
            for morpheme in alignment:
                # TODO: 'type': move to postprocessing if faster
                # -> what type of morpheme as defined in the corpus .ini
                d = {
                    'morpheme': morpheme[0],
                    'gloss_raw': morpheme[1],
                    'pos_raw': morpheme[2],
                    'morpheme_language': morpheme[3],
                    'lemma_id': morpheme[4],
                    'type': self.config['morphemes']['type'],
                    'warning': None if len(self.warnings) == 0 else
                    " ".join(self.warnings)}
                word_morphemes.append(d)
            result.append(word_morphemes)
        return result

    # ---------- cleaners ----------

    # ---------- utterance ----------

    @staticmethod
    def unify_unknown(utterance):
        return re.sub('xxx?|www|\*{3}', '???', utterance)

    @classmethod
    def clean_utterance(cls, utterance):
        """Clean up corpus-specific utterances.

        Args:
            utterance (str): The raw utterance.

        Returns:
            str: The cleaned utterance.
        """
        if utterance is not None:
            return cls.unify_unknown(utterance)

        return utterance

    # ---------- morphology tiers ----------

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        """No cleaning per default."""
        return morph_tier

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        """No cleaning per default."""
        return cls.clean_morph_tier(seg_tier)

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        """No cleaning per default."""
        return cls.clean_morph_tier(gloss_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        """No cleaning per default."""
        return cls.clean_morph_tier(pos_tier)

    @classmethod
    def clean_lang_tier(cls, lang_tier):
        """No cleaning per default."""
        return cls.clean_morph_tier(lang_tier)

    # ---------- morpheme words ----------

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        """No cleaning per default."""
        return morpheme_word

    @classmethod
    def clean_seg_word(cls, segment_word):
        """No cleaning per default."""
        return cls.clean_morpheme_word(segment_word)

    @classmethod
    def clean_gloss_word(cls, gloss_word):
        """No cleaning per default."""
        return cls.clean_morpheme_word(gloss_word)

    @classmethod
    def clean_pos_word(cls, pos_word):
        """No cleaning per default."""
        return cls.clean_morpheme_word(pos_word)

    @classmethod
    def clean_lang_word(cls, lang_word):
        """No cleaning per default."""
        return cls.clean_morpheme_word(lang_word)

    # ---------- morphemes ----------

    @classmethod
    def clean_morpheme(cls, morpheme):
        """No cleaning per default."""
        return morpheme

    @classmethod
    def clean_seg(cls, segment):
        """No cleaning per default."""
        return cls.clean_morpheme(segment)

    @classmethod
    def clean_gloss(cls, gloss):
        """No cleaning per default."""
        return cls.clean_morpheme(gloss)

    @classmethod
    def clean_pos(cls, pos):
        """No cleaning per default."""
        return cls.clean_morpheme(pos)

    @classmethod
    def clean_lang(cls, lang):
        """No cleaning per default."""
        return lang

    def __repr__(self):
        """Pretty print class name + plus path of session file."""
        return '%s(%r)' % (self.__class__.__name__, self.path)


###############################################################################


class ChintangReader(ToolboxReader):

    def make_rec(self, record):
        utterance, words, morphemes = super().make_rec(record)
        # We infer sentence type from Chintang \nep
        # but we do not add the nepali field to the database yet
        if 'nepali' in utterance:
            del utterance['nepali']

        return utterance, words, morphemes

    def get_childdirected(self, record):
        if 'childdirected' in record:
            tos_raw = record['childdirected']
            if 'directed' in tos_raw:
                if 'child' in tos_raw:
                    return True
                else:
                    return False
            else:
                del record['childdirected']

        return None

    def get_sentence_type(self, record):
        # https://github.com/uzling/acqdiv/issues/253
        # \eng: . = default, ? = question, ! = exclamation
        # \nep: । = default, rest identical.
        # Note this is not a "pipe" but the so-called danda at U+0964
        if ('nepali' in record.keys()
                and record['nepali'] is not None):
            match_punctuation = re.search('([।?!])$', record['nepali'])
            if match_punctuation is not None:
                sentence_type = None
                if match_punctuation.group(1) == '।':
                    sentence_type = 'default'
                if match_punctuation.group(1) == '?':
                    sentence_type = 'question'
                if match_punctuation.group(1) == '!':
                    sentence_type = 'exclamation'
                return sentence_type
        elif ('eng' in record.keys()
              and record['translation'] is not None):
            match_punctuation = re.search('([।?!])$',
                                          record['translation'])
            if match_punctuation is not None:
                sentence_type = None
                if match_punctuation.group(1) == '.':
                    sentence_type = 'default'
                if match_punctuation.group(1) == '?':
                    sentence_type = 'question'
                if match_punctuation.group(1) == '!':
                    sentence_type = 'exclamation'
                return sentence_type
        else:
            return None

    @staticmethod
    def remove_punctuation(seg_tier):
        return re.sub('[‘’\'“”\".!,:?+/]', '', seg_tier)

    @staticmethod
    def unify_unknown(seg_tier):
        return re.sub('\*\*\*', '???', seg_tier)

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        for cleaning_method in [cls.remove_punctuation, cls.unify_unknown]:
            seg_tier = cleaning_method(seg_tier)

        return seg_tier

    @staticmethod
    def remove_floating_clitic(morpheme_word):
        # TODO: double check this logic is correct with Robert
        return morpheme_word.replace(" - ", " ")

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        return cls.remove_floating_clitic(morpheme_word)

    def clean_lang(self, lang):
        lang = lang.strip('-')
        if lang in self.config['languages']:
            return self.config['languages'][lang]
        else:
            return 'Chintang'


###############################################################################


class IndonesianReader(ToolboxReader):

    def make_rec(self, record):
        utterance, words, morphemes = super().make_rec(record)
        if utterance:
            if 'speaker_label' in utterance:
                if utterance['speaker_label'] == '@PAR':
                    return None, None, None

        return utterance, words, morphemes

    def get_words(self, utterance):
        result = []
        words = utterance.split()

        for word in words:
            d = {}
            # Distinguish between word and word_target;
            # otherwise the target word is identical to the actual word:
            # https://github.com/uzling/acqdiv/blob/master/extraction
            # /parsing/corpus_parser_functions.py#L1859-L1867
            # Also: xx(x), www and *** is garbage from chat
            if re.search('\(', word):
                d['word_target'] = re.sub('[()]', '', word)
                d['word'] = re.sub('\([^)]+\)', '', word)
                d['word_actual'] = d['word']
                result.append(d)
            else:
                d['word_target'] = re.sub('xxx?|www', '???', word)
                d['word'] = re.sub('xxx?', '???', word)
                d['word_actual'] = d['word']
                result.append(d)

        return result

    def get_sentence_type(self, record):
        if re.search('\.', record['utterance_raw']):
            return 'default'
        elif re.search('\?\s*$', record['utterance_raw']):
            return 'question'
        elif re.search('!', record['utterance_raw']):
            return 'imperative'
        else:
            return None

    def get_warnings(self, utterance):
        # Insecure transcription [?], add warning, delete marker
        # cf. https://github.com/uzling/acqdiv/blob/master/
        # extraction/parsing/corpus_parser_functions.py#L1605-1610
        if re.search('\[\?\]', utterance):
            # TODO: what's that used for?
            # utterance = re.sub('\[\?\]', '', utterance)
            transcription_warning = 'transcription insecure'
            return transcription_warning

        return None

    def clean_utterance(self, utterance):
        utterance = super().clean_utterance(utterance)

        if utterance is not None:
            # TODO: () are not stripped (-> might interfer with
            # actual vs. target distinction)
            # delete punctuation and garbage
            utterance = re.sub('[‘’\'“”\".!,;:+/]|\?$|<|>', '', utterance)
            utterance = utterance.strip()

            # Insecure transcription [?], add warning, delete marker
            if re.search('\[\?\]', utterance):
                utterance = re.sub('\[\?\]', '', utterance)

        return utterance

    @staticmethod
    def remove_punctuation(morpheme_tier):
        return re.sub('[‘’\'“”\".!,:?+/]', '', morpheme_tier)

    @staticmethod
    def unify_unknown(morpheme_tier):
        return re.sub('xxx?|www', '???', morpheme_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        for cleaning_method in [cls.remove_punctuation, cls.unify_unknown]:
            morph_tier = cleaning_method(morph_tier)
        return morph_tier

    @classmethod
    def get_lang_tier(cls, utterance):
        return utterance.get('gloss_raw')

    @classmethod
    def get_langs(cls, morpheme_lang_word):
        return ['Indonesian' for _ in cls.get_morphemes(morpheme_lang_word)]

    # TODO: extract relevant source 'nt' (comment) field?

###############################################################################


class RussianReader(ToolboxReader):

    def get_warnings(self, utterance):
        if re.search('\[(\s*=?.*?|\s*xxx\s*)\]', utterance):
            for target in re.findall('\[=\?\s+[^\]]+\]', utterance):
                target_clean = re.sub('["\[\]?=]', '', target)
                transcription_warning = (
                    'transcription insecure (intended '
                    'form might have been "' + target_clean + '")')
                return transcription_warning

        return None

    def make_rec(self, record):
        utterance, words, morphemes = super().make_rec(record)
        utterance['gloss_raw'] = ' '.join(
            mor['gloss_raw'] for mword in morphemes for mor in mword)

        return utterance, words, morphemes

    def clean_utterance(self, utterance):
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

    @classmethod
    def get_gloss_tier(cls, utterance):
        return utterance.get('pos_raw', '')

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
    def get_lang_tier(cls, utterance):
        return utterance.get('pos_raw')

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


def main():
    from acqdiv.parsers.parsers import CorpusConfigParser

    cfg = CorpusConfigParser()
    cfg.read("ini/Chintang.ini")
    f = "tests/corpora/Chintang/Toolbox/Chintang.txt"
    # cfg.read("Russian.ini")
    # f = "../../corpora/Russian/toolbox/A00210817.txt"
    t = ToolboxReader(cfg, f)
    for record in t:
        print(record)
        # for k, v in record.items():
        #    print(k, "\t", v)


if __name__ == "__main__":
    main()
