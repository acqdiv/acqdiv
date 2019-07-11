import os

from acqdiv.parsers.chat.readers.CHATReader import CHATReader
from acqdiv.parsers.chat.cleaners.CHATCleaner import CHATCleaner
from acqdiv.parsers.SessionParser import SessionParser
from acqdiv.model.Session import Session
from acqdiv.model.Speaker import Speaker


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

    def get_words_dict(self, actual_utt, target_utt):
        actual_words = self.reader.get_utterance_words(actual_utt)
        target_words = self.reader.get_utterance_words(target_utt)

        words = []
        for word_actual, word_target in zip(actual_words, target_words):

            if self.reader.get_standard_form() == 'actual':
                word = word_actual
            else:
                word = word_target

            word_language = self.reader.get_word_language(word)

            word = self.cleaner.clean_word(word)
            word_actual = self.cleaner.clean_word(word_actual)
            word_target = self.cleaner.clean_word(word_target)

            if not self.consistent_actual_target:
                if word_actual == word_target:
                    word_actual = None
                    word_target = None

            word_dict = {
                'word_language': word_language if word_language else None,
                'word': word,
                'word_actual': word_actual,
                'word_target': word_target,
                'warning': None
            }
            words.append(word_dict)

        return words

    def next_utterance(self):
        """Yields the next utterance of a session."""
        while self.reader.load_next_record():

            source_id = self.get_source_id()
            addressee = self.cleaner.clean_record_speaker_label(
                self.session_filename, self.reader.get_addressee())
            translation = self.reader.get_translation()
            comment = self.reader.get_comments()
            speaker_label = self.cleaner.clean_record_speaker_label(
                self.session_filename, self.reader.get_record_speaker_label())
            utterance_raw = self.reader.get_utterance()
            start_raw = self.reader.get_start_time()
            end_raw = self.reader.get_end_time()
            sentence_type = self.reader.get_sentence_type()

            # actual & target distinction
            actual_utt = self.cleaner.clean_utterance(
                self.reader.get_actual_utterance())
            target_utt = self.cleaner.clean_utterance(
                self.reader.get_target_utterance())

            # clean translation
            translation = self.cleaner.clean_translation(translation)

            # get morphology tiers
            seg_tier_raw = self.reader.get_seg_tier()
            gloss_tier_raw = self.reader.get_gloss_tier()
            pos_tier_raw = self.reader.get_pos_tier()

            # clean the morphology tiers
            seg_tier = self.cleaner.clean_seg_tier(seg_tier_raw)
            gloss_tier = self.cleaner.clean_gloss_tier(gloss_tier_raw)
            pos_tier = self.cleaner.clean_pos_tier(pos_tier_raw)

            # cross cleaning
            actual_utt, target_utt, seg_tier, gloss_tier, pos_tier = \
                self.cleaner.utterance_cross_clean(
                    utterance_raw, actual_utt, target_utt,
                    seg_tier, gloss_tier, pos_tier)

            # get dictionary of words
            words = self.get_words_dict(actual_utt, target_utt)

            # rebuild utterance from cleaned words
            utterance = ' '.join(w['word'] for w in words)

            utterance_dict = {
                'source_id': source_id,
                'speaker_label': speaker_label,
                'addressee': addressee if addressee else None,
                'utterance_raw': utterance_raw,
                'utterance': utterance if utterance else None,
                'translation': translation if translation else None,
                'morpheme': seg_tier_raw if seg_tier_raw else None,
                'gloss_raw': gloss_tier_raw if gloss_tier_raw else None,
                'pos_raw': pos_tier_raw if pos_tier_raw else None,
                'sentence_type': sentence_type if sentence_type else None,
                'start_raw': start_raw if start_raw else None,
                'end_raw': end_raw if end_raw else None,
                'comment': comment if comment else None,
                'warning': None
            }

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
            morphemes = []
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

                    morpheme_language = self.reader.get_morpheme_language(
                                            seg, gloss, pos)

                    # clean the morphemes
                    seg = self.cleaner.clean_segment(seg)
                    gloss = self.cleaner.clean_gloss(gloss)
                    pos = self.cleaner.clean_pos(pos)

                    morpheme_dict = {
                        'morpheme_language':
                            morpheme_language if morpheme_language else None,
                        'morpheme': seg if seg else None,
                        'gloss_raw': gloss if gloss else None,
                        'pos_raw': pos if pos else None
                    }
                    wmorphemes.append(morpheme_dict)

                morphemes.append(wmorphemes)

            yield utterance_dict, words, morphemes

    def get_source_id(self):
        """Get the source id of the current utterance."""
        fname = self.session_path.split('/')[-1]
        fname_no_ext = fname.split('.')[0]
        uid = self.reader.get_uid()
        if fname:
            return '{}_{}'.format(fname_no_ext, uid)
        return uid
