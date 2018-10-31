import re

from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader


class QaqetReader(ToolboxReader):

    @classmethod
    def get_utterance_raw(cls, rec_dict):
        return cls.get_actual_utterance(rec_dict)

    @classmethod
    def get_actual_utterance(cls, rec_dict):
        return rec_dict.get('tx', '')

    @classmethod
    def get_target_utterance(cls, rec_dict):
        return rec_dict.get('trs-i', '')

    @classmethod
    def get_translation(cls, rec_dict):
        return rec_dict.get('ft', '')

    @classmethod
    def get_comment(cls, rec_dict):
        return rec_dict.get('nt', '')

    @classmethod
    def get_sentence_type(cls, rec_dict):
        """Get sentence type.

        Usually, there are no terminators in the transcriptions. In this case,
        the default value used. Only questions are explicitly marked,
        exclamations not.
        """
        utterance = cls.get_utterance_raw(rec_dict)
        if utterance.endswith('?'):
            return 'question'
        else:
            return 'default'

    @classmethod
    def get_words_data(cls, rec_dict):
        result = []
        actual_utterance = cls.clean_utterance(cls.get_utterance_raw(rec_dict))
        target_utterance = cls.clean_utterance(
            cls.get_target_utterance(rec_dict))

        actual_words = cls.get_words(actual_utterance)
        target_words = cls.get_words(target_utterance)

        if len(actual_words) != len(target_words):
            target_words = len(actual_words)*['']

        for actual, target in zip(actual_words, target_words):
            actual_clean = cls.clean_word(actual)
            target_clean = cls.clean_word(target)

            d = {
                'word': actual_clean,
                'word_actual': actual_clean,
                'word_target': target_clean if target_clean else None
            }
            result.append(d)
        return result

    # ---------- cleaners ----------

    # ---------- utterance ----------

    @classmethod
    def remove_events_utterance(cls, utterance):
        """Remove events in utterance.

        Events are enclosed in square brackets, e.g.
        [sound], [laugh], [cry], [sings], ...
        """
        # do not match unknowns such as [x]
        event_regex = re.compile(r'\[(?!x+).*\]')
        utterance = event_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(utterance)

    @classmethod
    def remove_punctuation(cls, utterance):
        punctuation_regex = re.compile(r'[,?.]')
        utterance = punctuation_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(utterance)

    @classmethod
    def null_untranscribed_utterance(cls, utterance):
        """Null untranscribed utterance.

        Marked as [x+].
        """
        untranscribed_regex = re.compile(r'\[x+\]')
        if untranscribed_regex.fullmatch(utterance):
            return ''

        return utterance

    @classmethod
    def unify_unknowns_utterance(cls, utterance):
        """Unify unknowns.

        Marked as [x+].
        """
        unk_regex = re.compile(r'\[x+\]')
        return unk_regex.sub('???', utterance)

    @classmethod
    def clean_utterance(cls, utterance):
        for cleaning_method in [
                cls.remove_events_utterance, cls.remove_punctuation,
                cls.null_untranscribed_utterance, cls.unify_unknowns_utterance
                ]:
            utterance = cleaning_method(utterance)

        return utterance

    # ---------- morphology tier ----------

    @classmethod
    def null_untranscribed_morphology_tier(cls, morph_tier):
        untranscribed_re = re.compile(r'\?\?|\*{3}|x{1,4}')

        if untranscribed_re.fullmatch(morph_tier):
            return ''

        return morph_tier

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        return cls.null_untranscribed_morphology_tier(morph_tier)

    @classmethod
    def remove_events_seg_tier(cls, seg_tier):
        events = {'click', 'cry', 'laugh', 'raises-eyebrows', 'shakes-head',
                  'sings', 'sneeze', 'sound', 'spits'}

        for event in events:
            seg_tier = seg_tier.replace(event, '')

        return cls.remove_redundant_whitespaces(seg_tier)

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        return cls.remove_events_seg_tier(seg_tier)

    @classmethod
    def remove_events_gloss_tier(cls, gloss_tier):
        events = {'CLICK', 'CRY', 'LAUGH', 'SINGS', 'SNEEZE', 'SOUND', 'SPITS',
                  'yes', 'what?'}
        for event in events:
            gloss_tier = gloss_tier.replace(event, '')

        return cls.remove_redundant_whitespaces(gloss_tier)

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        return cls.remove_events_gloss_tier(gloss_tier)

    @classmethod
    def remove_events_pos_tier(cls, pos_tier):
        events = {'GESTURE', 'SOUND'}

        for event in events:
            pos_tier = pos_tier.replace(event, '')

        return cls.remove_redundant_whitespaces(pos_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        return cls.remove_events_pos_tier(pos_tier)

    # ---------- morpheme ----------

    @classmethod
    def unify_unknowns_morpheme(cls, morpheme):
        unknown_re = re.compile(r'x{1,4}|\?{2}|\*{3}')
        return unknown_re.sub('???', morpheme)

    @classmethod
    def clean_morpheme(cls, morpheme):
        return cls.unify_unknowns_morpheme(morpheme)

    @classmethod
    def remove_morpheme_sep(cls, morpheme):
        """Remove morpheme and clitic separators.

        Morpheme (-), clitic (=)
        """
        return morpheme.strip('-').strip('=')

    @classmethod
    def lang2lang(cls, lang):
        """Map the original language label to ACQDIV label."""
        mapping = {
            'Q': 'Qaqet',
            'TP': 'Tok Pisin',
            'E': 'English',
            'GE': 'German',
            '???': ''
        }

        return mapping[lang]

    @classmethod
    def clean_lang(cls, lang):
        lang = cls.remove_morpheme_sep(lang)

        if lang:
            return cls.lang2lang(lang)

        return lang
