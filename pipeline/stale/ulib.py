"""
File to hold corpus-specific parsing functions/classes callable via each corpus' config.
"""

__author__ = 'chysi'

#####################
# Utterance parsing #
#####################

class TbxParser():
    pass

class XmlParser():
    def __init__(self, u):
        self.raw = u
        
    def clean(self):


class ChintangParser(TbxParser):
    pass

class CreeParser(XmlParser):
    pass
