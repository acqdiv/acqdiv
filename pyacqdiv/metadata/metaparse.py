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
            self.cdc = CdcParser(open(self.cfg['cdc_path']))
        else:
            self.cdc = None
        self.extract()
        #self.unify()

    def extract(self):
        od = self.cfg['out_dir']
        assert existing_dir(od)

        if self.cfg['metatype'] == 'IMDI':
            for filename in os.listdir(self.cfg['meta_dir']):
                if not filename.startswith('.'):
                    of = os.path.join(od, ".".join([filename.split(".")[0], "json"]))
                    with open(os.path.join(self.cfg['meta_dir'], filename), 'r') as fp:
                        md.Imdi(fp, of)
        else:
            for filename in os.listdir(self.cfg['meta_dir']):
                if not filename.startswith('.'):
                    of = os.path.join(od, ".".join([filename.split(".")[0], "json"]))
                    with open(os.path.join(self.cfg['meta_dir'], filename), 'r') as fp:
                        md.Chat(fp, of)

    def unify(self):
        for filename in os.listdir(self.cfg['out_dir']):
            if not filename.startswith('.'):
                inf = os.path.join(self.cfg['out_dir'], filename)
                jsu = Unifier(inf)
                jsu.unify(self.cdc)

if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read('metadata.ini')
    for section in cfg:
        for cid in (cfg.sections()):
            metadata = MetaExtractor(cid, dict(cfg.items(cid)))

