# -*- coding: utf-8 -*-

import os
import sys

current_dir = os.getcwd()
sys.path.append(current_dir)

import database_backend as db
import processors as processors
import postprocessor as pp
import unittest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_
import parsers as parsers


# helper functions
def connect():
    """ Performs database connection. We can add a database settings
    from settings.py later. Returns sqlalchemy engine instance.
    """
    return db.create_engine('sqlite:///tests/test_tlbx_acqdiv.sqlite3', echo=False)

def make_session():
    engine = connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def load_database(configs, engine):
    db.create_tables(engine)

    for config in configs:
        # Parse the config file and call the sessions processor
        cfg = parsers.CorpusConfigParser()
        cfg.read(config)
        cfg.set('paths', 'sessions', cfg['tests']['sessions'])
        cfg.set('paths', 'sessions_dir', cfg['tests']['sessions_dir'])
        cfg.set('paths', 'metadata_dir', cfg['tests']['metadata_dir'])
        cfg.set('corpus', 'format', cfg['tests']['format'])
        #print(cfg['paths']['sessions'])
        

        # Process by parsing the files and adding extracted data to the db
        c = processors.CorpusProcessor(cfg, engine)
        c.process_corpus()
        
        print("Postprocessing database entries for {0}...".format(config.split(".")[0]))
        pp.update_age(cfg, engine)
        pp.unify_glosses(cfg, engine)

class ToolbxTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize database connection and drop and then create tables on each call.
        # http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate
        engine = connect()

        cls.configs = ['Chintang.ini', 'Russian.ini', 'Indonesian.ini']
        
        load_database(cls.configs, engine)
    

    def testTLBXSessions(self):
        """
        Test if sessions for Toolbox test files are loaded correctly
        """
        session = make_session()
        self.assertEqual(len(session.query(func.count(db.Session.corpus), db.Session.corpus).group_by(db.Session.corpus).all()), len(ToolbxTest.configs))
        s = select([db.Session.id, db.Session.session_id, db.Session.corpus, db.Session.language, db.Session.date, db.Session.source_id, db.Session.media, db.Session.media_type])
        result = session.execute(s)
        self.assertEqual(str(result.fetchall()), "[(1, 'Chintang', 'Chintang', 'Chintang', '2004', 'Chintang', None, None), (2, 'Russian', 'Russian', 'Russian', '1995-04-24', None, None, None), (3, 'Indonesian', 'Indonesian', 'Indonesian', '1999-05-20', '1999-05-20', None, None)]")
        session.close()
        
        
    def testTLBXUtterances(self):
        """
        Test if utterances for Toolbox test files are loaded correctly
        """
        session = make_session()
        self.assertEqual(session.query(db.Utterance).count(),  2246)
        s_chntng = select([db.Utterance], and_(db.Utterance.utterance_id=="CLDLCh1R01S01.002"))
        s_ru = select([db.Utterance], and_(db.Utterance.utterance_id=="A00210817_3"))
        s_indon = select([db.Utterance], and_(db.Utterance.utterance_id=="447883094927120405"))
        result_chntng = session.execute(s_chntng)
        result_ru = session.execute(s_ru)
        result_indon = session.execute(s_indon)
        
        self.assertEqual(str(result_chntng.fetchall()), "[(2, 'Chintang', 'Chintang', 'Chintang', 'CLDLCh1R01S01.002', 'MKR', None, 'theke hapamettukumcum hou', 'theke hapamettukumcum hou', 'None', 'question', None, None, '00:00:01.908', '00:00:03.348', 'theke hapamettukumcum hou', 'theke *** hou', 'why *** AFF', 'adv n gm', None, None)]")
        self.assertEqual(str(result_ru.fetchall()), "[(375, 'Russian', 'Russian', 'Russian', 'A00210817_3', 'LEN', None, 'Alja , ne trogaj kisu .', 'Alja  ne trogaj kisu ', None, 'default', None, None, None, None, None, 'alja , ne trogatq kisa .', None, 'NAME:M:SG:NOM:AN PUNCT PCL V-IMP:2:SG:IRREFL:IPFV NOUN:F:SG:ACC:INAN PUNCT ', None, None)]")
        self.assertEqual(str(result_indon.fetchall()), "[(1003, 'Indonesian', 'Indonesian', 'Indonesian', '447883094927120405', 'MOTHIZ', None, 'e, Ai mana Ai, Ai, eh?', 'e Ai mana Ai Ai eh', 'hey, where is Ai, Ai, hey?', 'question', None, None, '0:00:21', None, None, 'e Ai mana Ai Ai eh', 'EXCL Ai which Ai Ai huh', None, None, None)]")       
        session.close()
        
        
    def testTLBXWords(self):
        """
        Test if words for Toolbox test files are loaded correctly
        """
        session = make_session()
        self.assertEqual(session.query(db.Word).count(), 5223)
        s_chntng = select([db.Word], and_(db.Word.utterance_id_fk=="CLDLCh1R01S01.001"))
        s_ru = select([db.Word], and_(db.Word.utterance_id_fk=="A00210817_3"))
        s_indon = select([db.Word], and_(db.Word.utterance_id_fk=="447883094927120405"))
        result_chntng = session.execute(s_chntng)
        result_ru = session.execute(s_ru)
        result_indon = session.execute(s_indon)
        
        self.assertEqual(str(result_chntng.fetchall()), "[(1, 'Chintang', 'CLDLCh1R01S01.001', 'Chintang', 'Chintang', 'habinɨŋ', None, None, None), (2, 'Chintang', 'CLDLCh1R01S01.001', 'Chintang', 'Chintang', 'habinɨŋ', None, None, None)]")
        self.assertEqual(str(result_ru.fetchall()), "[(920, 'Russian', 'A00210817_3', 'Russian', 'Russian', 'Alja', None, None, None), (921, 'Russian', 'A00210817_3', 'Russian', 'Russian', 'ne', None, None, None), (922, 'Russian', 'A00210817_3', 'Russian', 'Russian', 'trogaj', None, None, None), (923, 'Russian', 'A00210817_3', 'Russian', 'Russian', 'kisu', None, None, None)]")
        self.assertEqual(str(result_indon.fetchall()), "[(1900, 'Indonesian', '447883094927120405', 'Indonesian', 'Indonesian', 'e', None, 'e', None), (1901, 'Indonesian', '447883094927120405', 'Indonesian', 'Indonesian', 'Ai', None, 'Ai', None), (1902, 'Indonesian', '447883094927120405', 'Indonesian', 'Indonesian', 'mana', None, 'mana', None), (1903, 'Indonesian', '447883094927120405', 'Indonesian', 'Indonesian', 'Ai', None, 'Ai', None), (1904, 'Indonesian', '447883094927120405', 'Indonesian', 'Indonesian', 'Ai', None, 'Ai', None), (1905, 'Indonesian', '447883094927120405', 'Indonesian', 'Indonesian', 'eh', None, 'eh', None)]")
        session.close()
        
        
    def testTLBXMorphemes(self):
        """
        Test if morphemes for Toolbox test files are loaded correctly
        """
        session = make_session()
        self.assertEqual(session.query(db.Morpheme).count(), 5830) 
        s_chntng = select([db.Morpheme.morpheme, db.Morpheme.gloss, db.Morpheme.pos_raw], and_(db.Morpheme.utterance_id_fk=="CLDLCh1R01S01.001")) #check morphemes for a particular utterance
        s_ru = select([db.Morpheme.morpheme, db.Morpheme.gloss, db.Morpheme.pos_raw], and_(db.Morpheme.utterance_id_fk=="A00210817_3"))
        s_indon = select([db.Morpheme.morpheme, db.Morpheme.gloss, db.Morpheme.pos_raw], and_(db.Morpheme.utterance_id_fk=="447883094927120405"))
        result_chntng = session.execute(s_chntng)
        result_ru = session.execute(s_ru)
        result_indon = session.execute(s_indon)
        
        self.assertEqual(str(result_chntng.fetchall()), "[('hap', 'cry', 'vi'), ('-i', '-1/2pS/P', '-gm'), ('-nɨŋ', '-NEG', '-gm'), ('hap', 'cry', 'vi'), ('-i', '-1/2pS/P', '-gm'), ('-nɨŋ', '-NEG', '-gm')]")
        self.assertEqual(str(result_ru.fetchall()), "[('alja', 'M.SG.NOM.AN', 'NAME'), ('ne', 'PCL', 'PCL'), ('trogatq', 'IMP.2SG.IRREFL.IPFV', 'V'), ('kisa', 'F.SG.ACC.INAN', 'NOUN')]")
        self.assertEqual(str(result_indon.fetchall()), "[('e', 'EXCLA', None), ('Ai', 'Ai', None), ('mana', 'which', None), ('Ai', 'Ai', None), ('Ai', 'Ai', None), ('eh', 'huh', None)]")
        session.close()
        
        

    def testTLBXSpeakers(self):
        """
        Test if  speakers for Toolbox test files are loaded
        """
        session = make_session()
        self.assertEqual(session.query(db.Speaker).count(),  34 )
        s_chntng = select([db.Speaker.speaker_label, db.Speaker.name, db.Speaker.age_raw, db.Speaker.age, db.Speaker.age_in_days, db.Speaker.gender_raw, db.Speaker.gender, db.Speaker.languages_spoken, db.Speaker.birthdate], and_(db.Speaker.corpus == "Chintang"))
        s_ru = select([db.Speaker.speaker_label, db.Speaker.name, db.Speaker.age_raw, db.Speaker.age, db.Speaker.age_in_days, db.Speaker.gender_raw, db.Speaker.gender, db.Speaker.languages_spoken, db.Speaker.birthdate], and_(db.Speaker.corpus == "Russian"))
        s_indon = select([db.Speaker.speaker_label, db.Speaker.name, db.Speaker.age_raw, db.Speaker.age, db.Speaker.age_in_days, db.Speaker.gender_raw, db.Speaker.gender, db.Speaker.languages_spoken, db.Speaker.birthdate], and_(db.Speaker.corpus == "Indonesian"))
        result_chntng = session.execute(s_chntng)
        result_ru = session.execute(s_ru)
        result_indon = session.execute(s_indon)
        #print(result_indon.fetchall())
        self.assertEqual(str(result_chntng.fetchall()), "[('AM', 'Asar Maya', '31', '31;0.0', 11315, 'Female', None, 'ctn x-sil-BAP nep', 'Unspecified'), ('CHR', 'Chandra', '18', '18;0.0', 6570, 'Female', None, 'ctn x-sil-BAP nep', 'Unspecified'), ('Dala', 'Dalahangma', '28', '28;0.0', 10220, 'Female', None, 'x-sil-BAP x-sil-NEP x-sil-CTN', 'Unspecified'), ('GKR', 'Ganga Kumari', '40', '40;0.0', 14600, 'Female', None, 'nep x-sil-BAP ctn', 'Unspecified'), ('ILU', 'Ilu', '12', '12;0.0', 4380, 'Female', None, 'nep x-sil-BAP ctn', 'Unspecified'), ('INDRA', 'Indra', '5', '5;0.0', 1825, 'Female', None, 'nep ctn', 'Unspecified'), ('BISR', 'Bishal', '3', '3;0.0', 1095, 'Male', None, 'ctn', 'Unspecified'), ('Khuma', 'Khuma', '10', '10;0.0', 3650, 'Female', None, 'nep x-sil-BAP ctn', 'Unspecified'), ('Kuluk', 'Bishal', '5', '5;0.0', 1825, 'Male', None, 'x-sil-NEP x-sil-CTN', 'Unspecified'), ('LDCh4', 'Man Kumar', '2/3', '2;0.0', 956, 'Male', None, 'nep ctn', '2001-05-20'), ('MKR', 'Man Kumari', '25', '25;0.0', 9125, 'Female', None, 'bap ctn', 'Unspecified'), ('NR', 'Nanda Kumar', '41', '41;0.0', 14965, 'Male', None, 'nep x-sil-BAP ctn', 'Unspecified'), ('PBR', 'Purna Bahadur', '63', '63;0.0', 22995, 'Male', None, 'x-sil-NEP x-sil-BAP x-sil-CTN', 'Unspecified'), ('PUP', 'Puspa', '18', '18;0.0', 6570, 'Female', None, 'x-sil-ENG nep ctn x-sil-BAP', 'Unspecified'), ('PURB', 'Purna', '50', '50;0.0', 18250, 'Male', None, 'x-sil-BAP ctn nep', 'Unspecified'), ('RM', 'Rikhi Maya', '25/26', '25;0.0', 9410, 'Female', None, 'x-sil-BAP nep x-sil-ENG ctn', '1978-03-28'), ('RPPR', 'Ram Prasad', '15', '15;0.0', 5475, 'Male', None, 'nep x-sil-BAP ctn', 'Unspecified'), ('Sapana', 'Sapana', '12', '12;0.0', 4380, 'Female', None, 'nep ctn', 'Unspecified'), ('Shova', 'Shova', '32', '32;0.0', 11680, 'Female', None, 'x-sil-BAP nep ctn', 'Unspecified')]")
        self.assertEqual(str(result_ru.fetchall()), "[('PAP', 'Gregori', 'Unknown', None, None, 'Unknown', None, None, 'Unspecified'), ('LEN', 'Lena', 'Unknown', None, None, 'Unknown', None, None, 'Unspecified'), ('SAB', 'Sabine', 'Unknown', None, None, 'Unknown', None, None, 'Unspecified'), ('ALJ', 'Alja', 'Unknown', '1;8.17', 625, 'Unknown', None, None, '1993-08-07'), ('Unspecified', 'Stoll', 'Unspecified', None, None, 'Unspecified', None, None, 'Unspecified'), ('Unspecified', 'None', 'Unspecified', None, None, 'Unspecified', None, None, 'Unspecified')]")
        self.assertEqual(str(result_indon.fetchall()), "[('CHI', 'Hizkia', 'P1Y8M12D', '1;8.12', 617, 'male', None, 'ind jav', '1997-09-06'), ('MOT', 'Conny', None, None, None, 'female', None, 'xmm ind', None), ('EXP', 'Bety', 'P24Y0M10D', '24;0.10', 8770, 'female', None, 'ind jav', None), ('RIT', 'Rita', None, None, None, 'female', None, 'ind jav', None), ('IPA', 'Ipah', None, None, None, 'female', None, 'jav ind', None), ('KAT', 'Kartini', None, None, None, 'female', None, 'und', None), ('RAS', 'Rasyid', 'P4Y9M15D', '4;9.15', 1745, None, None, 'und', '1994-08-04'), ('REG', 'Regi', 'P0Y11M3D', '0;11.3', 333, 'male', None, 'ind', '1998-06-16'), ('XXX', None, None, None, None, None, None, 'und', None)]")
        session.close()
        
        
    def textTLBXUniquespeakers(self):
        """
        Test if unique speakers for Toolbox test files are loaded
        """
        session = make_session()
        self.assertEqual(session.query(db.Uniquespeakers).count(),13)
        session.close()
    
    
    
    
    
    
    

if __name__ == "__main__":
    current_dir = os.getcwd()
    sys.path.append(current_dir)

    import database_backend as db
    import processors as processors
    import unittest
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import func
    import parsers as parsers
