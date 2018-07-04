import re


class CHATCleaner:
    """Clean parts of a CHAT record.

    Note:
        The order of calling the cleaning methods has great impact on the final
        result, e.g. handling of repetitions has to be done first, before
        scoped symbols are removed.
    """

    @staticmethod
    def remove_redundant_whitespaces(utterance):
        """Remove redundant whitespaces in utterances.

        Strips multiple whitespaces as well as leading and trailing
        whitespaces. This method is routinely called by various
        cleaning methods.
        """
        whitespace_regex = re.compile(r'\s+')
        return whitespace_regex.sub(' ', utterance).strip(' ')

    @classmethod
    def remove_terminator(cls, utterance):
        """Remove the terminator from the utterance.

        There are 13 different terminators in CHAT. Coding: [+/.!?"]*[!?.]  .
        """
        # postcodes or nothing may follow terminators
        terminator_regex = re.compile(r'[+/.!?"]*[!?.](?=( \[\+|$))')
        clean = terminator_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    @staticmethod
    def null_untranscribed_utterances(utterance):
        """Null utterances containing only untranscribed material.

        Note:
            Nulling means here the utterance is returned as an empty string.
        """
        if utterance == 'xxx':
            return ''
        else:
            return utterance

    @staticmethod
    def null_event_utterances(utterance):
        """Null utterances that are events.

        CHAT coding: 0
        """
        if utterance == '0':
            return ''
        else:
            return utterance

    @classmethod
    def remove_events(cls, utterance):
        """Remove events from the utterance.

        Coding in CHAT: word starting with &=.
        """
        event_regex = re.compile(r'&=\S+')
        clean = event_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    @staticmethod
    def handle_repetitions(utterance):
        """Write out repeated words in the utterance.

        Coding in CHAT: [x <number>]  .
        """
        repetition_regex = re.compile(r'(?:<(.*?)>|(\S+)) \[x (\d)\]')
        # build cleaned utterance
        clean = ''
        match_end = 0
        for match in repetition_regex.finditer(utterance):
            # add material preceding match
            match_start = match.start()
            clean += utterance[match_end:match_start]

            # check whether it has scope over one or several words
            if match.group(1):
                words = match.group(1)
            else:
                words = match.group(2)

            # repeat the word
            repetitions = int(match.group(3))
            clean += ' '.join([words]*repetitions)

            match_end = match.end()

        # add material following last match
        clean += utterance[match_end:]

        if clean:
            return clean
        else:
            return utterance

    @classmethod
    def remove_omissions(cls, utterance):
        """Remove omissions in the utterance.

        Coding in CHAT: word starting with 0.
        """
        omission_regex = re.compile(r'0\S+')
        clean = omission_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    @staticmethod
    def unify_untranscribed(utterance):
        """Unify untranscribed material as xxx.

        Coding in CHAT: xxx, yyy, www   .
        """
        untranscribed_regex = re.compile(r'yyy|www')
        return untranscribed_regex.sub('xxx', utterance)

    @staticmethod
    def remove_form_markers(utterance):
        """Remove form markers from the utterance.

        Coding in CHAT: word ending with @.
        The @ and the part after it are removed.
        """
        form_marker_regex = re.compile(r'(\S+)@\S+')
        return form_marker_regex.sub(r'\1', utterance)

    @staticmethod
    def remove_linkers(utterance):
        """Remove linkers from the utterance.

        Coding in CHAT: +["^,+<] (always in the beginning of utterance).
        """
        linker_regex = re.compile(r'^\+["^,+<]')
        return linker_regex.sub('', utterance).lstrip(' ')

    @staticmethod
    def remove_separators(utterance):
        """Remove separators from the utterance.

        Separators are commas, colons or semi-colons which are surrounded
        by whitespaces.
        """
        separator_regex = re.compile(r' [,:;]( )')
        return separator_regex.sub(r'\1', utterance)

    @classmethod
    def remove_ca(cls, utterance):
        """Remove conversation analysis and satellite markers from utterance.

        Note:
            Only four markers (↓↑‡„) are attested in the corpora. Only those
            will be checked for removal.
        """
        ca_regex = re.compile(r'[↓↑‡„]')
        clean = ca_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    @staticmethod
    def remove_fillers(utterance):
        """Remove fillers from the utterance.

        Coding in CHAT: word starts with &-
        """
        filler_regex = re.compile(r'&-(\S+)')
        return filler_regex.sub(r'\1', utterance)

    @staticmethod
    def remove_pauses_within_words(utterance):
        """Remove pauses within words from the utterance.

        Coding in CHAT: ^ within word
        """
        pause_regex = re.compile(r'(\S+)\^(\S+)')
        return pause_regex.sub(r'\1\2', utterance)

    @staticmethod
    def remove_blocking(utterance):
        """Remove blockings in words from the utterance.

        Coding in CHAT: ^ at the beginning of the word
        """
        blocking_regex = re.compile(r'(^| )\^(\S+)')
        return blocking_regex.sub(r'\1\2', utterance)

    @classmethod
    def remove_pauses_between_words(cls, utterance):
        """Remove pauses between words from the utterance.

        Coding in CHAT: (.), (..), (...)
        """
        pause_regex = re.compile(r'\(\.{1,3}\)')
        clean = pause_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    @staticmethod
    def remove_drawls(utterance):
        """Remove drawls from the utterance.

        Coding in CHAT: : within or after word
        """
        drawl_regex = re.compile(r'(\S+):(\S+)?')
        return drawl_regex.sub(r'\1\2', utterance)

    @classmethod
    def remove_scoped_symbols(cls, utterance):
        """Remove scoped symbols from utterance.

        Coding in CHAT: < > [.*]    .

        Note:
            Scoped symbols can be nested:
                - word [...][...]
                - <word [...] word> [...]
                - <<word word> [...] word> [...]
        """
        scope_regex = re.compile(r'<|>|\[.*?\]')
        clean = scope_regex.sub('', utterance)
        return cls.remove_redundant_whitespaces(clean)

    # **********************************************************
    # ********** Processor interface cleaning methods **********
    # **********************************************************

    # ---------- utterance cleaning ----------

    @classmethod
    def clean_utterance(cls, utterance):
        """Return the cleaned utterance."""
        for cleaning_method in [
                cls.null_event_utterances, cls.unify_untranscribed,
                cls.handle_repetitions, cls.remove_terminator,
                cls.remove_events, cls.remove_omissions,
                cls.remove_form_markers, cls.remove_linkers,
                cls.remove_separators, cls.remove_ca,
                cls.remove_fillers, cls.remove_pauses_within_words,
                cls.remove_pauses_between_words, cls.remove_blocking,
                cls.remove_drawls, cls.remove_scoped_symbols,
                cls.null_untranscribed_utterances]:
            utterance = cleaning_method(utterance)

        return utterance

    # ---------- morphology tier cleaning ----------

    @staticmethod
    def clean_seg_tier(seg_tier):
        """Clean the segment tier."""
        return seg_tier

    @staticmethod
    def clean_gloss_tier(gloss_tier):
        """Clean the gloss tier."""
        return gloss_tier

    @staticmethod
    def clean_pos_tier(pos_tier):
        """Clean the POS tag tier."""
        return pos_tier

    # ---------- tier cross cleaning ----------

    @staticmethod
    def cross_clean(utterance, seg_tier, gloss_tier, pos_tier):
        """Clean across different tiers."""
        return utterance, seg_tier, gloss_tier, pos_tier

    # ---------- morpheme word cleaning ----------

    @staticmethod
    def clean_seg_word(seg_word):
        """Clean the segment word."""
        return seg_word

    @staticmethod
    def clean_gloss_word(gloss_word):
        """Clean the gloss word."""
        return gloss_word

    @staticmethod
    def clean_pos_word(pos_word):
        """Clean the POS tag word."""
        return pos_word

    # ---------- morpheme cleaning ----------

    @staticmethod
    def clean_segment(segment):
        """Clean the segment."""
        return segment

    @staticmethod
    def clean_gloss(gloss):
        """Clean the gloss."""
        return gloss

    @staticmethod
    def clean_pos(pos):
        """Clean the POS tag."""
        return pos


###############################################################################


class InuktitutCleaner(CHATCleaner):

    @staticmethod
    def replace_pos_separator(pos):
        """Replace the POS tag separator.

        A morpheme may have several POS tags separated by a pipe.
        POS tags to the right are subcategories of the POS tags to the left.
        The separator is replaced by a dot.

        Args:
            pos (str): The POS tag.

        Returns:
            str: POS tag separator replaced by a dot.
        """
        return pos.replace('|', '.')

    @staticmethod
    def replace_stem_gram_gloss_connector(gloss):
        """Replace the stem and grammatical gloss connector.

        A stem gloss is connected with a grammatical gloss by an ampersand.
        The connector is replaced by a dot.

        Args:
            gloss (str): The gloss.

        Returns:
            str: The stem and grammatical connector replaced by a dot.
        """
        return gloss.replace('&', '.')

    @staticmethod
    def remove_english_marker(seg):
        """Remove the marker for english words.

        English segments are marked with the form marker '@e'.

        Args:
            seg (str): The segment.

        Returns:
            str: The segment without '@e'.
        """
        english_marker_regex = re.compile(r'(\S+)@e')
        return english_marker_regex.sub(r'\1', seg)

    @classmethod
    def clean_xmor(cls, xmor):
        """Clean the morphology tier 'xmor'."""
        for cleaning_method in [cls.null_event_utterances,
                                cls.unify_untranscribed,
                                cls.remove_terminator,
                                cls.remove_separators,
                                cls.remove_scoped_symbols,
                                cls.null_untranscribed_utterances]:
            xmor = cleaning_method(xmor)

        return xmor

    # **********************************************************
    # ********** Processor interface cleaning methods **********
    # **********************************************************

    # ---------- morphology tier cleaning ----------

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        """Clean the xmor tier."""
        return cls.clean_xmor(seg_tier)

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        """Clean the xmor tier."""
        return cls.clean_xmor(gloss_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        """Clean the xmor tier."""
        return cls.clean_xmor(pos_tier)

    # ---------- morpheme cleaning ----------

    @classmethod
    def clean_segment(cls, seg):
        """Remove english markers from the segment."""
        return cls.remove_english_marker(seg)

    @classmethod
    def clean_gloss(cls, gloss):
        """Replace the stem and grammatical gloss connector."""
        return cls.replace_stem_gram_gloss_connector(gloss)

    @classmethod
    def clean_pos(cls, pos):
        """Replace the POS tag separator."""
        return cls.replace_pos_separator(pos)


###############################################################################


class CreeCleaner(CHATCleaner):

    @staticmethod
    def remove_morph_separators(utterance):
        """Remove morpheme separators in the utterance.

        Words may contain an underscore as a morpheme separator, e.g.
        'giddy_up', in the utterance.
        """
        morph_sep_regex = re.compile(r'(\S+)_(\S+)')
        return morph_sep_regex.sub(r'\1\2', utterance)

    @staticmethod
    def replace_zero(utterance):
        """Replace zéro morphemes in the utterance.

        'zéro' stands for zero morphemes is replaced by 'Ø'.
        """
        return utterance.replace('zéro', 'Ø')

    @staticmethod
    def replace_morpheme_separator(utterance):
        """Replace morpheme separators in the utterance.

        Morphemes are separated by a tilde.
        """
        return utterance.replace('~', '')

    @staticmethod
    def remove_square_brackets(morph_tier):
        """Remove redundant square brackets around morphology tiers.

        Morphology tiers have square brackets at their edges which can be
        removed. It is unclear what their purpose is.
        """
        return morph_tier.lstrip('[').rstrip(']')

    @staticmethod
    def replace_eng(gloss_tier, utterance):
        """Replace the 'Eng' glosses by the actual words in the gloss tier.

        Returns:
            str: The gloss tier with all its 'Eng' glosses replaced.
        """
        gloss_words = gloss_tier.split(' ')
        utterance_words = utterance.split(' ')

        # check if the words are correctly aligned
        if len(gloss_words) != len(utterance_words):
            return gloss_tier
        else:
            new_gloss_words = []
            for gloss_word, actual_word in zip(gloss_words, utterance_words):
                if 'Eng' in gloss_word:
                    new_gloss_words.append(actual_word)
                else:
                    new_gloss_words.append(gloss_word)
            return ' '.join(new_gloss_words)

    @staticmethod
    def replace_percentages(word):
        """Replace words consisting of percentages.

        '%%%' stand for untranscribed words. They are replaced by '???'.
        """
        if word == '%%%':
            return '???'
        else:
            return word

    @staticmethod
    def replace_hashtag(morph_element):
        """Replace words and morphemes consisting of a hashtag.

        '#' stands for unglossed words and morphemes. It is replaced by
        '???'
        """
        if morph_element == '#':
            return '???'
        else:
            return morph_element

    @staticmethod
    def handle_question_mark(morph_element):
        """Handle question marks in words and morphemes.

        '?' stands for unclear meanings of a morpheme and word. If it only
        consists of '?', it is replaced by '???'. If there is a form followed
        by '?', it is removed.
        """
        if morph_element == '?':
            return '???'

        return morph_element.repalce('?', '')

    @classmethod
    def replace_star(cls, morph_element):
        """Replace words or morphemes consisting of a star.

        The star marks an element that does not correspond to an element on
        another morphology tier. It is replaced by a '???'.
        """
        if morph_element == '*':
            return '???'
        else:
            return None

    @staticmethod
    def replace_gloss_connector(gloss):
        """Replace the gloss connectors.

        There are three different gloss connectors: '.', '+', ','
        ',' adds an additional specification to a gloss, e.g.
        'p,quest” (question particle)'. '+' and ',' are replaced by a dot.
        """
        return gloss.replace(',', '.').replace('+', '.')

    @staticmethod
    def uppercase_pos_in_parentheses(pos):
        """Uppercase POS tags in parentheses.

        Parentheses indicate covert grammatical categories.
        """
        pos_in_parentheses_regex = re.compile(r'(\()(\S+)(\))')
        # extract POS in parentheses
        match = pos_in_parentheses_regex.search(pos)
        if not match:
            return pos
        else:
            # replace by uppercased version
            up_pos = match.group(2).upper()
            return pos_in_parentheses_regex.sub(r'\1{}\3'.format(up_pos), pos)

    @classmethod
    def clean_morpheme_word(cls, morpheme_word):
        for cleaning_method in [
                cls.replace_percentages, cls.replace_hashtag,
                cls.handle_question_mark, cls.replace_star]:
            morpheme_word = cleaning_method(morpheme_word)

        return morpheme_word

    @classmethod
    def clean_morpheme(cls, morpheme):
        for cleaning_method in [
                cls.replace_hashtag, cls.handle_question_mark,
                cls.replace_star]:
            morpheme = cleaning_method(morpheme)

        return morpheme

    # **********************************************************
    # ********** Processor interface cleaning methods **********
    # **********************************************************

    # ---------- utterance cleaning ----------

    @classmethod
    def clean_utterance(cls, utterance):
        utterance = super().clean_utterance(utterance)
        for cleaning_method in [
                cls.remove_morph_separators, cls.replace_zero,
                cls.replace_morpheme_separator]:
            utterance = cleaning_method(utterance)

        return utterance

    # ---------- morphology tier cleaning ----------

    @classmethod
    def clean_seg_tier(cls, seg_tier):
        return cls.remove_square_brackets(seg_tier)

    @classmethod
    def clean_gloss_tier(cls, gloss_tier):
        return cls.remove_square_brackets(gloss_tier)

    @classmethod
    def clean_pos_tier(cls, pos_tier):
        return cls.remove_square_brackets(pos_tier)

    # ---------- tier cross cleaning ----------

    @classmethod
    def cross_clean(cls, utterance, seg_tier, gloss_tier, pos_tier):
        gloss_tier = cls.replace_eng(gloss_tier, utterance)
        return utterance, seg_tier, gloss_tier, pos_tier

    # ---------- morpheme word cleaning ----------

    @classmethod
    def clean_seg_word(cls, seg_word):
        return cls.clean_morpheme_word(seg_word)

    @classmethod
    def clean_gloss_word(cls, gloss_word):
        return cls.clean_morpheme_word(gloss_word)

    @classmethod
    def clean_pos_word(cls, pos_word):
        return cls.clean_morpheme_word(pos_word)

    # ---------- morpheme cleaning ----------

    @classmethod
    def clean_segment(cls, segment):
        return cls.clean_morpheme(segment)

    @classmethod
    def clean_gloss(cls, gloss):
        gloss = cls.clean_morpheme(gloss)
        return cls.replace_gloss_connector(gloss)

    @classmethod
    def clean_pos(cls, pos):
        pos = cls.clean_morpheme(pos)
        return cls.uppercase_pos_in_parentheses(pos)



if __name__ == '__main__':
    cleaner = CHATCleaner()
    print(repr(cleaner.remove_redundant_whitespaces('Das   ist zu  viel.')))
    print(repr(cleaner.remove_terminator('doa to: (.) mado to: +... [+ bch]')))
    print(repr(cleaner.null_untranscribed_utterances('xxx')))
    print(repr(cleaner.null_event_utterances('0')))
    print(repr(cleaner.remove_events(
        'I know &=laugh what that &=laugh means .')))
    print(repr(cleaner.handle_repetitions(
        'This <is a> [x 3] sentence [x 2].')))
    print(repr(cleaner.remove_omissions('This is 0not 0good .')))
    print(repr(cleaner.unify_untranscribed('This www I yyy is done .')))
    print(repr(cleaner.remove_form_markers('I know the A@l B@l C@l .')))
    print(repr(cleaner.remove_linkers('+" bir de köpek varmış .')))
    print(repr(cleaner.remove_blocking('te^st')))
    print(repr(cleaner.remove_blocking('^test ^test')))
    print(repr(cleaner.remove_separators(
        'that is , that is ; that is : that is .')))
    print(repr(cleaner.remove_ca('up ↑ and down ↓ .')))
    print(repr(cleaner.remove_fillers('&-um what &-um is that &-um .')))
    print(repr(cleaner.remove_pauses_within_words('Th^is is a com^puter .')))
    print(repr(cleaner.remove_pauses_between_words(
        'This (.) is (..) a (...) sentence .')))
    print(repr(cleaner.remove_drawls('Thi:s is tea: .')))
    print(repr(cleaner.remove_scoped_symbols(
        'ji [=! smiling] '
        '<take your shoes off> [!] '
        '(w)a [!!] '
        'Maks [= the name of CHIs dog] '
        'dur silim [: sileyim] '
        'dici [=? dizi] '
        '<Ekin beni yakalayamaz> [% said with singing] '
        'mami cuando [?] '
        'oturduğun [>1] '
        '<lana lana> [/] lana '
        'qaigu [//] qainngitualuk '
        'sen niye bozdun [///] kim bozdu '
        '<<ıspanak bitmediyse de> [/-] yemesin> [<] '
        'blubla [*] '
        'blabla [//][: blabla]')))

    print(repr(cleaner.clean_utterance(
        '<<ıspanak bitmediyse de> [/-] yemesin> [<] '
        'mami cuando [?] ^test test^test '
        'I know ↑ the A@l B@l C@l www blabla yyy '
        'bla:bla 0not 0good &=laugh ! [+ bla]')))

    test = '<DR|u^here&SG_ST+DI|na^ABS_SG> [*] <VR|ukkuaq^close_door+VV|' \
           'ADV|tsiaq^well+VV|nngit^NEG+NZ|juq^that_which+NN|AUG|' \
           'aluk^EMPH+VI|gavit^CSV_2sS.> [*] NR|anaana^mother IACT|' \
           'no@e^no IACT|no@e^no. [+ EX]'

    inuktitut_cleaner = InuktitutCleaner()
