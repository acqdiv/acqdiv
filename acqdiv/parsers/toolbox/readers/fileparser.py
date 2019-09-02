import re
import mmap
import contextlib

from acqdiv.parsers.toolbox.cleaners.cleaner import ToolboxCleaner
from acqdiv.parsers.toolbox.model.toolbox import ToolboxFile
from acqdiv.parsers.toolbox.model.record import Record

@contextlib.contextmanager
def memorymapped(path, access=mmap.ACCESS_READ):
    """ Return a block context with path as memory-mapped file. """
    fd = open(path)
    try:
        m = mmap.mmap(fd.fileno(), 0, access=access)
    except Exception:
        fd.close()
        raise
    try:
        yield m
    finally:
        m.close()
        fd.close()


class ToolboxFileParser:
    """Methods for creating a ToolboxFile instance."""

    @classmethod
    def parse(cls, path, separator):
        """Get a ToolboxFile instance.

        Args:
            path (str): Path to Toolbox file.
            separator (str): Field that marks beginning of a record.

        Returns:
            acqdiv.parsers.toolbox.model.toolbox.ToolboxFile: The Toolbox
            instance.
        """
        toolbox = ToolboxFile()

        with open(path, 'rb') as f:
            for record in cls.iter_records(f, separator):
                rec_dict = cls.get_record_dict(record)
                rec = Record()
                rec.tiers = rec_dict
                toolbox.records.append(rec)

        return toolbox

    @classmethod
    def iter_records(cls, toolbox_file, separator):
        """Iter the records of a toolbox file.

        Args:
            toolbox_file (file/file-like): The toolbox file.
            separator (str): Fieldmarker that marks beginning of record.

        Yields:
            str: The record.
        """
        _record_marker = re.compile(separator)

        with contextlib.closing(mmap.mmap(toolbox_file.fileno(),
                                          0, access=mmap.ACCESS_READ)) as data:
            ma = _record_marker.search(data)
            pos = ma.start()
            for ma in _record_marker.finditer(data, ma.end()):
                yield data[pos:ma.start()].decode()
                pos = ma.start()

            if ma is None:
                raise StopIteration
            else:
                yield data[pos:].decode()

    @classmethod
    def get_record_dict(cls, record):
        """Get the record dictionary.

        Metadata is ignored and returned as an empty dictionary.

        Args:
            record (str): Toolbox record.

        Returns:
            dict: Key and content of tiers.
        """
        rec_dict = {}

        # iter tiers of the record
        for tier in cls.get_tiers(record):
            # get field marker and content of tier
            field_marker, content = cls.get_tier(tier)
            # clean the content
            content = ToolboxCleaner.remove_redundant_whitespaces(content)

            # add content to dictionary
            rec_dict[field_marker] = content

        return rec_dict

    @staticmethod
    def get_tiers(record):
        """Return tiers of the record.

        Args:
            record (str): The record.

        Returns:
            list: The tiers of the record.
        """
        return record.split('\n')

    @staticmethod
    def get_tier(tier):
        """Return field marker and content.

        Args:
            tier (str): '\\name content'.

        Returns:
            tuple: (name, content).
        """
        # split into field marker and content
        tokens = re.split(r'\s+', tier, maxsplit=1)
        # get field marker
        field_marker = tokens[0]
        # remove \\ before the field marker
        field_marker = field_marker.replace("\\", "")

        # if content is missing
        if len(tokens) <= 1:
            content = ''
        else:
            content = tokens[1]

        return field_marker, content
