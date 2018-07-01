
class CHATParser:
    """Gathers all data for the DB for a given CHAT session file.

    Uses the CHATParser for parsing and inferring data from the CHAT file and
    CHATCleaner for cleaning these data.
    """

    def __init__(self, session_path, parser, cleaner):
        """Initialize the path of the CHAT session file.

        Args:
            session_path (str): The path to the CHAT session path.
            parser (CHATParser): The CHAT parser.
            cleaner (CHATCleaner): The CHAT cleaner.
        """
        self.session_path = session_path
        self.p = parser
        self.c = cleaner

    def next_utterance(self):
        """Yields the next utterance of a session.

        Requires the implementation of the following methods:

            CHATParser:
                iter_records
                get_uid
                get_main_line
                get_speaker_label
                get_addressee
                get_utterance
                get_actual_form
                get_target_form
                get_translation
                get_sentence_type
                get_time
                get_start_raw
                get_end_raw
                get_words
                get_seg_tier
                get_gloss_tier
                get_pos_tier
                get_seg_words
                get_gloss_words
                get_pos_words
                get_segments
                get_glosses
                get_poses

            CHATCleaner
                clean_utterance
                clean_seg_tier
                clean_gloss_tier
                clean_pos_tier
                clean_segment
                clean_gloss
                clean_pos
        """
        # go through each record in the session
        for rec in self.p.iter_records(self.session_path):

            # get source ID
            source_id = self.p.get_uid()

            # get fields from record
            addressee = self.p.get_addressee(rec)
            translation = self.p.get_translation(rec)
            comment = self.p.get_comments(rec)

            # get fields from main line
            main_line = self.p.get_main_line(rec)
            speaker_label = self.p.get_speaker_label(main_line)
            utterance_raw = self.p.get_utterance(main_line)

            # get fields from time
            rec_time = self.p.get_time(main_line)
            start_raw = self.p.get_start(rec_time)
            end_raw = self.p.get_end(rec_time)

            # get actual and target utterances and clean them
            actual_utterance = self.c.clean_utterance(
                self.p.get_actual_form(utterance_raw))
            target_utterance = self.c.clean_utterance(
                self.p.get_target_form(utterance_raw))
            # set actual or target utterance as standard
            utterance = actual_utterance

            # get sentence type from utterance
            sentence_type = self.p.get_sentence_type(utterance)

            # get morphology tiers and clean them
            seg_tier = self.c.clean_seg_tier(self.p.get_seg_tier(rec))
            gloss_tier = self.c.clean_gloss_tier(self.p.get_gloss_tier(rec))
            pos_tier = self.c.clean_pos_tier(self.p.get_pos_tier(rec))

            utterance_dict = {
                'source_id': source_id,
                'speaker_label': speaker_label,
                'addressee': addressee,
                'utterance_raw': utterance_raw,
                'utterance': utterance,
                'translation': translation,
                'morpheme': seg_tier,
                'gloss_raw': gloss_tier,
                'pos_raw': pos_tier,
                'sentence_type': sentence_type,
                'start_raw': start_raw,
                'end_raw': end_raw,
                'comment': comment,
                'warning': None
            }

            # get actual and target words from the respective utterances
            actual_words = self.p.get_words(actual_utterance)
            target_words = self.p.get_words(target_utterance)

            # collect all words of the utterance
            words = []
            for word_actual, word_target in zip(actual_words, target_words):

                word_dict = {
                    'word_language': 'Inuktitut',
                    'word': word_actual,
                    'word_actual': word_actual,
                    'word_target': word_target,
                    'warning': None
                }
                words.append(word_dict)

            # get morpheme words from the respective morphology tiers
            wsegs = self.p.get_seg_words(seg_tier)
            wglosses = self.p.get_gloss_words(gloss_tier)
            wposes = self.p.get_pos_words(pos_tier)

            # collect morpheme data of an utterance
            morphemes = []
            # go through all morpheme words
            for wseg, wgloss, wpos in zip(wsegs, wglosses, wposes):

                # collect morpheme data of a word
                wmorphemes = []

                # get morphemes from the morpheme words
                segments = self.p.get_segments(wseg)
                glosses = self.p.get_glosses(wgloss)
                poses = self.p.get_poses(wpos)

                # go through morphemes
                for seg, gloss, pos in zip(segments, glosses, poses):

                    # clean the morphemes
                    seg = self.c.clean_segment(seg)
                    gloss = self.c.clean_gloss(gloss)
                    pos = self.c.clean_pos(pos)

                    morpheme_dict = {
                        'morpheme_language': None,
                        'morpheme': seg,
                        'gloss_raw': gloss,
                        'pos_raw': pos
                    }
                    wmorphemes.append(morpheme_dict)

                morphemes.append(wmorphemes)

            yield utterance_dict, words, morphemes

