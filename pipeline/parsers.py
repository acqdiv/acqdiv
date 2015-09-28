""" Parsers for CHAT XML and Toolbox files for acqdiv corpora, and an acqdiv config file parser.
"""

import os
import sys
import configparser
import glob
import re
import xml.etree.ElementTree as ET
import json
from pprint import pprint

from metadata import Imdi, Chat
from factories import *
import cree


# TODO: integrate the Corpus specific parsing routines from the body parser
# TODO: integrate the metadata parsing
from toolbox import ToolboxFile


class CorpusConfigParser(configparser.ConfigParser):
    """ Config parser for corpus .ini files """

    def optionxform(self, optionstr):
        return optionstr


    # TODO: identify whether we want (extended) interolation, ordered dicts, inline commenting, etc.
    #    _dict_type = collections.OrderedDict
    #    _inline_comment_prefixes = ('#',)
    #    _interpolation = configparser.ExtendedInterpolation()

    #    def __init__(self, defaults=None):
    #        super(Config, self).__init__(defaults, dict_type=self._dict_type,
    #            inline_comment_prefixes=self._inline_comment_prefixes,
    #            interpolation=self._interpolation)

    def __init__(self):
        super().__init__()

    # file level initializations
    def read(self, filenames, encoding=None):
        super().read(filenames, encoding)

        # Load up the list of relative paths to corpus sessions files.
        # This creates a dependency that processors.py must be in same location as parsers.py!
        self.path = self['paths']['sessions']
        self.session_files = glob.glob(self.path)
        self.metadata_dir = self['paths']['metadata_dir']
        self.sessions_dir = self['paths']['sessions_dir']

        # Load up a dictionary of 'peculiarities'; these map the 'local'
        # symbols used in the corpus to the 'standard' symbols.
        # TODO: fix the inline commenting "#"
        # TODO: peculiarities moved to [record_tiers]
        # self.peculiarities = dict(self.items('peculiarities'))
        self.format = self['corpus']['format']
        self.corpus = self['corpus']['corpus']

        # ...And now any other additional things you want to do on
        # configfile load time.

class SessionParser(object):
    """ Static class-level method to create a new parser instance based on session format type.
    """

    @staticmethod
    def create_parser(config, file_path):
        corpus = config.corpus
        format = config.format

        # TODO: update when we dump using JSON
        if format == "ChatXML":
            if corpus == "Cree":
                return CreeParser(config, file_path)
            else:
                return ChatXMLParser(config, file_path)
        elif format == "Toolbox":
            return ToolboxParser(config, file_path)
        elif format == "JSON":
            return JsonParser(config, file_path)
        else:
            assert 0, "Unknown format type: " + format

    def __init__(self, config, file_path):
        self.config = config
        self.file_path = file_path
        # SessionParser.create_parser(self.config, self.file_path)

    # TODO: get SHA1 fingerprint of file -- provides unique data ID for db
    def sha1(self):
        pass

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

    # Generator to yield Utterances for the Utterance table in the db
    # def next_record(self):
    #    pass

class ToolboxParser(SessionParser):
    """ For Chintang, Indonesian, Russian, & potentially Dene  """

    def __init__(self, config, file_path):
        SessionParser.__init__(self, config, file_path)

        # Session body for utterances, etc.
        self.session_file = ToolboxFile(self.config, self.file_path)

        # Metadata
        if self.config['metadata']['type'] == "XML":
            # hack to get the separate metadata file paths for IMDIs
            temp = self.file_path.replace(self.config.sessions_dir, self.config.metadata_dir)
            self.metadata_file_path = temp.replace(".txt", ".xml")
            self.metadata_parser = Chat(self.config, self.metadata_file_path)

        elif self.config['metadata']['type'] == "IMDI":
            temp = self.file_path.replace(self.config.sessions_dir, self.config.metadata_dir)
            self.metadata_file_path = temp.replace(".txt", ".imdi")
            self.metadata_parser = Imdi(self.config, self.metadata_file_path)
        else:
            assert 0, "Unknown metadata format type: "#  + format


        # check for missing metadata files?
        """
        if not os.path.isfile(self.metadata_file_path):
            print("MISSING FILE:", self.metadata_file_path)
            sys.exit(1)
        """
        # self.metadata_parser = Imdi(self.metadata_file_path)

    def get_session_metadata(self):
        # Do toolbox-specific parsing of session metadata.
        # Presumably we will have to look for the metadata file in the config.
        # The config so it knows what symbols to look for.

        # this is an ugly hack due to the Indonesian corpus (body=Toolbox, but meta=XML)
        if self.metadata_parser.__class__.__name__ == "Imdi":
            return self.metadata_parser.metadata['session']
        elif self.metadata_parser.__class__.__name__ == "Chat":
            return self.metadata_parser.metadata['session']
        else:
            assert 0, "Unknown metadata format type: "#  + format

    def next_speaker(self):
        """ Yield participants metadata for the Speaker table in the db
        :return dictionary
        """
        for speaker in self.metadata_parser.metadata['participants']:
            yield speaker

    def next_utterance(self):
        """ Yield session level utterance data:
        returns ordered dictionary of config file record_tiers
        """
        for record in self.session_file:
#            print()
#            print("record:", record)
#            print()
            yield record


class ChatXMLParser(SessionParser):
    """ For Cree, Inuktitut, MiiPro, Miyata, Sesotho, Turkish, & Yucatec """

    def __init__(self, config, file_path):
        SessionParser.__init__(self, config, file_path)
        self.metadata_parser = Chat(config, self.file_path)
        #TODO: can this be a self.body_parser() or something?
        with open(self.file_path, 'r') as xml:
            self.tree = ET.parse(xml)
        self.root = self.tree.getroot()
        # this creates a dictionary of child:parent pairs
        # I don't know what it's good for yet but I'm putting it in here until
        # we can figure out what rsk uses it for in his parser
        # and whether we need it.
        #self.pmap = {c:p for p in self.tree.iter() for c in p}
        self.clean_tree()

    def get_session_metadata(self):
        # Do xml-specific parsing of session metadata.
        # The config so it knows what symbols to look for.
        return self.metadata_parser.metadata['session']

    # Generator to yield Speakers for the Speaker table in the db
    def next_speaker(self):
        for speaker in self.metadata_parser.metadata['participants']:
            yield speaker

    def clean_tree(self):
        """ Removes prefixed namespaces """
        for elem in self.root.iter():
            elem.tag = re.sub('^\{http[^\}]+\}', '', elem.tag)
        #    tag = elem.tag
        #    attrib = elem.attrib
        #    #God knows what those are good for. Debugging?

    def next_utterance(self):
        # Do xml-specific parsing of utterances.
        # The config so it knows what symbols to look for.
        uf = XmlUtteranceFactory()

        for u in self.root.findall('.//u'):
            yield uf.make_utterance(u), uf.next_word, uf.next_morpheme
    
class CreeParser(ChatXMLParser):
    """ Cazim's attempt at a Cree corpus specific subclass parser
    """
    def next_utterance(self):
        uf = cree.CreeUtteranceFactory()
        for u in self.root.findall('.//u'):
            yield uf.make_utterance(u), uf.next_word, uf.next_morpheme


class JsonParser(SessionParser):
    """ Parser for JSON output from:
    https://github.com/uzling/acqdiv/tree/master/extraction/parsing

    # TODO:
        - what to do with the stars?
            - "phonetic": "* * *",
            - "phonetic_target": "* * *",

    """
    def __init__(self, config, file_path):
        SessionParser.__init__(self, config, file_path)

        # load the data
        self.filename = os.path.splitext(os.path.basename(self.file_path))[0]
        with open(file_path) as data_file:
            self.data = json.load(data_file)
        # TODO: update when no longer using JSON
        temp = self.file_path.replace(self.config.sessions_dir, self.config.metadata_dir)
        self.metadata_file_path = temp.replace(".json", ".xml")
        self.metadata_parser = Chat(self.config, self.metadata_file_path)

    def next_utterance(self):
        """ Get each utterance from Robert's JSON output
        :return: utterance{}, words[word{}, word{}]
        """
        # Robert's JSON output is a dictionary: {key ("filename"): [u1{...}, u2{...}]}
        #  here we iterate over the utterances (each record)
        # Warning: the dictionary's key IS NOT ALWAYS the same as the file name...
        #  so we get the *key* (one json file per session; one key based on ID *or* filename)
        #  and use that
        x = self.data.keys() # in Py3 returns a dict_keys object, not a list!
        keys = list(x)
        assert(len(keys) == 1), "there is more than one key in the json file"
        key = keys[0] # should only be one top-level key per json file

        for record in self.data[key]:
            utterance = collections.OrderedDict()
            words = []
            morphemes = []

            # iterate over the utterance keys in the json parsed object and grab what is specified in the .ini
            for k in record:
                if k in self.config['json_mappings']:
                    label = self.config['json_mappings'][k]
                    utterance[label] = record[k]

                # TODO: Robert doesn't output the whole utterance, recreate it by gathering up the words
                full_utterance = []

                # Robert's {words:[]} is a list of dictionaries with keys like "full_word_target"
                d = collections.OrderedDict()
                if k == 'words':
                    for word in record['words']:
                        # this assigns the "proper" word target (corpus-specific) to the db, e.g. word <- full_word_target
                        # and recreates the "full word" utterance
                        word_target_label = self.config['json_mappings']['word']
                        if word_target_label in word:
                            # this is a hack to skip empty dictionaries in Robert's parser's json output
                            if not type(word[word_target_label]) is dict:
                                d[self.config['json_mappings']['full_word']] = word[word_target_label]
                                full_utterance.append(word[word_target_label])

                        if 'warnings' in word:
                            d[self.config['json_mappings']['warnings']] = word['warnings']

                        if 'utterance_id' in utterance:
                            d['utterance_id_fk'] = utterance['utterance_id']
                        words.append(d)

                        # morphemes{} parsing within word[] and extraction of .ini specified db columns
                        # morphemes are also a key:[] pair in words{}; morphemes: [segment:'ga', pos_target:'Eng']...
                        if 'morphemes' in word:
                            d2 = collections.OrderedDict()
                            if len(word['morphemes']) > 0: # skip empty lists in the json
                                for e in word['morphemes']: # iter over morpheme dicts
                                    for k_json_mappings_morphemes in self.config['json_mappings_morphemes']:
                                        if k_json_mappings_morphemes in e:
                                            d2[self.config['json_mappings_morphemes'][k_json_mappings_morphemes]] = \
                                            e[k_json_mappings_morphemes]

                                            # print(e[k_json_mappings_morphemes])
                                    if len(d2) > 0:
                                        morphemes.append(d2)
                # Recreate the full utterance string
                utterance['utterance_cleaned'] = " ".join(full_utterance)
            yield utterance, words, morphemes

    # TODO: this will have to be removed (copied from ChatXML for the time being)
    def get_session_metadata(self):
        # Do xml-specific parsing of session metadata.
        # The config so it knows what symbols to look for.
        return self.metadata_parser.metadata['__attrs__']

    def next_speaker(self):
        """ Yield participants metadata for the Speaker table in the db
        :return dictionary
        """
        for speaker in self.metadata_parser.metadata['participants']:
            yield speaker


if __name__ == "__main__":
    import time
    start_time = time.time()

    from parsers import CorpusConfigParser
    cfg = CorpusConfigParser()
    cfg.read("CreeJSON.ini")
    f = "../../corpora/Cree/json/Ani/2006-10-18.json"  ## ATTN: the folder structure on the server looks different now: corpora/Cree/json/.json
    c = JsonParser(cfg, f)
    #c.next_utterance() # why doesn't this work?
    #because it's a generator and you really should be doing 
    next(c.next_utterance())
    #the original call creates a generator object, but doesn't do anything with it!

    print()
    print("--- %s seconds ---" % (time.time() - start_time))
