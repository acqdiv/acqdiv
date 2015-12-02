"""Class to handle unique ids of ACQDIV corpora's unique speakers
"""
import database_backend as backend
from sqlalchemy.orm import sessionmaker
import operator,re
from configparser import ConfigParser

def unique_id(engine,configs):
	Session = sessionmaker(bind=engine)
	session = Session()
	"""
		Creates unique IDs for the unique speakers in current corpus (config) puts it into 
		an .ini file. IDs are fix and should only be changed manually.

		Args:
        	engine: SQLalchemy engine object.
        	configs: a list a corpus config files
	"""
	corpora = [c[:-4] for c in configs]
	corpus_dict = {}
	for c in corpora:
		speakers = {}
		counter = 1
		if c == 'Turkish':
			c = 'Turkish_KULLD'
		for row in session.query(backend.Unique_Speaker).filter(backend.Unique_Speaker.corpus == c):
			#every speaker of current corpus c gets an unique ID
			if not 'Japanese' in c:
				id = row.corpus[:3].upper() + (5-len(str(counter)))*'0' + str(counter)
			elif c == 'Japanese_MiiPro':
				id = 'JMI' + (5-len(str(counter)))*'0' + str(counter)
			else:
				id = 'JMY' + (5-len(str(counter)))*'0' + str(counter)
			speakers[(row.name, row.speaker_label,row.birthdate)] = id
			counter += 1
		corpus_dict[c] = speakers #add dictionary of speakers of corpus c to dict of all ids




"""
	ini = open('unique_ids.ini','w')
	for curr_corpus in sorted(corpus_dict):
		ini.write('['+curr_corpus+']\n')
		speakers = corpus_dict[curr_corpus]
		for k,v in sorted(speakers.items(),key=operator.itemgetter(1)) :
			key = ''
			for i in k:
				if i == None:
					i = 'None'
				key += i+' '
			key = key.replace(' ','_')
			entry = key[:-1] + '= ' + v
			ini.write(entry+'\n')
		ini.write('\n')
	ini.close()
"""
def speakers_key(speakerlist):
	"""helper function to create new entry in ini file of unique ids
	"""
	key = ''
	for i in speakerlist:
		if i == None:
			i = 'None'
		key += i+'_'
	key = key[:-1]

	return key


def new_id(speaker):
	"""
		adds a new unique id for new unique speaker speaker

		Args:
			speaker: a row of an SQLalchemy table
	"""
	cfg_mapping = ConfigParser()
	cfg_mapping.optionxform = str
	cfg_mapping.read("unique_ids.ini")
	new_num = len(cfg_mapping[speaker.corpus])+1
	id = speaker.corpus[:3].upper() + (5-len(str(new_num)))*'0' + str(new_num)
	key = ''
	temp = [speaker.name, speaker.speaker_label, speaker.birthdate]
	for i in temp:
		if i == None:
			i = 'None'
		key += i+' '
	key = key.replace(' ','_')
	cfg_mapping[speaker.corpus][key] = id

	with open('unique_ids.ini') as configfile:
		cfg_mapping.write(configfile)

def new_entry(speaker):
	print('here')
	cfg_mapping = ConfigParser()
	cfg_mapping.optionxform = str
	cfg_mapping.read("unique_ids.ini")
	corpus = speaker[0]
	try:
		counter = len(cfg_mapping[corpus])+1
	except KeyError:
		counter = 1
	if 'jap' not in corpus.lower():
		id = corpus[:3].upper() + (5-len(str(counter)))*'0' + str(counter)
	elif corpus == 'Japanese_MiiPro':
		id = 'JMI' + (5-len(str(counter)))*'0' + str(counter)
	else:
		id = 'JMY' + (5-len(str(counter)))*'0' + str(counter)
	key = speakers_key(speaker[1:])
	try:
		cfg_mapping[corpus][key] = id
	except KeyError:
		cfg_mapping[corpus] = {}
		cfg_mapping[corpus][key] = id
	
	with open('unique_ids.ini','w') as configfile:
		cfg_mapping.write(configfile)


def unique_speaker():
	return

