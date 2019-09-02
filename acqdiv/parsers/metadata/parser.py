import os
import re

from lxml import objectify


class MetadataParser(object):
    """ Base metadata parser class.

    metadata.MetadataParser wraps an lxml.objectify tree. It gets relevant metadata
    from the tree and exposes them in a dictionary.

    Attributes:
        metadata: A dictionary of all metadata values extracted from the
                  file the tree was initialized with.
    """

    def __init__(self, path):
        self.path = path
        self.tree = objectify.parse(path)
        self.root = self.tree.getroot()
        self.metadata = {
            '__attrs__': self.parse_attrs(self.root),
                    }
        self.metadata['__attrs__']['Cname'] = re.sub(r'\.xml.*|\.imdi.*', "", os.path.basename(str(self.path)))

        # Special case for Indonesian
        # Explanation: this converts the session ID to the same format as in the body files
        # Unless that issue was fixed in another way we will probably still want it

        # TODO: figure out what's going wrong with Indonesian
        """
        print(self.metadata['__attrs__']['Cname'])

        if self.metadata_path['corpus'] == "Indonesian":
            match = re.match(r"(\w{3})-\d{2}(\d{2})-(\d{2})-(\d{2})",self.metadata['__attrs__']['Cname'])
            self.metadata['__attrs__']['Cname'] = match.group(1).upper() + '-' + match.group(4) + match.group(3) + match.group(2)
        self.metadata['__attrs__']['schemaLocation'] = self.metadata['__attrs__'].pop('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
        """
        # assert existing_dir(self.input_path())


    def parse_attrs(self, e):
        """
        Parses and returns attributes of the root node.

        args:
            e: root node of an XML session file

        returns:
            A dictionary of all attributes of e.
        """
        return {k: e.attrib[k] for k in e.keys()}


    def get_everything(self, root):
        """
        Parses and returns a list of all tag tuples in the tree.

        args:
            root: Root node of an XML session file

        returns:
            a list of tuples, each representing all tags of a node
        """
        everything = []
        for e in root.getiterator():
            if e is not None:
                everything.append((e.tag.replace("{http://www.mpi.nl/IMDI/Schema/IMDI}", ""), e))
        return everything