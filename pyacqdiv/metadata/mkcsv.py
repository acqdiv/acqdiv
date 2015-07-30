#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv
import unittest

class JsonReader():

    def __init__(self, path):
        self.path = path
        with open(path) as fp:
            self.data = json.load(fp)
        self.fname = self.get_file_id()
        self.participant_rows = self.get_participant_rows()
        self.session_row = self.get_session_row()

    def get_file_id(self):
        return self.data['__attrs__']['Cname']

    def get_participant_rows(self):
        rows = []
        session = self.data['session']['id']
        lang = self.data['session']['language']
        for participant in self.data['participants']:
             rows.append( 
                     [lang, session, participant['code'], participant['name'], 
                     participant['age.days'], participant['age'], 
                     participant['birthdate'], participant['sex'], 
                     participant['role']])
        return rows

    def get_session_row(self):
        sid = self.data['session']['id']
        lang = self.data['session']['language']
        date = self.data['session']['date']
        try:
            continent = self.data['session']['location']['continent']
        except:
            continent = None
        try:
            country = self.data['session']['location']['country']
        except:
            country = None
        genre = self.data['session']['genre']
        sit = self.data['session']['situation']
        row = [lang,sid,date,genre,sit,continent,country]
        return row

class CSVDumper():

    def __init__(self, inpath, sessionfile, partfile):
        self.data = JsonReader(inpath)
        self.sessionfile = sessionfile
        self.partfile = partfile

    def dump(self):
        with open(self.sessionfile, 'a', newline='') as fp:
            writer = csv.writer(fp, dialect='unix')
            writer.writerow(self.data.session_row)
        with open(self.partfile, 'a', newline='') as fp:
            writer = csv.writer(fp, dialect='unix')
            writer.writerows(self.data.participant_rows)

class TestCSV(unittest.TestCase):

    def setUp(self):
        reader = JsonReader('cleanmeta/cree_ani/2005-09-14.json')

if __name__ == "__main__":
    dumper = CSVDumper('cleanmeta/cree_ani/2005-09-14.json', 'cree_sessions.csv', 'ani_2005-09-14.csv')
    dumper.dump()

