from acqdiv.parsers.xml import CHATReader
from acqdiv.parsers.xml import CHATCleaner


class CHATParser:
    """Gathers all data for the DB for a given CHAT session file.

    Uses the CHATReader for reading and inferring data from the CHAT file and
    CHATCleaner for cleaning these data.
    """

    def __init__(self, session_path):
        self.session_path = session_path
        self.reader = self.get_reader()
        self.cleaner = self.get_cleaner()

    @staticmethod
    def get_reader():
        return CHATReader.CHATReader()

    @staticmethod
    def get_cleaner():
        return CHATCleaner.CHATCleaner()

    def next_utterance(self):
        """Yields the next utterance of a session."""
        # go through each record in the session
        for rec in self.reader.iter_records(self.session_path):

            # get source ID
            source_id = self.reader.get_uid()

            # get fields from record
            addressee = self.reader.get_addressee(rec)
            translation = self.reader.get_translation(rec)
            comment = self.reader.get_comments(rec)

            # get fields from main line
            main_line = self.reader.get_main_line(rec)
            speaker_label = self.reader.get_speaker_label(main_line)
            utterance_raw = self.reader.get_utterance_raw(main_line)

            # get fields from time
            rec_time = self.reader.get_time(main_line)
            start_raw = self.reader.get_start(rec_time)
            end_raw = self.reader.get_end(rec_time)

            # get fields from raw utterance
            sentence_type = self.reader.get_sentence_type(utterance_raw)
            actual_utterance = self.cleaner.clean_utterance(
                self.reader.get_actual_utterance(utterance_raw))
            target_utterance = self.cleaner.clean_utterance(
                self.reader.get_target_utterance(utterance_raw))
            utterance = self.cleaner.clean_utterance(
                self.reader.get_utterance(utterance_raw))

            # get morphology tiers and clean them
            seg_tier = self.cleaner.clean_seg_tier(
                            self.reader.get_seg_tier(rec))
            gloss_tier = self.cleaner.clean_gloss_tier(
                            self.reader.get_gloss_tier(rec))
            pos_tier = self.cleaner.clean_pos_tier(
                            self.reader.get_pos_tier(rec))

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
            actual_words = self.reader.get_words(actual_utterance)
            target_words = self.reader.get_words(target_utterance)

            # collect all words of the utterance
            words = []
            for word_actual, word_target in zip(actual_words, target_words):

                word_dict = {
                    'word_language': None,
                    'word': word_actual,
                    'word_actual': word_actual,
                    'word_target': word_target,
                    'warning': None
                }
                words.append(word_dict)

            # get morpheme words from the respective morphology tiers
            wsegs = self.reader.get_seg_words(seg_tier)
            wglosses = self.reader.get_gloss_words(gloss_tier)
            wposes = self.reader.get_pos_words(pos_tier)

            # collect morpheme data of an utterance
            morphemes = []
            # go through all morpheme words
            for wseg, wgloss, wpos in zip(wsegs, wglosses, wposes):

                # collect morpheme data of a word
                wmorphemes = []

                # get morphemes from the morpheme words
                segments = self.reader.get_segments(wseg)
                glosses = self.reader.get_glosses(wgloss)
                poses = self.reader.get_poses(wpos)

                # go through morphemes
                for seg, gloss, pos in zip(segments, glosses, poses):

                    # clean the morphemes
                    seg = self.cleaner.clean_segment(seg)
                    gloss = self.cleaner.clean_gloss(gloss)
                    pos = self.cleaner.clean_pos(pos)

                    morpheme_dict = {
                        'morpheme_language': None,
                        'morpheme': seg,
                        'gloss_raw': gloss,
                        'pos_raw': pos
                    }
                    wmorphemes.append(morpheme_dict)

                morphemes.append(wmorphemes)

            yield utterance_dict, words, morphemes


class CreeParser(CHATParser):
    @staticmethod
    def get_reader():
        return CHATReader.CreeReader()

    @staticmethod
    def get_cleaner():
        return CHATCleaner.CreeCleaner()


class InuktitutParser(CHATParser):
    @staticmethod
    def get_reader():
        return CHATReader.InuktitutReader()

    @staticmethod
    def get_cleaner():
        return CHATCleaner.InuktitutCleaner()


def main():
    import glob
    import acqdiv
    import os
    import time

    # Cree parsing
    start_time = time.time()

    acqdiv_path = os.path.dirname(acqdiv.__file__)
    corpus_path = os.path.join(acqdiv_path, 'corpora/Cree/cha/*.cha')

    for path in glob.iglob(corpus_path):
        parser = CreeParser(path)

        print(path)

        for utterance, words, morphemes in parser.next_utterance():
            pass

    print('--- %s seconds ---' % (time.time() - start_time))


if __name__ == '__main__':
    main()
