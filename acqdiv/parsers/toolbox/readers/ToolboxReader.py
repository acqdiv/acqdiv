# -*- coding: utf-8 -*-
"""Generic Reader for toolbox files."""

import re
import mmap
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

    warnings = []
    language = 'Undefined'

    def __init__(self, file_path):
        """Initializes a Toolbox file object.

        Args:
            file_path (str): The path of the session file.
        """
        self.path = file_path

    def __iter__(self):
        """Yield utterance, words, morphemes a session transcript file.

        This iterator directly extracts utterances for the DB column
        utterance_raw and calls various functions to extract information from
        the following levels:

        - get_sentence_type: Extract the sentence type.
        - clean_utterance: Clean up the utterance.
        - add_utterance_warnings: Get warnings like "transcription insecure".
        - get_words_data: Extract words in an utterance for the words table.
        - get_morphemes: Extract the morphemes in a word for the morphemes
                         table.

        Note:
            The record marker needs to be updated if the corpus doesn't use
            "\ref" for record markers.

        Yields:
            tuple:
                utterance: {}
                words: [{},{}...]
                morphemes: [[{},{}...], [{},{}...]...]
        """
        with open(self.path, 'rb') as f:
            for record in self.iter_records(f):
                yield self.make_rec(record)

    @staticmethod
    def iter_records(toolbox_file):
        """Iter the records of a toolbox file.

        Args:
            toolbox_file (file/file-like): The toolbox file.

        Yields:
            str: The record.
        """
        _record_marker = re.compile(br'\\ref')

        with contextlib.closing(mmap.mmap(toolbox_file.fileno(),
                                          0, access=mmap.ACCESS_READ)) as data:
            ma = _record_marker.search(data)
            # Skip the first rows that contain metadata information:
            # https://github.com/uzling/acqdiv/issues/154
            # TODO: what's that used for?
            # header = data[:ma.start()].decode()
            pos = ma.start()
            for ma in _record_marker.finditer(data, ma.end()):
                yield data[pos:ma.start()].decode()
                pos = ma.start()

            if ma is None:
                raise StopIteration
            else:
                yield data[pos:].decode()

    @classmethod
    def make_rec(cls, record):
        """Parse and make utterance, words and morpheme structures.

        Args:
          record (str): Toolbox record.

        Returns:
          tuple: (utterance, words, morphemes)
        """
        rec_dict = cls.get_record_dict(record)

        if not cls.is_record(rec_dict):
            return None, None, None
        else:
            utterance = cls.get_utterance_data(rec_dict)
            words = cls.get_words_data(rec_dict)

            # TODO: morphemes are nulled if there is no utterance, is this OK?
            if utterance['utterance']:
                morphemes = cls.get_morphemes_data(rec_dict)
                cls.add_word_language(words, morphemes)
                cls.fix_wm_misalignments(words, morphemes)
            else:
                morphemes = []

            cls.null_empty_values(utterance)

            return utterance, words, morphemes

    @classmethod
    def get_record_dict(cls, record):
        """Get the record dictionary.

        Metadata is ignored and returned as an empty dictionary.

        Args:
            record (str): Toolbox record.

        Returns:
            dict: Key and content of tiers.
        """
        rec_dict = {}

        # iter tiers of the record
        for tier in cls.get_tiers(record):
            # get field marker and content of tier
            field_marker, content = cls.get_tier(tier)
            # clean the content
            content = cls.remove_redundant_whitespaces(content)

            # add content to dictionary
            rec_dict[field_marker] = content

        return rec_dict

    @staticmethod
    def get_tiers(record):
        """Return tiers of the record.

        Args:
            record (str): The record.

        Returns:
            list: The tiers of the record.
        """
        return record.split('\n')

    @staticmethod
    def get_tier(tier):
        """Return field marker and content.

        Args:
            tier (str): '\\name content'.

        Returns:
            tuple: (name, content).
        """
        # split into field marker and content
        tokens = re.split(r'\s+', tier, maxsplit=1)
        # get field marker
        field_marker = tokens[0]
        # remove \\ before the field marker
        field_marker = field_marker.replace("\\", "")

        # if content is missing
        if len(tokens) <= 1:
            content = ''
        else:
            content = tokens[1]

        return field_marker, content

    @staticmethod
    def remove_redundant_whitespaces(string):
        """Remove redundant whitespaces."""
        string = re.sub(r'\s+', ' ', string)
        string = string.strip()
        return string

    @classmethod
    def is_record(cls, rec_dict):
        """Is the record really a record or just metadata?"""
        for tier in rec_dict:
            content = rec_dict[tier]

            if content.startswith('@'):
                return False

        return True

    # ---------- utterance data ----------

    @classmethod
    def get_utterance_data(cls, rec_dict):
        """Get the utterance dictionary.

        Extracts all fields from the record dictionary relevant for the DB.

        Args:
            rec_dict (dict): The record dictionary.

        Returns:
            dict: The utterance dictionary.
        """
        cls.warnings = []

        # get utterance data
        speaker_label = cls.get_speaker_label(rec_dict)
        addressee = cls.get_addressee(rec_dict)
        utterance_raw = cls.get_utterance_raw(rec_dict)
        utterance_clean = cls.clean_utterance(utterance_raw)
        sentence_type = cls.get_sentence_type(rec_dict)
        child_directed = cls.get_childdirected(rec_dict)
        source_id = cls.get_source_id(rec_dict)
        start_raw = cls.get_start_raw(rec_dict)
        end_raw = cls.get_end_raw(rec_dict)
        translation = cls.get_translation(rec_dict)
        comment = cls.get_comment(rec_dict)
        morpheme = cls.get_seg_tier(rec_dict)
        gloss_raw = cls.get_gloss_tier(rec_dict)
        pos_raw = cls.get_pos_tier(rec_dict)

        cls.add_utterance_warnings(utterance_raw)
        warning = cls.get_warning()

        utterance = {
            'speaker_label': speaker_label,
            'addressee': addressee,
            'utterance_raw': utterance_raw,
            'utterance': utterance_clean,
            'sentence_type': sentence_type,
            'childdirected': child_directed,
            'source_id': source_id,
            'start_raw': start_raw,
            'end_raw': end_raw,
            'translation': translation,
            'comment': comment,
            'warning': warning,
            'morpheme': morpheme,
            'gloss_raw': gloss_raw,
            'pos_raw': pos_raw
        }

        return utterance

    @classmethod
    def get_source_id(cls, rec_dict):
        return rec_dict.get('ref', '')

    @classmethod
    def get_speaker_label(cls, rec_dict):
        return rec_dict.get('ELANParticipant', '')

    @classmethod
    def get_addressee(cls, rec_dict):
        return rec_dict.get('add', '')

    @classmethod
    def get_start_raw(cls, rec_dict):
        return rec_dict.get('ELANBegin', '')

    @classmethod
    def get_end_raw(cls, rec_dict):
        return rec_dict.get('ELANEnd', '')

    @classmethod
    def get_utterance_raw(cls, rec_dict):
        return rec_dict.get('tx', '')

    @classmethod
    def get_sentence_type(cls, rec_dict):
        """Get utterance type (aka sentence type) of an utterance.

        Possible values:
            - default (.)
            - question (?)
            - imperative or exclamation (!)

        Args:
            rec_dict (dict): The record.

        Returns:
            str: The sentence type.
        """
        utterance_raw = cls.get_utterance_raw(rec_dict)
        match_punctuation = re.search('([.?!])$', utterance_raw)
        if match_punctuation is not None:
            if match_punctuation.group(1) == '.':
                return 'default'
            elif match_punctuation.group(1) == '?':
                return 'question'
            elif match_punctuation.group(1) == '!':
                return 'imperative'

        return ''

    @classmethod
    def get_childdirected(cls, rec_dict):
        """Not coded per default.

        Args:
            rec_dict (dict): The record.
        """
        return None

    @classmethod
    def get_translation(cls, rec_dict):
        return rec_dict.get('eng', '')

    @classmethod
    def get_comment(cls, rec_dict):
        return rec_dict.get('comment', '')

    @classmethod
    def get_warning(cls):
        if cls.warnings:
            return "Empty value in the input for: " + ", ".join(cls.warnings)
        else:
            return ''

    @classmethod
    def add_utterance_warnings(cls, utterance):
        """No warnings per default.

        Args:
            utterance (str): The utterance.
        """
        pass

    # ---------- words data ----------

    @classmethod
    def get_words_data(cls, rec_dict):
        """Get list of words from the utterance.

        Each word is a dictionary of key-value pairs.

        Args:
            rec_dict (dict): The record dictionary.

        Returns:
            list(dict): The list of words as dictionaries.
        """
        result = []
        utterance = cls.get_utterance_raw(rec_dict)
        utterance_clean = cls.clean_utterance(utterance)
        words = cls.get_words(utterance_clean)

        for word in words:
            word_clean = cls.clean_word(word)
            d = {
                'word': word_clean,
                'word_actual': word
            }
            result.append(d)
        return result

    @classmethod
    def get_words(cls, utterance):
        return utterance.split()

    # ---------- morphemes data ----------

    @classmethod
    def get_morphemes_data(cls, rec_dict):
        """Get list of lists of morphemes.

        Each morpheme is a dict of key-value pairs.

        Args:
            rec_dict (dict): The utterance.

        Returns:
            list: Lists that contain dictionaries of morphemes.
        """
        cls.warnings = []
        morphology_data = cls.get_morphology_data(rec_dict)
        fixed_morphology_data = cls.fix_mm_misalignments(morphology_data)

        morphemes_dict = []
        mwords = zip(*fixed_morphology_data)
        for mw in mwords:
            alignment = list(zip_longest(*mw, fillvalue=None))
            word_morphemes = []
            for morpheme in alignment:
                d = cls.get_morpheme_dict(morpheme)
                word_morphemes.append(d)
            morphemes_dict.append(word_morphemes)

        return morphemes_dict

    @classmethod
    def get_morphology_data(cls, rec_dict):
        """Get morphology data.

        This method returns at a minimum segments, glosses, POS tags and the
        languages. It can additionally return other morphology data such as the
        morpheme dictionary IDs.

        Args:
            rec_dict (dict): The record dictionary.

        Returns:
            tuple: (segments, glosses, poses, languages, *)
        """
        # get segments
        segments = cls.get_list_of_list_morphemes(
            rec_dict, cls.get_seg_tier, cls.get_seg_words, cls.get_segs,
            cls.clean_seg_tier, cls.clean_seg_word, cls.clean_seg)
        # get glosses
        glosses = cls.get_list_of_list_morphemes(
            rec_dict, cls.get_gloss_tier, cls.get_gloss_words,
            cls.get_glosses, cls.clean_gloss_tier, cls.clean_gloss_word,
            cls.clean_gloss)
        # get parts-of-spech tags
        poses = cls.get_list_of_list_morphemes(
            rec_dict, cls.get_pos_tier, cls.get_pos_words, cls.get_poses,
            cls.clean_pos_tier, cls.clean_pos_word, cls.clean_pos)
        # get morpheme languages
        langs = cls.get_list_of_list_morphemes(
            rec_dict, cls.get_lang_tier, cls.get_lang_words, cls.get_langs,
            cls.clean_lang_tier, cls.clean_lang_word, cls.clean_lang)

        return segments, glosses, poses, langs

    # ---------- morpheme tier ----------

    @classmethod
    def get_seg_tier(cls, rec_dict):
        return rec_dict.get('mb', '')

    @classmethod
    def get_gloss_tier(cls, rec_dict):
        return rec_dict.get('ge', '')

    @classmethod
    def get_pos_tier(cls, rec_dict):
        return rec_dict.get('ps', '')

    @classmethod
    def get_lang_tier(cls, rec_dict):
        return rec_dict.get('lg', '')

    # ---------- morpheme words ----------

    @classmethod
    def get_morpheme_words(cls, morpheme_tier):
        _word_boundary = re.compile('(?<![(\-|=)\s])\s+(?![(\-|=)\s])')

        if morpheme_tier:
            return re.split(_word_boundary, morpheme_tier)
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
    def get_list_of_list_morphemes(
            cls, rec_dict, tier_getter, words_getter, morphemes_getter,
            clean_tier=None, clean_word=None, clean_morpheme=None):
        """Get list of list of morphemes.

        Args:
            rec_dict (dict): The record dictionary containing the tiers.
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
        tier = tier_getter(rec_dict)
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

    @classmethod
    def fix_mm_misalignments(cls, morphology_data):
        """Fix morpheme misalignments in the morphology data.

        The gloss tier is used for comparison. If there are any misalignments
        between the gloss and another morphology tier, then the values of
        the morpohlogy tier are deleted. In the case of morpheme language,
        the default language will be used.

        Args:
            morphology_data (tuple): (segments, glosses, poses, languages, *)

        Returns:
            tuple: (segments, glosses, poses, languages, *)
        """
        glosses = morphology_data[1]
        len_mw = len(glosses)
        fixed_morphology_data = []
        # for each type of morphology tier
        for i, t in enumerate(morphology_data):
            # check if there are misalignments
            if cls.struct_eqv(t, glosses):
                fixed_morphology_data.append(t)
            else:
                # set a default language
                if i == 3:
                    fixed_morphology_data.append(
                        [[cls.language] for _ in range(len_mw)])
                else:
                    # null all values
                    fixed_morphology_data.append(
                        [[] for _ in range(len_mw)])

        return tuple(fixed_morphology_data)

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

    @classmethod
    def get_morpheme_dict(cls, morpheme):
        """Get the morpheme dictionary.

        Args:
            morpheme(tuple): (segment, glosse, pos, language, *)

        Returns:
            dict: Every morpheme values mapped to a dictionary key.
        """
        d = {
            'morpheme': morpheme[0],
            'gloss_raw': morpheme[1],
            'pos_raw': morpheme[2],
            'morpheme_language': morpheme[3],
            'type': cls.get_morpheme_type(),
            'warning': " ".join(cls.warnings) if cls.warnings else None
        }

        return d

    @staticmethod
    def get_morpheme_type():
        return 'target'

    # ---------- miscellaneous ----------

    @classmethod
    def add_word_language(cls, words, morphemes):
        for i in range(len(words)):
            try:
                words[i]['word_language'] = \
                    morphemes[i][0]['morpheme_language']
            except IndexError:
                break

    @classmethod
    def fix_wm_misalignments(cls, words, morphemes):
        """Fix words less than morphemes misalignments."""
        if len(morphemes) - len(words) > 0:
            misalignment = len(morphemes) - len(words)
            for i in range(0, misalignment):
                words.append({})

    @staticmethod
    def null_empty_values(dictionary):
        for key in dictionary:
            if dictionary[key] == '':
                dictionary[key] = None

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
        return cls.unify_unknown(utterance)

    # ---------- utterance word ----------

    @classmethod
    def clean_word(cls, word):
        return cls.unify_unknown(word)

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
        return cls.clean_morpheme(lang)

    def __repr__(self):
        """Pretty print class name + plus path of session file."""
        return '%s(%r)' % (self.__class__.__name__, self.path)
