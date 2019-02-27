import re

from acqdiv.parsers.toolbox.readers.ToolboxReader import ToolboxReader


class IndonesianReader(ToolboxReader):

    language = 'Indonesian'

    @classmethod
    def get_source_id(cls, rec_dict):
        return rec_dict.get('id', '')

    @classmethod
    def get_speaker_label(cls, rec_dict):
        return rec_dict.get('sp', '')

    @classmethod
    def get_start_raw(cls, rec_dict):
        return rec_dict.get('begin', '')

    @classmethod
    def get_utterance_raw(cls, rec_dict):
        return rec_dict.get('tx', '')

    @classmethod
    def get_translation(cls, rec_dict):
        return rec_dict.get('ft', '')

    @classmethod
    def get_comment(cls, rec_dict):
        return rec_dict.get('nt', '')

    @classmethod
    def get_seg_tier(cls, rec_dict):
        return rec_dict.get('mb', '')

    @classmethod
    def get_gloss_tier(cls, rec_dict):
        return rec_dict.get('ge', '')

    @classmethod
    def is_record(cls, rec_dict):
        if not super().is_record(rec_dict):
            return False

        if cls.get_speaker_label(rec_dict) == '@PAR':
            return False

        return True

    @classmethod
    def get_words_data(cls, rec_dict):
        result = []
        # TODO: this is not modular yet
        utterance = cls.get_utterance_raw(rec_dict)
        utterance_clean = cls.clean_utterance(utterance)

        for word in cls.get_words(utterance_clean):
            d = {}
            # Distinguish between word and word_target;
            # otherwise the target word is identical to the actual word
            if re.search('\(', word):
                d['word_target'] = re.sub('[()]', '', word)
                d['word'] = re.sub('\([^)]+\)', '', word)
                d['word_actual'] = d['word']
                result.append(d)
            else:
                d['word_target'] = re.sub('xxx?|www', '???', word)
                d['word'] = re.sub('xxx?', '???', word)
                d['word_actual'] = d['word']
                result.append(d)

        return result

    @classmethod
    def get_sentence_type(cls, rec_dict):
        utterance_raw = cls.get_utterance_raw(rec_dict)
        if re.search('\.', utterance_raw):
            return 'default'
        elif re.search('\?\s*$', utterance_raw):
            return 'question'
        elif re.search('!', utterance_raw):
            return 'imperative'
        else:
            return ''

    @classmethod
    def add_utterance_warnings(cls, utterance):
        # Insecure transcription [?], add warning, delete marker
        # cf. https://github.com/uzling/acqdiv/blob/master/
        # extraction/parsing/corpus_parser_functions.py#L1605-1610
        if re.search('\[\?\]', utterance):
            transcription_warning = 'transcription insecure'
            cls.warnings.append(transcription_warning)

    @classmethod
    def remove_utterance_punctuation(cls, utterance):
        utterance = re.sub('[‘’\'“”\".!,;:+/]|\?$|<|>', '', utterance)
        return cls.remove_redundant_whitespaces(utterance)

    @classmethod
    def remove_insecure_transcription_marker(cls, utterance):
        return re.sub('\[\?\]', '', utterance)

    @classmethod
    def clean_utterance(cls, utterance):
        for cleaning_method in [
                super().clean_utterance, cls.remove_utterance_punctuation,
                cls.remove_insecure_transcription_marker]:
            utterance = cleaning_method(utterance)

        return utterance

    @staticmethod
    def remove_morph_tier_punctuation(morpheme_tier):
        return re.sub('[‘’\'“”\".!,:?+/]', '', morpheme_tier)

    @staticmethod
    def unify_unknown(morpheme_tier):
        return re.sub('xxx?|www', '???', morpheme_tier)

    @classmethod
    def clean_morph_tier(cls, morph_tier):
        for cleaning_method in [
                cls.remove_morph_tier_punctuation, cls.unify_unknown]:
            morph_tier = cleaning_method(morph_tier)
        return morph_tier

    @classmethod
    def get_lang_tier(cls, rec_dict):
        return cls.get_gloss_tier(rec_dict)

    @classmethod
    def get_langs(cls, morpheme_lang_word):
        return ['Indonesian' for _ in cls.get_morphemes(morpheme_lang_word)]
