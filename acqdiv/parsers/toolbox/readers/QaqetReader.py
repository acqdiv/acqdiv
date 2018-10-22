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

    # ---------- clean utterance ----------

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
    def remove_morpheme_sep(cls, morpheme):
        """Remove morpheme and clitic separators.

        Morpheme (-), clitic (=)
        """
        return morpheme.strip('-').strip('=')

    @classmethod
    def null_untranscribed_morpheme(cls, morpheme):
        if morpheme in {'??', '***'}:
            return ''

        return morpheme

    @classmethod
    def lang2lang(cls, lang):
        """Map the original language label to ACQDIV label."""
        mapping = {
            'Q': 'Qaqet',
            'TP': 'Tok Pisin',
            'E': 'English',
            'GE': 'German'}

        return mapping[lang]

    @classmethod
    def clean_lang(cls, lang):
        lang = cls.remove_morpheme_sep(lang)
        lang = cls.null_untranscribed_morpheme(lang)

        if lang:
            return cls.lang2lang(lang)

        return lang
