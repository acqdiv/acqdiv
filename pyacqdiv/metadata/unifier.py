#!usr/bin/python
# -*- coding: utf-8 -*-
# Created by Cazim Hysi @ UZH
# cazim.hysi@gmail.com

import json
import sys
import unittest
import age

class Unifier():

    def __init__(self, path):

        self.path = path
        with open(path) as jsf:
            self.metadata = json.load(jsf)
        if 'IMDI' in self.metadata["__attrs__"]['schemaLocation']:
            self.metatype = 'IMDI'
        else:
            self.metatype = 'XML'
        self.null = ["Unknown", "Unspecified", "None"]

    def unify(self, lang, cdc=None):
        DEBUG = 0
        if self.metatype == 'IMDI':
            self.unifyImdi(lang)
        else:
            self.unifyXml(lang, cdc)
        if DEBUG == 0:
                with open(self.path, 'w') as unifile:
                    json.dump(self.metadata, unifile)

    def unifyImdi(self, lang):

        SessionHeads = {'id': None,
                               'date': None,
                               'genre': None,
                               'location': None,
                               'situation': None,
                               'language': lang}

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
                                    'age.days': None,
                                    'role': None,
                                    'sex': None}

        ImdiMediaHeads = {'resourcelink': 'file',
                          'format': 'format',
                          'size': 'size',
                          'timeposition': 'length'}


#First Pass: detect all elements we want to remove
#It is sadly not possible to do remove and correct in a single iteration

        metadata = {}

        metadata['__attrs__'] = self.metadata['__attrs__']

        metadata['project'] = ProjectHeads.copy()
        metadata['session'] = SessionHeads.copy()
        metadata['media'] = {}
        metadata['media']['mediafile'] = MediaHeads.copy()
        metadata['participants'] = []

        for head in self.metadata['project']:
            if head in ProjectHeads.copy():
                metadata['project'][head] = self.metadata['project'][head]

        for head in self.metadata['session']:
            if head in SessionHeads.copy():
                metadata['session'][head] = self.metadata['session'][head]

        #The IMDI mediafile headers get special treatment because they actually need reassignment

        for resource in self.metadata['media']:
            if resource == 'mediafile':
                for head in self.metadata['media'][resource]:
                    if head in ImdiMediaHeads:
                        metadata['media'][resource][ImdiMediaHeads[head]] = self.metadata['media'][resource][head]

        for i in range(len(self.metadata['participants'])):
            metadata['participants'].append(ParticipantHeads.copy())
            for head in self.metadata['participants'][i]:
                if head == 'code':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] not in self.null:
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]        
                if head == 'role':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] not in self.null:
                            metadata['participants'][i][head] = self.metadata['participants'][i][head]
                elif head == 'familysocialrole':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] not in self.null:
                        metadata['participants'][i]['role'] = self.metadata['participants'][i][head]        
                elif head == 'name':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] not in self.null:
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]
                elif head == 'id':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] not in self.null:
                        metadata['participants'][i]['code'] = self.metadata['participants'][i][head]
                elif head == 'sex':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] not in self.null:
                        metadata['participants'][i][head] = self.metadata['participants'][i][head].lower()
                elif head == 'birthdate':
                    if "\n" not in self.metadata['participants'][i][head] and self.metadata['participants'][i][head] not in self.null:
                        metadata['participants'][i][head] = self.metadata['participants'][i][head]

        for participant in metadata['participants']:
            if participant['birthdate']:
                try:
                    recdate = age.numerize_date(metadata['session']['date'])
                    bdate = age.numerize_date(participant['birthdate'])
                    agelist = age.format_imdi_age(bdate, recdate)
                    participant['age'] = agelist[0]
                    participant['age.days'] = agelist[1]
                except Exception as e:
                        print("Couldn't calculate age in " + self.path)
                        print("Error: {0}".format(e))

        self.metadata = metadata

    def unifyXml(self, lang, cdc=None):

        SessionHeads = {'id': None,
                               'date': None,
                               'genre': None,
                               'location': None,
                               'situation': None,
                               'language': lang}

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
                                    'age.days': None,
                                    'role': None,
                                    'sex': None}

        metadata = {}

        metadata['project'] = ProjectHeads.copy()
        metadata['session'] = SessionHeads.copy()
        metadata['media'] = {}
        metadata['media']['mediafile'] = MediaHeads.copy()
        metadata['participants'] = []

        for attr in self.metadata['__attrs__']:
            if attr == 'Cname':
                metadata['session']['id'] = self.metadata['__attrs__'][attr]
            elif attr == 'Date':
                metadata['session']['date'] = self.metadata['__attrs__'][attr]
            elif attr == 'Media':
                metadata['media']['mediafile']['file'] = self.metadata['__attrs__'][attr]
            elif attr == 'Mediatypes':
                metadata['media']['mediafile']['format'] = self.metadata['__attrs__'][attr]
            else:
                continue

        metadata['__attrs__'] = self.metadata['__attrs__']

        parts = len(self.metadata['participants'])

        for i in range(parts):
            metadata['participants'].append(ParticipantHeads.copy())
            for head in self.metadata['participants'][i]:
                if head == 'role':
                    metadata['participants'][i][head] = self.metadata['participants'][i][head]        
                elif head == 'name':
                    metadata['participants'][i][head] = self.metadata['participants'][i][head]
                elif head == 'age':
                    metadata['participants'][i][head] = self.metadata['participants'][i][head]
                elif head == 'id':
                    metadata['participants'][i]['code'] = self.metadata['participants'][i][head]
                elif head == 'sex':
                    metadata['participants'][i][head] = self.metadata['participants'][i][head].lower()
                elif head == 'birthdate':
                    metadata['participants'][i][head] = self.metadata['participants'][i][head]

        if cdc:
            metadata['session']['genre'] = cdc.metadata['IMDI_Genre'] if 'IMDI_Genre' in cdc.metadata else None
            metadata['session']['location'] = {}
            metadata['session']['location']['continent'] = cdc.metadata['IMDI_Continent'] if 'IMDI_Continent' in cdc.metadata else None
            metadata['session']['location']['country'] = cdc.metadata['IMDI_Country'] if 'IMDI_Country' in cdc.metadata else None
            metadata['project']['name'] = cdc.metadata['Title'] if 'Title' in cdc.metadata else None
            metadata['project']['contact'] = cdc.metadata['Creator'] if 'Creator' in cdc.metadata else None


        for participant in metadata['participants']:
            if participant['age']:
                try:
                    agestr = participant['age']
                    participant['age'] = age.format_xml_age(agestr)
                    participant['age.days'] = age.calculate_xml_days(participant['age'])
                except Exception as e:
                        print("Couldn't calculate age in " + self.path)
                        print("Error: {0}".format(e))
                        participant['age'] = None
                        participant['age.days'] = None

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

    jsu = Unifier("sesothotest.json")
    jsu.unify()
    with open("unify.json", "w") as unify:
        json.dump(jsu.metadata, unify)
