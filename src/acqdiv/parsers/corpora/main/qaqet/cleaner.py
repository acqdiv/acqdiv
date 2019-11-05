import re

from acqdiv.parsers.toolbox.cleaners.cleaner import ToolboxCleaner
from acqdiv.parsers.corpora.main.qaqet.gloss_mapper import QaqetGlossMapper
from acqdiv.parsers.corpora.main.qaqet.pos_mapper import QaqetPOSMapper


class QaqetCleaner(ToolboxCleaner):

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
            cls.remove_events_utterance,
            cls.remove_punctuation,
            # cls.null_untranscribed_utterance,
            cls.unify_unknowns_utterance
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
        # morph_tier = cls.null_untranscribed_morphology_tier(morph_tier)
        return morph_tier

    @classmethod
    def remove_events_seg_tier(cls, seg_tier):
        events = {
            'action',
            'click',
            'cry',
            'laugh',
            'raises-eyebrows',
            'shakes-head',
            'sings',
            'sneeze',
            'sound',
            'spits'
        }

        for event in events:
            seg_tier = seg_tier.replace(event, '')

        return cls.remove_redundant_whitespaces(seg_tier)

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        return cls.remove_events_seg_tier(seg_tier)

    @classmethod
    def remove_events_gloss_tier(cls, gloss_tier):
        events = {
            'ACTION',
            'CLICK',
            'CRY',
            'LAUGH',
            'SINGS',
            'SNEEZE',
            'SOUND',
            'SPITS'
        }
        for event in events:
            gloss_tier = gloss_tier.replace(event, '')

        return cls.remove_redundant_whitespaces(gloss_tier)

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        return cls.remove_events_gloss_tier(gloss_tier)

    @classmethod
    def remove_events_pos_tier(cls, pos_tier):
        events = {
            'ACTION',
            'GESTURE',
            'SOUND'
        }

        for event in events:
            pos_tier = pos_tier.replace(event, '')

        return cls.remove_redundant_whitespaces(pos_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        return cls.remove_events_pos_tier(pos_tier)

    # ---------- morpheme ----------

    @classmethod
    def clean_lang_word(cls, lang_word):
        if lang_word == '??':
            return ''

        return lang_word

    # ---------- morpheme ----------

    @classmethod
    def clean_gloss(cls, gloss):
        return QaqetGlossMapper.map(gloss)

    @classmethod
    def clean_pos(cls, pos):
        return QaqetPOSMapper.map(pos)

    @classmethod
    def clean_pos_ud(cls, pos_ud):
        return QaqetPOSMapper.map(pos_ud, ud=True)

    @classmethod
    def lang2lang(cls, lang):
        """Map the original language label to ACQDIV label."""
        mapping = {
            'Q': 'Qaqet',
            'TP': 'Tok Pisin',
            'E': 'English',
            'GE': 'German',
            'K': 'Kuanua'
        }

        return mapping.get(lang, 'Qaqet')

    @classmethod
    def clean_lang(cls, lang):
        lang = super().clean_lang(lang)
        return cls.lang2lang(lang)
