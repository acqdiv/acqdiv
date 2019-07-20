import os

from acqdiv.parsers.chat.readers.CHATReader import CHATReader
from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner
from acqdiv.parsers.SessionParser import SessionParser
from acqdiv.model.Session import Session
from acqdiv.model.Speaker import Speaker
from acqdiv.model.Utterance import Utterance
from acqdiv.model.Word import Word
from acqdiv.model.Morpheme import Morpheme


class CHATParser(SessionParser):
    """Gathers all data for the DB for a given CHAT session file.

    Uses the CHATReader for reading and inferring data from the CHAT file and
    CHATCleaner for cleaning these data.
    """

    def __init__(self, session_path):
        self.session = Session()

        self.session_path = session_path
        self.session_filename = os.path.basename(self.session_path)

        with open(session_path) as session_file:
            self.reader = self.get_reader(session_file)

        self.cleaner = self.get_cleaner()
        self.consistent_actual_target = True

    @staticmethod
    def get_reader(session_file):
        """Return a CHATReader instance.

        Returns:
            acqdiv.parsers.chat.readers.CHATReader.CHATReader:
            The reader instance.
        """
        return CHATReader(session_file)

    @staticmethod
    def get_cleaner():
        """Return a CHATCleaner instance.

        Returns:
            acqdiv.parsers.chat.cleaners.CHATCleaner.CHATCleaner:
            The cleaner instance.
        """
        return CHATCleaner()

    def parse(self):
        """Get the session instance.

        Returns:
            acqdiv.model.Session.Session: The Session instance.
        """
        self.add_session_metadata()
        self.add_speakers()
        self.add_records()

        return self.session

    def add_session_metadata(self):
        """Add the metadata of a session."""
        session = self.session

        date = self.cleaner.clean_date(self.reader.get_session_date())
        media_filename = self.reader.get_session_media_filename()

        # any corrections of the metadata
        date, media_filename = self.cleaner.clean_session_metadata(
            self.session_filename, date, media_filename)

        session.source_id = os.path.splitext(self.session_filename)[0]
        session.date = date if date else None
        session.media_filename = media_filename if media_filename else None

    def add_speakers(self):
        """Add the speakers of a session."""
        while self.reader.load_next_speaker():
            speaker = Speaker()

            speaker_label = self.reader.get_speaker_label()
            name = self.reader.get_speaker_name()
            role = self.reader.get_speaker_role()
            age = self.reader.get_speaker_age()
            gender = self.reader.get_speaker_gender()
            language = self.reader.get_speaker_language()
            birth_date = self.cleaner.clean_date(
                                self.reader.get_speaker_birthdate())
            target_child = self.reader.get_target_child()

            # any corrections of the metadata
            speaker_label, name, role, age, gender, language, birth_date = \
                self.cleaner.clean_speaker_metadata(
                    self.session_filename, speaker_label, name, role, age,
                    gender, language, birth_date, target_child)

            speaker.code = speaker_label
            speaker.name = name if name else None
            speaker.age_raw = age if age else None
            speaker.gender_raw = gender if gender else None
            speaker.role_raw = role
            speaker.languages_spoken = language if language else None
            speaker.birth_date = birth_date if birth_date else None

            self.session.speakers.append(speaker)

    def add_words(self, actual_utt, target_utt):
        actual_words = self.reader.get_utterance_words(actual_utt)
        target_words = self.reader.get_utterance_words(target_utt)

        utt = self.session.utterances[-1]

        for word_actual, word_target in zip(actual_words, target_words):

            w = Word()
            w.utterance = utt
            utt.words.append(w)

            if self.reader.get_standard_form() == 'actual':
                word = word_actual
            else:
                word = word_target

            w.word_language = self.reader.get_word_language(word)
            w.word = self.cleaner.clean_word(word)
            w.word_actual = self.cleaner.clean_word(word_actual)
            w.word_target = self.cleaner.clean_word(word_target)
            w.warning = ''

            if not self.consistent_actual_target:
                if word_actual == word_target:
                    w.word_actual = None
                    w.word_target = None

    def add_records(self):
        """
        """
        while self.reader.load_next_record():
            utt = Utterance()
            utt.session = self.session
            self.session.utterances.append(utt)

            utt.source_id = self.get_source_id()
            utt.addressee = self.cleaner.clean_record_speaker_label(
                self.session_filename, self.reader.get_addressee())
            utt.translation = self.cleaner.clean_translation(
                                self.reader.get_translation())
            utt.comment = self.reader.get_comments()
            utt.speaker_label = self.cleaner.clean_record_speaker_label(
                self.session_filename, self.reader.get_record_speaker_label())
            utt.utterance_raw = self.reader.get_utterance()
            utt.start_raw = self.reader.get_start_time()
            utt.end_raw = self.reader.get_end_time()
            utt.sentence_type = self.reader.get_sentence_type()
            utt.warning = ''

            # actual & target distinction
            actual_utt = self.cleaner.clean_utterance(
                self.reader.get_actual_utterance())
            target_utt = self.cleaner.clean_utterance(
                self.reader.get_target_utterance())

            # get morphology tiers
            utt.morpheme = self.reader.get_seg_tier()
            utt.gloss_raw = self.reader.get_gloss_tier()
            utt.pos_raw = self.reader.get_pos_tier()

            # clean the morphology tiers
            seg_tier = self.cleaner.clean_seg_tier(utt.morpheme)
            gloss_tier = self.cleaner.clean_gloss_tier(utt.gloss_raw)
            pos_tier = self.cleaner.clean_pos_tier(utt.pos_raw)

            # cross cleaning
            actual_utt, target_utt, seg_tier, gloss_tier, pos_tier = \
                self.cleaner.utterance_cross_clean(
                    utt.utterance_raw, actual_utt, target_utt,
                    seg_tier, gloss_tier, pos_tier)

            # get dictionary of words
            self.add_words(actual_utt, target_utt)

            # rebuild utterance from cleaned words
            utt.utterance = ' '.join(w.word for w in utt.words)

            # get morpheme words from the respective morphology tiers
            wsegs = self.reader.get_seg_words(seg_tier)
            wglosses = self.reader.get_gloss_words(gloss_tier)
            wposes = self.reader.get_pos_words(pos_tier)

            # determine number of words to be considered based on
            # main morphology tier and existence of this morphology tier
            if self.reader.get_main_morpheme() == 'segment':
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
                wsegs = wlen*['']
            if wlen != len(wglosses):
                wglosses = wlen*['']
            if wlen != len(wposes):
                wposes = wlen*['']

            # collect morpheme data of an utterance
            # go through all morpheme words
            for wseg, wgloss, wpos in zip(wsegs, wglosses, wposes):

                cleaned_wseg = self.cleaner.clean_seg_word(wseg)
                cleaned_wgloss = self.cleaner.clean_gloss_word(wgloss)
                cleaned_wpos = self.cleaner.clean_pos_word(wpos)

                # collect morpheme data of a word
                wmorphemes = []

                # get morphemes from the morpheme words
                segments = self.reader.get_segments(cleaned_wseg)
                glosses = self.reader.get_glosses(cleaned_wgloss)
                poses = self.reader.get_poses(cleaned_wpos)

                # determine number of morphemes to be considered
                if self.reader.get_main_morpheme() == 'segment':
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
                    segments = mlen*['']
                if mlen != len(glosses):
                    glosses = mlen*['']
                if mlen != len(poses):
                    poses = mlen*['']

                # go through morphemes
                for seg, gloss, pos in zip(segments, glosses, poses):
                    m = Morpheme()
                    m.utterance = utt

                    m.morpheme_language = self.reader.get_morpheme_language(
                                            seg, gloss, pos)

                    # clean the morphemes
                    m.morpheme = self.cleaner.clean_segment(seg)
                    m.gloss_raw = self.cleaner.clean_gloss(gloss)
                    m.pos_raw = self.cleaner.clean_pos(pos)

                    wmorphemes.append(m)

                utt.morphemes.append(wmorphemes)

    def get_source_id(self):
        """Get the source id of the current utterance."""
        fname = self.session_path.split('/')[-1]
        fname_no_ext = fname.split('.')[0]
        uid = self.reader.get_uid()
        if fname:
            return '{}_{}'.format(fname_no_ext, uid)
        return uid
