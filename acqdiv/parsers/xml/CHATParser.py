import contextlib
import mmap
import re


class CHATParser:
    """Parser for CHAT metadata and records of a session."""

    # ---------- session processing ----------

    @staticmethod
    def get_metadata(session_path):
        """Get the metadata of a session."""
        pass

    @staticmethod
    def iter_records(session_path):
        """Yield a record of the CHAT file.

        A record starts with ``*speaker_label:\t`` in CHAT.

        Yields:
            str: The next record.
        """
        with open(session_path, 'rb') as f:
            # use memory-mapping of files
            with contextlib.closing(
                    mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as text:

                # create a record generator
                rec_generator = re.finditer(br'\*[A-Z]{3}:\t', text)

                # get start of first record
                rec_start_pos = next(rec_generator).start()

                # iter all records
                for rec in rec_generator:

                    # get start of next record
                    next_rec_start_pos = rec.start()

                    # get the stringified record
                    rec_str = text[rec_start_pos:next_rec_start_pos].decode()

                    yield rec_str

                    # set new start of record
                    rec_start_pos = next_rec_start_pos

                # handle last record
                rec_str = text[rec_start_pos:].decode()
                yield rec_str

    # ---------- record processing ----------

    @staticmethod
    def remove_line_breaks(rec):
        """Remove line breaks within the tiers of a record.

        CHAT inserts line breaks when the text of a main line or dependent
        tier becomes too long.

        Args:
            rec (str): The record.

        Returns:
            str: Record without break lines within the tiers.
        """
        return rec.replace('\n\t', ' ')

    @classmethod
    def get_main_line(cls, rec):
        """Get the main line of the record."""
        rec = cls.remove_line_breaks(rec)
        main_line_regex = re.compile(r'\*[A-Z]{3}:\t.*')
        return main_line_regex.search(rec).group()

    @staticmethod
    def get_dependent_tier(rec, name):
        """Get the content of the dependent tier from the record.

        Args:
            rec (str): The record.
            name (str): The name of the dependent tier.

        Returns:
            str: The content of the dependent tier.
        """
        dependent_tier_regex = re.compile(r'%{}:\t(.*)'.format(name))
        match = dependent_tier_regex.search(rec)
        if match is None:
            return None
        else:
            return match.group(1)

    # ---------- main line processing ----------

    @staticmethod
    def get_speaker_label(main_line):
        """Get the speaker label from the main line.

        Args:
            main_line (str): The main line.

        Returns:
            str: The speaker label.

        """
        speaker_label_regex = re.compile(r'(?<=^\*)[A-Z]{3}')
        return speaker_label_regex.search(main_line).group()

    @staticmethod
    def get_utterance(main_line):
        """Get the utterance from the main line.

        Args:
            main_line (str): The main line.

        Returns:
            str: The utterance.
        """
        utterance_regex = re.compile(r'(?<=:\t).*[.!?]')
        return utterance_regex.search(main_line).group()

    @staticmethod
    def get_time(main_line):
        """Get the time from the main line.

        Args:
            main_line (str): The main line.

        Returns:
            str: The time consisting of start and end time.
        """
        time_regex = re.compile(r'\d+_\d+')
        match = time_regex.search(main_line)
        if match is None:
            return ''
        else:
            return match.group()

    # ---------- utterance processing ----------

    @staticmethod
    def get_shortening_actual(utterance):
        """Get the actual form of shortenings.

        Coding in CHAT: parentheses within word.
        The part with parentheses is removed.
        """
        shortening_regex = re.compile(r'(\S*)\(\S+\)(\S*)')
        return shortening_regex.sub(r'\1\2', utterance)

    @staticmethod
    def get_shortening_target(utterance):
        """Get the target form of shortenings.

        Coding in CHAT: \w+(\w+)\w+ .
        The part in parentheses is kept, parentheses are removed.
        """
        shortening_regex = re.compile(r'(\S*)\((\S+)\)(\S*)')
        return shortening_regex.sub(r'\1\2\3', utterance)

    @staticmethod
    def get_replacement_actual(utterance):
        """Get the actual form of replacements.

        Coding in CHAT: [: <words>] .
        Keeps replaced words, removes replacing words with brackets.
        """
        # several scoped words
        replacement_regex1 = re.compile(r'<(.*?)> \[: .*?\]')
        clean = replacement_regex1.sub(r'\1', utterance)
        # one scoped word
        replacement_regex2 = re.compile(r'(\S+) \[: .*?\]')
        return replacement_regex2.sub(r'\1', clean)

    @staticmethod
    def get_replacement_target(utterance):
        """Get the target form of replacements.

        Coding in CHAT: [: <words>] .
        Removes replaced words, keeps replacing words with brackets.
        """
        replacement_regex = re.compile(r'(?:<.*?>|\S+) \[: (.*?)\]')
        return replacement_regex.sub(r'\1', utterance)

    @staticmethod
    def get_fragment_actual(utterance):
        """Get the actual form of fragments.

        Coding in CHAT: word starting with &.
        Keeps the fragment, removes the & from the word.
        """
        fragment_regex = re.compile(r'&(\S+)')
        return fragment_regex.sub(r'\1', utterance)

    @staticmethod
    def get_fragment_target(utterance):
        """Get the target form of fragments.

        Coding in CHAT: word starting with &.
        The fragment is marked as untranscribed (xxx).
        """
        fragment_regex = re.compile(r'&\S+')
        return fragment_regex.sub('xxx', utterance)

    @classmethod
    def get_actual_form(cls, utterance):
        """Get the actual form of the utterance."""
        for actual_method in [cls.get_shortening_actual,
                              cls.get_fragment_actual,
                              cls.get_replacement_actual]:
            utterance = actual_method(utterance)

        return utterance

    @classmethod
    def get_target_form(cls, utterance):
        """Get the target form of the utterance."""
        for target_method in [cls.get_shortening_target,
                              cls.get_fragment_target,
                              cls.get_replacement_target]:
            utterance = target_method(utterance)

        return utterance

    @staticmethod
    def get_sentence_type(utterance):
        """Get the sentence type of an utterance.

        The sentence type is inferred from the utterance terminator.
        """
        mapping = {'.': 'declarative',
                   '?': 'question',
                   '!': 'exclamation',
                   '+.': 'broken for coding',
                   '+..': 'trail off',
                   '+..?': 'trail off of question',
                   '+!?': 'question with exclamation',
                   '+/.': 'interruption',
                   '+/?': 'interruption of a question',
                   '+//.': 'self-interruption',
                   '+//?': 'self-interrupted question',
                   '+"/.': 'quotation follows',
                   '+".': 'quotation precedes'}
        terminator_regex = re.compile(r'([+/.!?"]*[!?.])(?=( \[\+|$))')
        match = terminator_regex.search(utterance)
        return mapping[match.group(1)]

    # ---------- time processing ----------

    @staticmethod
    def get_start(rec_time):
        """Get the start time from the time.

        Args:
            rec_time (str): The time.

        Returns:
            str: The start time.
        """
        if not rec_time:
            return rec_time
        else:
            start_regex = re.compile(r'(\d+)_')
            return start_regex.search(rec_time).group(1)

    @staticmethod
    def get_end(rec_time):
        """Get the end time from the time.

        Args:
            rec_time (str): The time.

        Returns:
            str: The end time.
        """
        if not rec_time:
            return rec_time
        else:
            end_regex = re.compile(r'_(\d+)')
            return end_regex.search(rec_time).group(1)

###############################################################################

class InuktitutParser(CHATParser):
    """Inferences for Inuktitut."""

    @staticmethod
    def get_actual_alternative(utterance):
        """Get the actual form of alternatives.

        Coding in CHAT: [=? <words>]
        The actual form is the alternative given in brackets.
        """
        replacement_regex = re.compile(r'(?:<.*?>|\S+) \[=\? (.*?)\]')
        return replacement_regex.sub(r'\1', utterance)

    @staticmethod
    def get_target_alternative(utterance):
        """Get the target form of alternatives.

        Coding in CHAT: [=? <words>]
        The target form is the original form.
        """
        # several scoped words
        alternative_regex1 = re.compile(r'<(.*?)> \[=\? .*?\]')
        clean = alternative_regex1.sub(r'\1', utterance)
        # one scoped word
        alternative_regex2 = re.compile(r'(\S+) \[=\? .*?\]')
        return alternative_regex2.sub(r'\1', clean)

    @classmethod
    def get_actual_form(cls, utterance):
        """Get the actual form of the utterance.

        Considers alternatives as well.
        """
        utterance = super().get_actual_form(utterance)
        return cls.get_actual_alternative(utterance)

    @classmethod
    def get_target_form(cls, utterance):
        """Get the target form of the utterance.

        Considers alternatives as well.
        """
        utterance = super().get_target_form(utterance)
        return cls.get_target_alternative(utterance)

    @classmethod
    def iter_words(cls, tier):
        for word in tier.split(' '):
            yield word

    @classmethod
    def iter_morphemes(cls, word):
        morpheme_regex = re.compile(r'(\w+|)+')
        for morpheme in word.split('+'):
            pass


if __name__ == '__main__':
    import glob
    import acqdiv
    import os
    import time

    start_time = time.time()

    acqdiv_path = os.path.dirname(acqdiv.__file__)
    corpora_path = os.path.join(acqdiv_path, 'corpora/*/cha/*.cha')

    for path in glob.iglob(corpora_path):

        chat_parser = CHATParser()

        for rec in chat_parser.iter_records(path):
            main_line = chat_parser.get_main_line(rec)
            speaker_label = chat_parser.get_speaker_label(main_line)
            utterance = chat_parser.get_utterance(main_line)
            rec_time = chat_parser.get_time(main_line)
            start = chat_parser.get_start(rec_time)
            end = chat_parser.get_end(rec_time)

    print('--- %s seconds ---' % (time.time() - start_time))

    parser = CHATParser()
    print(repr(parser.get_shortening_actual(
        'This (i)s a short(e)ned senten(ce)')))
    print(repr(parser.get_shortening_target(
        'This (i)s a short(e)ned senten(ce)')))
    print(repr(parser.get_replacement_actual(
        'This us [: is] <srane suff> [: strange stuff]')))
    print(repr(parser.get_replacement_target(
        'This us [: is] <srane suff> [: strange stuff]')))
    print(repr(parser.get_fragment_actual('This is &at .')))
    print(repr(parser.get_fragment_target('This is &at .')))
    print(repr(parser.get_sentence_type('This is a sent +!?')))

    inuktitut_parser = InuktitutParser()
    print(repr(inuktitut_parser.get_actual_alternative(
        'This is the target [=? actual] form.')))
    print(repr(inuktitut_parser.get_target_alternative(
        'This is the target [=? actual] form.')))

    test = 'LR|qa^outside+LI|unnga^ALL+VZ|aq^go_by_way_of+VV|VA|' \
           'tit^CAUS+VV|lauq^POL+VI|nnga^IMP_2sS_1sO VR|' \
           'nimak^move_around+VV|VA|tit^CAUS+VV|nngit^NEG+VI|' \
           'lugu^ICM_XxS_3sO? VR|kuvi^pour+NZ|suuq^HAB+NN|AUG|aluk^EMPH?'
