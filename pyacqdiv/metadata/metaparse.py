import metadata as md
from cdc import CdcParser
from unifier import Unifier
from configparser import ConfigParser
from pyacqdiv.util import existing_dir
import os

class MetaExtractor():
    
    def __init__(self, meta_dir, cfg):
        self.path = meta_dir
        self.cfg = cfg
        if self.cfg['cdc'] == 'yes':
            self.cdc = CdcParser(self.cfg['cdc_path'])
        else:
            self.cdc = None
        self.extract()
        self.unify()

    def extract(self):
        od = self.cfg['out_dir']
        assert existing_dir(od)

        if self.cfg['metatype'] == 'IMDI':
            for filename in os.listdir(self.cfg['meta_dir']):
                if not filename.startswith('.') or os.path.isdir(filename):
                    of = os.path.join(od, filename.split(".")[0])
                    with open(os.path.join(self.cfg['meta_dir'], filename), 'r') as fp:
                        try:
                            md.Imdi(fp, of)
                        except Exception as e:
                            print("Skipped file " + filename + ":")
                            print("Error: {0}".format(e))

        else:
            for filename in os.listdir(self.cfg['meta_dir']):
                if not filename.startswith('.') or os.path.isdir(filename):
                    of = os.path.join(od, filename.split(".")[0])
                    with open(os.path.join(self.cfg['meta_dir'], filename), 'r') as fp:
                        try:
                            md.Chat(fp, of)
                        except Exception as e:
                            print("Skipped file " + filename + ":")
                            print("Error: {0}".format(e))

    def unify(self):
        for filename in os.listdir(self.cfg['out_dir']):
            if not filename.startswith('.') or os.path.isdir(filename):
                inf = os.path.join(self.cfg['out_dir'], filename)
                try:
                    jsu = Unifier(inf)
                    jsu.unify(self.cdc)
                except Exception as e:
                    print("Could not unify file " + filename + ":")
                    print("Error: {0}".format(e))

if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read('metadata.ini')
    for cid in cfg.sections():
        metadata = MetaExtractor(cid, dict(cfg.items(cid)))

