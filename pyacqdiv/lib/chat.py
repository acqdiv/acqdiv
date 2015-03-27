"""
Functionality to support creation of acqdiv-style CHAT files.
"""
from string import Template


CHAT_TEMPLATE = Template("""\
@UTF8
@Begin
@Languages: $languages
@Participants:  $participants
$ids
@Media: $filename, audio
$lines
@End
""")


def chat(language, participants, ids, filename, lines):
    return CHAT_TEMPLATE.substitute(
        languages=language,
        participants=participants,
        ids='\n'.join(ids),
        filename=filename,
        lines='\n'.join(map(normalize, lines)))


def normalize(text):
    """ remove weird/control characters from a unicode line """
    return text.translate({_ord: None for _ord in [1, 2, 6, 7, 8, 26, 96, 130]})
