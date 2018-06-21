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
