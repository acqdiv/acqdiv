import metadata as md
import mkcsv
from cdc import CdcParser
from unifier import Unifier
from configparser import ConfigParser
from pyacqdiv.util import existing_dir
import os

class MetaExtractor():
    
    def __init__(self, corpus, cfg, fpass):
        self.corpus = corpus
        self.cfg = cfg
        if self.cfg['cdc'] == 'yes':
            self.cdc = CdcParser(self.cfg['cdc_path'])
        else:
            self.cdc = None
        self.extract()
        self.unify()
        if fpass == 1:
            self.setupcsv()
        self.tocsv()

    def extract(self):
        od = self.cfg['json_dir']
        assert existing_dir(od)

        if self.cfg['metatype'] == 'IMDI':
            for filename in os.listdir(self.cfg['meta_dir']):
                if not filename.startswith('.') or os.path.isdir(filename):
                    of = os.path.join(od, filename.split(".")[0])
                    with open(os.path.join(self.cfg['meta_dir'], filename), 'r') as fp:
                        try:
                            md.Imdi(self.corpus, fp, of)
                        except Exception as e:
                            print("Skipped file " + filename + ":")
                            print("Error: {0}".format(e))

        else:
            for filename in os.listdir(self.cfg['meta_dir']):
                if not filename.startswith('.') or os.path.isdir(filename):
                    of = os.path.join(od, filename.split(".")[0])
                    with open(os.path.join(self.cfg['meta_dir'], filename), 'r') as fp:
                        try:
                            md.Chat(self.corpus, fp, of)
                        except Exception as e:
                            print("Skipped file " + filename + ":")
                            print("Error: {0}".format(e))

    def unify(self):
        for filename in os.listdir(self.cfg['json_dir']):
            if not filename.startswith('.') or os.path.isdir(filename):
                inf = os.path.join(self.cfg['json_dir'], filename)
                try:
                    jsu = Unifier(inf)
                    jsu.unify(self.cfg['lang'], self.cdc)
                except Exception as e:
                    print("Could not unify file " + filename + ":")
                    print("Error: {0}".format(e))

    def tocsv(self):
        assert existing_dir(self.cfg['csv_dir'])
        for filename in os.listdir(self.cfg['json_dir']):
            if not filename.startswith('.') or os.path.isdir(filename):
                inf = os.path.join(self.cfg['json_dir'], filename)
                sf = os.path.join(self.cfg['csv_dir'], 'sessions.csv')
                pf = os.path.join(self.cfg['csv_dir'], 'participants.csv')
                dumper = mkcsv.CSVDumper(inf,sf,pf)
                dumper.dump()

    def setupcsv(self):
        assert existing_dir(self.cfg['csv_dir'])
        sf = os.path.join(self.cfg['csv_dir'], 'sessions.csv')
        pf = os.path.join(self.cfg['csv_dir'], 'participants.csv')
        with open(sf, 'w') as sfp:
            sfp.write('"Language","SessionID","SessionDate","SessionGenre","SessionSituation","SessionContinent","SessionCountry"\n')
        with open(pf, 'w') as pfp:
            pfp.write('"Language","SessionID","SpeakerLabel","SpeakerName","SpeakerAgeDays","SpeakerAge","SpeakerBirthday","SpeakerGender","SpeakerRole"\n')

if __name__ == '__main__':
    first_pass = 1
    cfg = ConfigParser()
    cfg.read('metadata.ini')
    for cid in cfg.sections():
        metadata = MetaExtractor(cid, dict(cfg.items(cid)), first_pass)
        first_pass = 0

