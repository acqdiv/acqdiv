import os

from acqdiv.parsers.chat.readers.reader import CHATReader
from acqdiv.parsers.chat.cleaners.cleaner import CHATCleaner
from acqdiv.parsers.session_parser import SessionParser

from acqdiv.util.age import get_age_in_days
from acqdiv.util.role import RoleMapper
from acqdiv.util.alignment import align_words_morphemes, fix_misalignments
from acqdiv.util.childdirectedness import infer_childdirected

from acqdiv.model.session import Session
from acqdiv.model.speaker import Speaker
from acqdiv.model.utterance import Utterance
from acqdiv.model.word import Word
from acqdiv.model.morpheme import Morpheme


class CHATParser(SessionParser):
    """Gathers all data for the DB for a given CHAT session file.

    Uses the CHATReader for reading and inferring data from the CHAT file and
    CHATCleaner for cleaning these data.
    """

    role_mapper = RoleMapper()

    def __init__(self, session_path):
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
            acqdiv.parsers.chat.readers.reader.CHATReader:
            The reader instance.
        """
        return CHATReader(session_file)

    @staticmethod
    def get_cleaner():
        """Return a CHATCleaner instance.

        Returns:
            acqdiv.parsers.chat.cleaners.cleaner.CHATCleaner:
            The cleaner instance.
        """
        return CHATCleaner()

    def parse(self):
        """Get the session instance.

        Returns:
            acqdiv.model.session.Session: The Session instance.
        """
        session = Session()
        self.add_session_metadata(session)
        self.add_speakers(session)
        self.add_records(session)

        return session

    def add_session_metadata(self, session):
        """Add the metadata to the session."""
        date = self.cleaner.clean_date(self.reader.get_session_date())
        media_filename = self.reader.get_session_media_filename()

        # any corrections of the metadata
        date, media_filename = self.cleaner.clean_session_metadata(
            self.session_filename, date, media_filename)

        session.source_id = os.path.splitext(self.session_filename)[0]
        session.date = date if date else None
        session.media_filename = media_filename if media_filename else None

    def add_speakers(self, session):
        """Add the speakers to the session."""
        while self.reader.load_next_speaker():
            speaker = Speaker()

            speaker_label = self.reader.get_speaker_label()
            name = self.reader.get_speaker_name()
            role_raw = self.reader.get_speaker_role()
            age_raw = self.reader.get_speaker_age()
            gender_raw = self.reader.get_speaker_gender()
            language = self.reader.get_speaker_language()
            birth_date = self.cleaner.clean_date(
                                self.reader.get_speaker_birthdate())
            target_child = self.reader.get_target_child()

            # any corrections of the metadata
            speaker_label, name, role_raw, age_raw, gender_raw, language, birth_date = \
                self.cleaner.clean_speaker_metadata(
                    self.session_filename, speaker_label, name, role_raw, age_raw,
                    gender_raw, language, birth_date, target_child)

            speaker.code = speaker_label
            speaker.name = self.cleaner.clean_name(name)
            speaker.languages_spoken = language
            speaker.birth_date = birth_date

            speaker.age_raw = age_raw
            speaker.age = self.cleaner.clean_age(speaker.age_raw)
            speaker.age_in_days = get_age_in_days(speaker.age)

            speaker.role_raw = role_raw
            speaker.role = self.role_mapper.role_raw2role(speaker.role_raw)
            speaker.macro_role = self.role_mapper.infer_macro_role(
                speaker.role_raw, speaker.age_in_days, speaker.code)

            speaker.gender_raw = gender_raw
            speaker.gender = self.cleaner.clean_gender(speaker.gender_raw)
            if not speaker.gender:
                speaker.gender = self.role_mapper.role_raw2gender(
                    speaker.role_raw)

            session.speakers.append(speaker)

    def add_records(self, session):
        """Add the records."""
        while self.reader.load_next_record():
            utt = self.add_utterance(session)
            self.add_words(utt)
            self.add_morphemes(utt)
            align_words_morphemes(utt)

    @staticmethod
    def _get_speaker(label, speakers):
        for speaker in speakers:
            if speaker.code == label:
                return speaker

        return None

    def add_utterance(self, session):
        """Add the utterance to the session."""
        utt = Utterance()
        session.utterances.append(utt)
        utt.source_id = self.get_source_id()
        speaker_label = self.cleaner.clean_record_speaker_label(
            self.session_filename, self.reader.get_record_speaker_label())
        utt.speaker = self._get_speaker(speaker_label, session.speakers)
        addressee_label = self.cleaner.clean_record_speaker_label(
            self.session_filename, self.reader.get_addressee())
        utt.addressee = self._get_speaker(addressee_label, session.speakers)
        utt.childdirected = infer_childdirected(utt)
        utt.translation = self.cleaner.clean_translation(
            self.reader.get_translation())
        utt.comment = self.reader.get_comments()
        utt.utterance_raw = self.reader.get_utterance()
        utt.start_raw = self.reader.get_start_time()
        utt.start = self.cleaner.clean_timestamp(utt.start_raw)
        utt.end_raw = self.reader.get_end_time()
        utt.end = self.cleaner.clean_timestamp(utt.end_raw)
        utt.sentence_type = self.reader.get_sentence_type()
        utt.warning = ''

        # set raw morphology tiers
        utt.morpheme_raw = self.reader.get_seg_tier()
        utt.gloss_raw = self.reader.get_gloss_tier()
        utt.pos_raw = self.reader.get_pos_tier()

        # clean the morphology tiers
        seg_tier = self.cleaner.clean_seg_tier(utt.morpheme_raw)
        gloss_tier = self.cleaner.clean_gloss_tier(utt.gloss_raw)
        pos_tier = self.cleaner.clean_pos_tier(utt.pos_raw)

        # actual & target distinction
        actual_utt = self.cleaner.clean_utterance(
            self.reader.get_actual_utterance())
        target_utt = self.cleaner.clean_utterance(
            self.reader.get_target_utterance())

        # cross cleaning
        actual_utt, target_utt, seg_tier, gloss_tier, pos_tier = \
            self.cleaner.utterance_cross_clean(
                utt.utterance_raw, actual_utt, target_utt,
                seg_tier, gloss_tier, pos_tier)

        utt.actual_utterance = actual_utt
        utt.target_utterance = target_utt
        utt.morpheme = seg_tier
        utt.gloss = gloss_tier
        utt.pos = pos_tier

        return utt

    def add_words(self, utt):
        """Add the words to the utterance."""
        actual_words = self.reader.get_utterance_words(utt.actual_utterance)
        target_words = self.reader.get_utterance_words(utt.target_utterance)

        for word_actual, word_target in zip(actual_words, target_words):

            w = Word()
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

        # rebuild utterance from cleaned words
        utt.utterance = ' '.join(w.word for w in utt.words)

    def get_source_id(self):
        """Get the source id of the current utterance."""
        fname = self.session_path.split('/')[-1]
        fname_no_ext = fname.split('.')[0]
        uid = self.reader.get_uid()
        if fname:
            return '{}_{}'.format(fname_no_ext, uid)
        return uid

    def add_morphemes(self, utt):
        """Add the morphemes to the utterance."""
        wsegs = self.reader.get_seg_words(utt.morpheme)
        wglosses = self.reader.get_gloss_words(utt.gloss)
        wposes = self.reader.get_pos_words(utt.pos)

        if self.reader.get_main_morpheme() == 'segment':
            wsegs, wglosses, wposes = \
                fix_misalignments([wsegs, wglosses, wposes])
        else:
            wglosses, wsegs, wposes = \
                fix_misalignments([wglosses, wsegs, wposes])

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
                segments, glosses, poses = \
                    fix_misalignments([segments, glosses, poses])
            else:
                glosses, segments, poses = \
                    fix_misalignments([glosses, segments, poses])

            # go through morphemes
            for seg, gloss, pos in zip(segments, glosses, poses):
                m = Morpheme()

                m.morpheme_language = self.reader.get_morpheme_language(
                    seg, gloss, pos)

                m.morpheme = self.cleaner.clean_segment(seg)
                m.gloss_raw = self.cleaner.clean_gloss_raw(gloss)
                m.gloss = self.cleaner.clean_gloss(gloss)
                m.pos_raw = self.cleaner.clean_pos_raw(pos)
                m.pos = self.cleaner.clean_pos(pos)
                m.pos_ud = self.cleaner.clean_pos_ud(pos)
                m.type = self.reader.get_morpheme_type()

                wmorphemes.append(m)

            utt.morphemes.append(wmorphemes)
