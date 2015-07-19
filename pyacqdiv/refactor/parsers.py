""" Parsers for parsing CHAT XML and Toolbox files for acqdiv corpora
"""

# TODO: integrate the Corpus specific parsing routines from the body parser
# TODO: integrate the metadata parsing

class SessionParser(object):
    # Static class-level method to create a new parser instance
    # based on session format type.
    def create_parser(config):
        format = config.format()
        if format == "ChatXML":
            return ChatXMLParser(config)
        if format == "Toolbox":
            return ToolboxParser(config)
        assert 0, "Unknown format type: " + format
    create_parser(config) = staticmethod(create_parser)

    def __init__(self, config):
        self.config = config

    # To be overridden in subclasses.

    # Session metadata for the Sessions table in the db
    def get_session_metadata(self):
        pass

    # Generator to yield Speakers for the Speaker table in the db
    def next_speaker(self):
        pass

    # Generator to yield Utterances for the Utterance table in the db
    def next_utterance(self):
        pass


class ChatXMLParser(SessionParser):
    # Note: do we need additional special syntax to indicate that we're extending Session?

    # Note: make sure this is overriding the superclass.parse. Need a keyword?
    def get_session_metadata(self):
        # Do xml-specific parsing of session metadata.
        # The config so it knows what symbols to look for.
        pass

    # Generator to yield Speakers for the Speaker table in the db
    def next_speaker(self):
        pass

    # Note: make sure this is overriding the superclass.parse. Need a keyword?
    def next_utterance(self):
        # Do xml-specific parsing of utterances.
        # The config so it knows what symbols to look for.
        pass

    # not sure here how @rabart extracts stuff from the XML, but Xpath
    #  seems reasonable; esp becuz you can get the patterns for free from
    #  the developer tools in some browsers

class ToolboxParser(SessionParser):
    # Note: do we need additional special syntax to indicate that we're extending Session?

    # Note: make sure this is overriding the superclass.parse. Need a keyword?
    def get_session_metadata(self):
        # Do toolbox-specific parsing of session metadata.
        # Presumably we will have to look for the metadata file in the config.
        # The config so it knows what symbols to look for.
        pass

    # Generator to yield Speakers for the Speaker table in the db
    def next_speaker(self):
        pass

    # Note: make sure this is overriding the superclass.parse. Need a keyword?
    def next_utterance(self):
        # Do toolbox-specific parsing of utterances.
        # The config so it knows what symbols to look for.
        pass
