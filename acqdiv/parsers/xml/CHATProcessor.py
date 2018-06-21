from acqdiv.parsers.xml import CHATParser
from acqdiv.parsers.xml import CHATCleaner


class CHATProcessor:
    pass


class InuktitutProcessor:

    def __init__(self):
        self.p = CHATParser.InuktitutParser()
        self.c = CHATCleaner.InuktitutCleaner()

    def next_utterance(self, session_path):

        for rec in self.p.iter_records(session_path):
            main_line = self.p.get_main_line(rec)
            utterance = self.p.get_utterance(main_line)
            rec_time = self.p.get_time(main_line)
            actual_utterance = self.p.get_actual_form(utterance)
            target_utterance = self.p.get_target_form(utterance)
            actual_utterance = self.c.clean(actual_utterance)
            target_utterance = self.c.clean(target_utterance)

            utt_dict = {
                'source_id': None,
                'speaker_label': self.p.get_speaker_label(main_line),
                'addressee': self.p.get_dependent_tier(rec, 'add'),
                'utterance_raw': utterance,
                'utterance': actual_utterance,
                'translation': self.p.get_dependent_tier(rec, 'eng'),
                'morpheme': None,
                'gloss_raw': None,
                'pos_raw': None,
                'sentence_type': self.p.get_sentence_type(utterance),
                'start_raw': self.p.get_start(rec_time),
                'end_raw': self.p.get_end(rec_time),
                'comment': None,
                'warning': None
            }

            words = []
            morphemes = []
            xmor = self.p.get_dependent_tier(rec, 'xmor')
            xmor = self.c.clean_xmor(xmor)

            for actual, target, mword in zip(
                    self.p.iter_words(actual_utterance),
                    self.p.iter_words(target_utterance),
                    self.p.iter_words(xmor)):

                word_dict = {
                    'corpus': 'Inuktitut',
                    'language': 'Inuktitut',
                    'word_language': 'Inuktitut',
                    'word': actual,
                    'word_actual': actual,
                    'word_target': target,
                    'warning': None
                }
                words.append(word_dict)

                wmorphemes = []
                mword = self.c.remove_english_word_marker(mword)
                for pos, seg, gloss in self.p.iter_morphemes(mword):
                    pos = self.c.replace_pos_separator(pos)
                    gloss = self.c.replace_stem_grammatical_gloss_connector(
                                gloss)
                    morpheme_dict = {
                        'morpheme_language': None,
                        'morpheme': seg,
                        'gloss_raw': gloss,
                        'pos_raw': pos
                    }
                    wmorphemes.append(morpheme_dict)
                morphemes.append(wmorphemes)
