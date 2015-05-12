#!usr/bin/python
# -*- coding: utf-8 -*-
# Created by Cazim Hysi @ UZH
# cazim.hysi@gmail.com

import json
import sys
import unittest

class Unifier():

    SessionHeads = {'code':None,
                           'date':None,
                           'genre':None,
                           'location':None,
                           'situation':None}

    ProjectHeads = {'name': None, 
                           'shortname': None,
                           'contact': None, 
                           'id': None}

    MediaHeads = {'file': None,
                          'format': None,
                          'size': None,
                          'length': None}

    ParticipantHeads = {'code': None,
                                'name': None,
                                'birthdate': None,
                                'age': None,
                                'role': None,
                                'sex': None}

    def __init__(self, path):
        self.path = path
        with open(path) as jsf:
            self.metadata = json.load(jsf)
        if 'IMDI' in  self.metadata['__attrs__']['schemaLocation']:
            self.metatype = 'IMDI'
        else:
            self.metatype = 'XML'

    def unify(self, cdc=None):
        DEBUG = 0
        if self.metatype == 'IMDI':
            self.unifyImdi()
        else:
            self.unifyXml(cdc)
        if DEBUG == 0:
            with open(self.path, 'w') as unifile:
                json.dump(self.metadata, unifile)

    def unifyImdi(self):

        ProjectHeads = Unifier.ProjectHeads
        SessionHeads = Unifier.SessionHeads
        MediaHeads = Unifier.MediaHeads
        ParticipantHeads = Unifier.ParticipantHeads


        ImdiMediaHeads = {'resourcelink': 'file',
                          'format': 'format',
                          'size': 'size',
                          'timeposition': 'length'}


#First Pass: detect all elements we want to remove
#It is sadly not possible to do remove and correct in a single iteration

        metadata = {}

        metadata['project'] = ProjectHeads
        metadata['session'] = SessionHeads
        metadata['media'] = {}
        metadata['media']['mediafile'] = MediaHeads

        metadata['participants'] = []
        for head in self.metadata['project']:
            if head in ProjectHeads:
                metadata['project'][ProjectHeads[head]] = self.metadata['project'][head]

        for head in self.metadata['session']:
            if head in SessionHeads:
                metadata['session'][SessionHeads[head]] = self.metadata['session'][head]
                
        #The IMDI mediafile headers get special treatment because they actually need reassignment

        for resource in self.metadata['media']:
            if resource == 'mediafile':
                for head in self.metadata['media'][resource]:
                    if head in ImdiMediaHeads:
                        metadata['media'][resource][ImdiMediaHeads[head]] = self.metadata['media'][resource][head]

        for i in range(len(self.metadata['participants'])):
            metadata['participants'].append(ParticipantHeads)
            for head in self.metadata['participants'][i]:
                if head == 'code':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] != 'Unspecified':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]        
                if head == 'familysocialrole':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] != 'Unspecified':
                        metadata['participants'][i]['role'] = self.metadata['participants'][i][head]        
                if head == 'role':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] != 'Unspecified':
                            metadata['participants'][i][head] = self.metadata['participants'][i][head]
                elif head == 'name':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] != 'Unspecified':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]
                elif head == 'id':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] != 'Unspecified':
                        metadata['participants'][i]['code'] = self.metadata['participants'][i][head]
                elif head == 'sex':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] != 'Unspecified':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]
                elif head == 'birthdate':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] != 'Unspecified':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]

        self.metadata = metadata

    def unifyXml(self, cdc=None):

        ProjectHeads = Unifier.ProjectHeads
        SessionHeads = Unifier.SessionHeads
        MediaHeads = Unifier.MediaHeads
        ParticipantHeads = Unifier.ParticipantHeads

        metadata = {}

        metadata['project'] = ProjectHeads
        metadata['session'] = SessionHeads
        metadata['media'] = {}
        metadata['media']['mediafile'] = MediaHeads
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
                metadata['participants'].append(ParticipantHeads)
                for head in self.metadata['participants'][i]:
                    if head == 'role':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]        
                    elif head == 'name':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]
                    elif head == 'code':
                        metadata['participants'][i]['code'] = self.metadata['participants'][i][head]
                    elif head == 'sex':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]
                    elif head == 'birthdate':
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]

        if cdc:
            metadata['session']['genre'] = cdc.metadata['IMDI_Genre'] if 'IMDI_Genre' in cdc.metadata else None
            metadata['session']['location'] = {}
            metadata['session']['location']['continent'] = cdc.metadata['IMDI_Continent'] if 'IMDI_Continent' in cdc.metadata else None
            metadata['session']['location']['country'] = cdc.metadata['IMDI_Country'] if 'IMDI_Country' in cdc.metadata else None
            metadata['project']['name'] = cdc.metadata['Title'] if 'Title' in cdc.metadata else None
            metadata['project']['contact'] = cdc.metadata['Creator'] if 'Creator' in cdc.metadata else None

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
