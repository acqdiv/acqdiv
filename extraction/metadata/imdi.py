"""
$ python metadata.py pax45.xml
$ cat pax45.xml.json | python -mjson.tool

{
    "__attrs__": {
        "Corpus": "Paxton", 
        "Date": "1993-12-11", 
        "Id": "pax45", 
        "Lang": "eng", 
        "Media": "pax45", 
        "Mediatypes": "audio", 
        "PID": "11312/c-00012562-1", 
        "Version": "2.0.2", 
        "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": "http://www.talkbank.org/ns/talkbank http://talkbank.org/software/talkbank.xsd"
    }, 
    "comments": {
        "Date": "11-DEC-1993"
    }, 
    "participants": [
        {
            "age": "P1Y8M22D", 
            "birthday": "1992-03-19", 
            "id": "CHI", 
            "language": "eng", 
            "name": "Paxton", 
            "role": "Target_Child", 
            "sex": "male"
        }
    ], 
    "utterances": [
        {
            "end": 390.0, 
            "id": "u0", 
            "start": 387.268, 
            "who": "CHI"
        }, 
...
    ]
}
"""
import sys
import json

from lxml import objectify


def parse_attrs(e):
    return {k: e.attrib[k] for k in e.keys()}


def parse_utterance(u):
    res = {
        'id': u.attrib['uID'],
        'who': u.attrib['who'],
    }
    if hasattr(u, 'media'):
        res['start'] = float(u.media.attrib['start'])
        res['end'] = float(u.media.attrib['end'])
    return res

def parse_words(u):
    # TODO: parse words
    # if hasattr(u, 'w'):
    # ...
    pass


def parse_metadata(path):
    tree = objectify.parse(path)
    root = tree.getroot()
    for e in root.Session.MDGroup.Actors.Actor.getchildren(): 
        print e.tag
        for tag in e:
            print tag.text


    sys.exit(1)
    chat = {
        # '__attrs__': parse_attrs(root),
        'session': [parse_attrs(p) for p in root.Session.Description]#.MDGroup.Actors.Actor],
        #'comments': {c.attrib['type']: unicode(c) for c in root.comment},
        #'utterances': [parse_utterance(u) for u in root.u],
    }
    print chat

    with open(path + '.json', 'w') as fp:
        json.dump(chat, fp)


if __name__ == '__main__':
    parse_metadata(sys.argv[1])

# python imdi.py russian/imdi/Vanja/imdis_Sept2010/V01110710.imdi

# TODO:
# Russian: generate the age from the session; add sex to imdi files


