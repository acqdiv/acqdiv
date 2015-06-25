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
        self.csv_fieldnames = self.get_csv_fields()
        self.participant_rows = self.get_participant_rows()
        self.session_row = self.get_session_row()

    def get_file_id(self):
        return self.data['__attrs__']['Cname']

    def get_csv_fields(self):
        pass

    def get_participant_rows(self):
        rows = []
        session = self.data['session']['id']
        for participant in self.data['participants']:
             rows.append( 
                     [session, participant['code'], participant['name'], 
                     participant['age.days'], participant['age'], 
                     participant['birthdate'], participant['sex'], 
                     participant['role']])
        return rows

    def get_session_row(self):
        sid = self.data['session']['id']
        lang = self.data['__attrs__']['Lang']
        date = self.data['session']['date']
        location = self.data['session']['location']['country']
        media = self.data['media']['mediafile']['file']
        mediaformat = self.data['media']['mediafile']['format']
        row = [sid,lang,date,location,media,mediaformat]
        return row


class CSVDumper():

    def __init__(self, inpath, sessionfile, partfile):
        self.data = JsonReader(inpath)
        self.sessionfile = sessionfile
        self.partfile = partfile

    def dump(self):
        with open(self.sessionfile, 'a') as fp:
            writer = csv.writer(fp)
            writer.writerow(self.data.session_row)
        with open(self.partfile, 'a') as fp:
            writer = csv.writer(fp)
            writer.writerows(self.data.participant_rows)

class TestCSV(unittest.TestCase):

    def setUp(self):
        reader = JsonReader('cleanmeta/cree_ani/2005-09-14.json')

if __name__ == "__main__":
    dumper = CSVDumper('cleanmeta/cree_ani/2005-09-14.json', 'cree_sessions.csv', 'ani_2005-09-14.csv')
    dumper.dump()

