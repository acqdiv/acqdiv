"""
Functionality to support creation of acqdiv-style CHAT files.
"""
from string import Template


CHAT_TEMPLATE = Template("""\
@UTF8
@Begin
@Languages:\t$languages
@Participants:\t$participants
$ids
$sessions
$lines
@End
""")

def chat(language, participants, ids, filename, sessions, lines):
    return CHAT_TEMPLATE.substitute(
        languages=language,
        participants=', '.join(participants),
        ids='\n'.join(ids),
        filename=filename,
        sessions='\n'.join(sessions),
        lines='\n'.join(map(normalize, lines)))

def repair_lines(lines):
    for i, e in reversed(list(enumerate(lines))):
        if i > 0 and not e.startswith(("*", "%", "@")):
            lines[i-1] = lines[i-1].strip()
            lines[i-1] += " "+lines.pop(i).strip()
    return lines

def normalize(text):
    """ remove weird/control characters from a unicode line """
    return text.translate({_ord: None for _ord in [1, 2, 6, 7, 8, 26, 96, 130]})
