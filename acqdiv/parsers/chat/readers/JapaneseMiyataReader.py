from acqdiv.parsers.chat.readers.ACQDIVCHATReader import ACQDIVCHATReader


class JapaneseMiyataReader(ACQDIVCHATReader):

    @staticmethod
    def get_word_language(word):
        if word.endswith('@s:eng'):
            return 'English'
        elif word.endswith('@s:deu'):
            return 'German'
        else:
            return 'Japanese'
