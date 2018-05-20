import contextlib
import mmap
import re


class SessionParser:
    """Parser for a session."""

    def __init__(self, session_path):
        """Set the path of the session file."""
        self.session_path = session_path


class RecordParser(SessionParser):
    """Parser for records of a session."""
    pass


class CHATRecordParser(RecordParser):
    """Parser for CHAT records of a session."""

    def iter_records(self):
        """Yield a record of the CHAT file.

        A record starts with ``*speaker_label:\t`` in CHAT.

        Yields:
            dict: The next record in the CHAT file.

        """
        with open(self.session_path, 'rb') as f:
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

                    yield self.get_rec_dict(rec_str)

                    # set new start of record
                    rec_start_pos = next_rec_start_pos

                # handle last record
                rec_str = text[rec_start_pos:].decode()
                yield self.get_rec_dict(rec_str)

    def get_rec_dict(self, rec_str):
        """Get a record dictionary from the stringified record.

        The dictionary has the following keys:
            utterance
            speaker_label
            start
            end
            dependent_tier_name1
            dependent_tier_name2
            <further dependent tiers>

        Args:
            rec_str (str): The stringified record.

        Returns:
            dict: The record dictionary.

        """
        rec_dict = {}
        rec_str = self.remove_line_breaks(rec_str)
        main_line_dict = self.get_main_line_dict(rec_str)
        dependent_tiers_dict = self.get_dependent_tiers(rec_str)
        rec_dict.update(main_line_dict)
        rec_dict.update(dependent_tiers_dict)
        return rec_dict


    def remove_line_breaks(self, rec_str):
        """Remove line breaks within main line or dependent tiers.

        CHAT inserts line breaks when the text of a main line or dependent
        tier becomes too long.

        Args:
            rec_str (str): The stringified record.

        Returns:
            str: record without break lines within main line or dependent tiers

        """
        return rec_str.replace('\n\t', ' ')

    def get_main_line_dict(self, record_str):
        """Get the main line dictionary from the record.

        The dictionary has the following keys:
            utterance
            speaker_label
            start
            end

        Args:
            record_str (str): The stringified record.

        Returns:
            dict: The main line dictionary.

        """
        main_line_dict = {}
        main_line = self.get_main_line_str(record_str)
        main_line_dict['speaker_label'] = self.get_speaker_label(main_line)
        main_line_dict['utterance'] = self.get_utterance(main_line)
        main_line_dict['start'] = self.get_start(main_line)
        main_line_dict['end'] = self.get_end(main_line)

        return main_line_dict

    def get_main_line_str(self, record_str):
        """Get the stringified main line from the record.

        Args:
            record_str (str): The stringified record.

        Returns:
            str: The stringified main line.

        """
        main_line_regex = re.compile(r'\*[A-Z]{3}:\t.*')
        return main_line_regex.search(record_str).group()

    def get_speaker_label(self, main_line):
        """Get speaker label from the main line.

        Args:
            main_line (str): The stringified main line.

        Returns:
            str: The speaker label.

        """
        speaker_label_regex = re.compile(r'(?<=^\*)[A-Z]{3}')
        return speaker_label_regex.search(main_line).group()

    def get_utterance(self, main_line):
        """Get utterance from the main line.

        Args:
            main_line (str): The stringified main line.

        Returns:
            str: The utterance.

        """
        utterance_regex = re.compile(r'(?<=:\t).*[.!?]')
        return utterance_regex.search(main_line).group()

    def get_start(self, main_line):
        """Get start time from the main line.

        Args:
            main_line (str): The stringified main line.

        Returns:
            str: The start time.

        """
        start_regex = re.compile(r'\d+(?=_\d+)')
        match = start_regex.search(main_line)
        # start time might be missing
        if match is None:
            return None
        else:
            return match.group()

    def get_end(self, main_line):
        """Get end time from the main line.

        Args:
            main_line (str): The stringified main line.

        Returns:
            str: The end time.

        """
        # look-behind does not work here, therefore we use a capturing group
        end_regex = re.compile(r'(\d+_)(\d+)')
        match = end_regex.search(main_line)
        # end time might be missing
        if match is None:
            return None
        else:
            return match.group(2)

    def get_dependent_tiers(self, record_str):
        """Get the dependent tiers from the record.

        Args:
            record_str (str): The stringified record.

        Returns:
            dict: The dependent tiers with name as key and content as value.

        """
        dependent_tiers = {}

        dependent_tiers_regex = re.compile(r'%[a-z]+:\t.*')
        for match in dependent_tiers_regex.finditer(record_str):
            dependent_tier = match.group()
            name, content = self.get_dependent_tier(dependent_tier)
            dependent_tiers[name] = content

        return dependent_tiers

    def get_dependent_tier(self, dependent_tier):
        """Get the name and content of the dependent tier.

        Args:
            dependent_tier (str): The stringified dependent tier.

        Returns:
            tuple: The name and content of the dependent tier.

        """
        dependent_tier_regex = re.compile(r'%([a-z]+):\t(.*)')
        match = dependent_tier_regex.search(dependent_tier)
        tier_name = match.group(1)
        tier_content = match.group(2)
        return tier_name, tier_content


if __name__ == '__main__':
    import glob
    import acqdiv
    import os
    import time

    start_time = time.time()

    acqdiv_path = os.path.dirname(acqdiv.__file__)
    corpora_path = os.path.join(acqdiv_path, 'corpora/*/cha/*.cha')

    for path in glob.iglob(corpora_path):

        rec_parser = CHATRecordParser(path)

        for rec in rec_parser.iter_records():
            pass

    print('--- %s seconds ---' % (time.time() - start_time))
