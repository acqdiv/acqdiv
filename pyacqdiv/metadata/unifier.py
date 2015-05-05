#!usr/bin/python
# -*- coding: utf-8 -*-
# Created by Cazim Hysi @ UZH
# cazim.hysi@gmail.com

import json
import sys
import unittest

class Unifier():

    def __init__(self, path):
        with open(path) as jsf:
            self.metadata = json.load(jsf)
        if 'IMDI' in  self.metadata['__attrs__']['schemaLocation']:
            self.metatype = 'IMDI'
        else:
            self.metatype = 'XML'

    def unify(self):
        if self.metatype == 'IMDI':
            self.unifyImdi()
        else:
            self.unifyXml()

    def unifyImdi(self):
        ImdiProjectHeads = {'name': 'name', 
                            'shortname': 'shortname',
                            'contact': 'contact', 
                            'id': 'id'}

        ImdiSessionHeads = {'code': 'code',
                            'date': 'date',
                            'genre': 'genre',
                            'location': 'location',
                            'situation': 'situation'}

        ImdiMediaHeads = {'resourcelink': 'file',
                          'format': 'format',
                          'size': 'size',
                          'timeposition': 'length'}

        ImdiParticipantHeads = {'code': 'code',
                                'name': 'name',
                                'birthdate': 'birthdate',
                                'age': 'age',
                                'sex': 'sex',
                                'role': 'familysocialrole'}

        UnwantedProjectHeads = set()
        UnwantedSessionHeads = set()
        UnwantedMediaHeads = set()
        UnwantedMediaTypes = set()
        UnwantedParticipantHeads = set()

#First Pass: detect all elements we want to remove
#It is sadly not possible to do remove and correct in a single iteration

        for head in self.metadata['project']:
            if head not in ImdiProjectHeads:
                UnwantedProjectHeads.add(head) 
            else:
                self.metadata['project'][ImdiProjectHeads[head]] = self.metadata['project'].pop(head)

        for head in self.metadata['session']:
            if head not in ImdiSessionHeads:
                UnwantedSessionHeads.add(head)
            else:
                self.metadata['session'][ImdiSessionHeads[head]] = self.metadata['session'].pop(head)
                
        for resource in self.metadata['media']:
            if resource == 'mediafile':
                for head in self.metadata['media'][resource]:
                    if head not in ImdiMediaHeads:
                        UnwantedMediaHeads.add(head)
                    else:
                        self.metadata['media'][resource][ImdiMediaHeads[head]] = self.metadata['media'][resource].pop(head)
            else:
                UnwantedMediaTypes.add(resource)

        for participant in self.metadata['participants']:
            for head in participant:
                if head not in ImdiParticipantHeads:
                    UnwantedParticipantHeads.add(head)
                else:
                    participant[ImdiParticipantHeads[head]] = participant.pop(head)


        for key in UnwantedProjectHeads:
            del self.metadata['project'][key]

        for key in UnwantedSessionHeads:
            del self.metadata['session'][key]

        for participant in self.metadata['participants']:
            for key in UnwantedParticipantHeads:
                del participant[key]

        for mtype in UnwantedMediaTypes:
            del self.metadata['media'][mtype]

        for resource in self.metadata['media']:
            for key in UnwantedMediaHeads:
                del self.metadata['media'][resource][key]

    def unifyXml(self):
       
        metadata = {}
        
        XmlSessionHeads = {'code':None,
                           'date':None,
                           'genre':None,
                           'location':None,
                           'situation':None}

        XmlProjectHeads = {'name': None, 
                           'shortname': None,
                           'contact': None, 
                           'id': None}

        XmlMediaHeads = {'file': None,
                          'format': None,
                          'size': None,
                          'length': None}

        XmlParticipantHeads = {'code': None,
                                'name': None,
                                'birthdate': None,
                                'age': None,
                                'role': None,
                                'sex': None}

        metadata['project'] = XmlProjectHeads
        metadata['session'] = XmlSessionHeads
        metadata['media'] = {}
        metadata['media']['mediafile'] = XmlMediaHeads
        metadata['participants'] = []

        for attr in self.metadata['__attrs__']:
            if attr == 'Cname':
                metadata['session']['code'] = self.metadata['__attrs__'][attr]
            elif attr == 'Date':
                metadata['session']['date'] = self.metadata['__attrs__'][attr]
            elif attr == 'Media':
                metadata['media']['mediafile']['file'] = self.metadata['__attrs__'][attr]
            elif attr == 'Mediatypes':
                metadata['media']['mediafile']['format'] = self.metadata['__attrs__'][attr]
            else:
                continue

        metadata['__attrs__'] = self.metadata['__attrs__']

        for i in range(len(self.metadata['participants'])):
                metadata['participants'].append(XmlParticipantHeads)
                for head in self.metadata['participants'][i]:
                    if head == 'role':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]        
                    elif head == 'name':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]
                    elif head == 'id':
                        metadata['participants'][i]['code'] = self.metadata['participants'][i][head]
                    elif head == 'sex':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]
                    elif head == 'birthdate':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]


        self.metadata = metadata

class testJson(unittest.TestCase):

    def setUp(self):
        self.jsu = Unifier("russiantest.json")
        self.jsc = Unifier("miiprotest.json")

    def testLoadsJson(self):
        self.assertIsNotNone(self.jsu.metadata)
        self.assertIsNotNone(self.jsc.metadata)

    def testTypesCorrectly(self):
        self.assertEqual(self.jsu.metatype, 'IMDI')
        self.assertEqual(self.jsc.metatype, 'XML')

    def testUnifiesWithoutError(self):
        self.jsu.unify()
        self.assertIsNotNone(self.jsu.metadata)

if __name__ == "__main__":
    jsu = Unifier("russiantest.json")
    jsu.unify()
    with open("unify.json", "w") as unify:
        json.dump(jsu.metadata, unify)

    jsc = Unifier("miiprotest.json")
    jsc.unify()
    with open("unify_xml.json", "w") as unify:
        json.dump(jsc.metadata, unify)
