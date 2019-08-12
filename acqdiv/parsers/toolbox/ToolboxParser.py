from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader
from acqdiv.parsers.metadata.IMDIParser import IMDIParser
from acqdiv.parsers.toolbox.cleaners.ToolboxCleaner import ToolboxCleaner
from acqdiv.parsers.toolbox.readers.ToolboxFileParser import ToolboxFileParser
from acqdiv.parsers.SessionParser import SessionParser
from acqdiv.model.Session import Session
from acqdiv.model.Speaker import Speaker
from acqdiv.model.Utterance import Utterance
from acqdiv.model.Word import Word
from acqdiv.model.Morpheme import Morpheme

import os


class ToolboxParser(SessionParser):
    """Gathers all data for the DB for a given Toolbox session file.

    Uses the ToolboxReader for reading a toolbox file and
    IMDIParser or CHATParser for reading the corresponding metadata file.
    """

    def get_record_reader(self):
        return ToolboxReader()

    def get_metadata_reader(self):
        return IMDIParser(self.metadata_path)

    def get_cleaner(self):
        return ToolboxCleaner()

    def __init__(self, toolbox_path, metadata_path):
        """Get toolbox and metadata readers.

        Args:
            toolbox_path (str): Path to the toolbox file.
            metadata_path (str): Path to the metadata file.
        """
        self.session = Session()

        self.metadata_path = metadata_path
        self.toolbox_path = toolbox_path

        # get record reader
        self.record_reader = self.get_record_reader()
        # get metadata reader
        self.metadata_reader = self.get_metadata_reader()
        # get cleaner
        self.cleaner = self.get_cleaner()

    def parse(self):
        """Get the session instance.

        Returns:
            acqdiv.model.Session.Session: The Session instance.
        """
        self.add_session_metadata()
        self.add_speakers()
        self.add_record()

        return self.session

    def get_media_filenames(self):
        md = self.metadata_reader.metadata

        media_filenames = set()

        for mediafile in md['media']['mediafile']:
            link = mediafile['resourcelink']
            filename = os.path.basename(link)
            filename_without_ext = os.path.splitext(filename)[0]
            media_filenames.add(filename_without_ext)

        return ','.join(name for name in media_filenames)

    def add_session_metadata(self):
        """Add the metadata of a session."""
        self.session.source_id = os.path.splitext(
            os.path.basename(self.toolbox_path))[0]
        self.session.date = self.metadata_reader.metadata['session'].get(
            'date', None)
        self.session.media_filename = self.get_media_filenames()

    def add_speakers(self):
        """Add the speakers of a session."""
        for speaker_dict in self.metadata_reader.metadata['participants']:
            speaker = Speaker()
            speaker.session = self.session
            speaker.birth_date = speaker_dict.get('birthdate', None)
            speaker.gender_raw = speaker_dict.get('sex', None)
            speaker.code = speaker_dict.get('code', None)
            speaker.age_raw = speaker_dict.get('age', None)
            speaker.role_raw = speaker_dict.get('role', None)
            speaker.name = speaker_dict.get('name', None)
            speaker.languages_spoken = speaker_dict.get('languages', None)

            self.session.speakers.append(speaker)

    def add_record(self):
        """
        """
        separator = self.record_reader.get_rec_separator()
        toolbox_file = ToolboxFileParser.parse(self.toolbox_path, separator)

        for rec in toolbox_file.records:

            if self.record_reader.is_record(rec):

                rec = self.cleaner.cross_clean(rec)

                self.add_utterance(rec)

                actual_utterance = self.cleaner.clean_utterance(
                    self.record_reader.get_actual_utterance(rec))
                target_utterance = self.cleaner.clean_utterance(
                    self.record_reader.get_target_utterance(rec))
                self.add_words(actual_utterance, target_utterance)

                self.add_morphemes(
                    self.record_reader.get_seg_tier(rec),
                    self.record_reader.get_gloss_tier(rec),
                    self.record_reader.get_pos_tier(rec),
                    self.record_reader.get_lang_tier(rec),
                    self.record_reader.get_id_tier(rec)
                )

    def add_utterance(self, rec):
        """Add the utterance to the Session instance.

        Args:
            rec (acqdiv.parsers.toolbox.model.Record.Record): The record.
        """
        utt = Utterance()
        self.session.utterances.append(utt)
        utt.session = self.session

        utt.speaker_label = self.record_reader.get_speaker_label(rec)
        utt.addressee = self.record_reader.get_addressee(rec)
        utt.utterance_raw = self.record_reader.get_actual_utterance(rec)
        utt.utterance = self.cleaner.clean_utterance(utt.utterance_raw)
        utt.sentence_type = self.record_reader.get_sentence_type(rec)
        utt.childdirected = self.record_reader.get_childdirected(rec)
        utt.source_id = self.record_reader.get_source_id(rec)
        utt.start_raw = self.record_reader.get_start_raw(rec)
        utt.end_raw = self.record_reader.get_end_raw(rec)
        utt.translation = self.record_reader.get_translation(rec)
        utt.comment = self.record_reader.get_comment(rec)
        utt.morpheme = self.record_reader.get_seg_tier(rec)
        utt.gloss_raw = self.record_reader.get_gloss_tier(rec)
        utt.pos_raw = self.record_reader.get_pos_tier(rec)

    def add_words(self, actual_utterance, target_utterance):
        """Get list of words from the utterance.

        Args:
            actual_utterance (str): The clean actual utterance.
            target_utterance (str): The clean target utterance.
        """
        words = self.record_reader.get_words(actual_utterance)
        utterance = self.session.utterances[-1]

        for word in words:
            w = Word()
            w.utterance = utterance
            utterance.words.append(w)

            word_clean = self.cleaner.clean_word(word)

            w.word = word_clean
            w.word_actual = w.word
            w.word_target = ''
            w.word_language = ''

    def add_morphemes(
            self, seg_tier, gloss_tier, pos_tier, lang_tier, id_tier):
        # clean morphology tiers
        seg_tier = self.cleaner.clean_seg_tier(seg_tier)
        gloss_tier = self.cleaner.clean_gloss_tier(gloss_tier)
        pos_tier = self.cleaner.clean_pos_tier(pos_tier)
        lang_tier = self.cleaner.clean_lang_tier(lang_tier)
        id_tier = self.cleaner.clean_morph_tier(id_tier)

        # get morpheme words from the respective morphology tiers
        wsegs = self.record_reader.get_seg_words(seg_tier)
        wglosses = self.record_reader.get_gloss_words(gloss_tier)
        wposes = self.record_reader.get_pos_words(pos_tier)
        wlangs = self.record_reader.get_lang_words(lang_tier)
        wids = self.record_reader.get_id_words(id_tier)

        # determine number of words to be considered based on
        # main morphology tier and existence of this morphology tier
        if self.record_reader.get_main_morpheme() == 'segment':
            wlen = len(wsegs)
            # segment tier does not exist
            if not wlen:
                wlen = len(wglosses)
        else:
            wlen = len(wglosses)
            # gloss tier does not exist
            if not wlen:
                wlen = len(wsegs)

        # if both segment and gloss tier do not exists, take the pos tier
        if not wlen:
            wlen = len(wposes)

        # check for wm-misalignments between morphology tiers
        # if misaligned, replace by a list of empty strings
        if wlen != len(wsegs):
            wsegs = wlen * ['']
        if wlen != len(wglosses):
            wglosses = wlen * ['']
        if wlen != len(wposes):
            wposes = wlen * ['']
        if wlen != len(wlangs):
            wlangs = wlen * ['']
        if wlen != len(wids):
            wids = wlen * ['']

        utt = self.session.utterances[-1]

        # go through all morpheme words
        for wseg, wgloss, wpos, wlang, wid in zip(
                wsegs, wglosses, wposes, wlangs, wids):

            cleaned_wseg = self.cleaner.clean_seg_word(wseg)
            cleaned_wgloss = self.cleaner.clean_gloss_word(wgloss)
            cleaned_wpos = self.cleaner.clean_pos_word(wpos)
            cleaned_wlang = self.cleaner.clean_lang_word(wlang)
            cleaned_wid = self.cleaner.clean_morpheme_word(wid)

            # collect morpheme data of a word
            wmorphemes = []

            # get morphemes from the morpheme words
            segments = self.record_reader.get_segs(cleaned_wseg)
            glosses = self.record_reader.get_glosses(cleaned_wgloss)
            poses = self.record_reader.get_poses(cleaned_wpos)
            langs = self.record_reader.get_langs(cleaned_wlang)
            ids = self.record_reader.get_ids(cleaned_wid)

            # determine number of morphemes to be considered
            if self.record_reader.get_main_morpheme() == 'segment':
                mlen = len(segments)
                if not mlen:
                    mlen = len(glosses)
            else:
                mlen = len(glosses)
                if not mlen:
                    mlen = len(segments)

            # if both segment and gloss do not exists, take the pos
            if not mlen:
                mlen = len(poses)

            # check for mm-misalignments between morphology tiers
            # if misaligned, replace by a list of empty strings
            if mlen != len(segments):
                segments = mlen * ['']
            if mlen != len(glosses):
                glosses = mlen * ['']
            if mlen != len(poses):
                poses = mlen * ['']
            if mlen != len(langs):
                langs = mlen * ['']
            if mlen != len(ids):
                ids = mlen * ['']

            # go through morphemes
            for seg, gloss, pos, lang, id_ in zip(
                    segments, glosses, poses, langs, ids):

                m = Morpheme()
                m.utterance = utt

                # clean the morphemes
                m.morpheme = self.cleaner.clean_seg(seg)
                m.gloss_raw = self.cleaner.clean_gloss_raw(gloss)
                m.gloss = self.cleaner.clean_gloss(m.gloss_raw)
                m.pos_raw = self.cleaner.clean_pos_raw(pos)
                m.pos = self.cleaner.clean_pos(m.pos_raw)
                m.morpheme_language = self.cleaner.clean_lang(lang)
                m.lemma_id = self.cleaner.clean_id(id_)
                m.warning = ''
                m.type = self.record_reader.get_morpheme_type()

                wmorphemes.append(m)

            utt.morphemes.append(wmorphemes)
