"""Class to handle unique ids of ACQDIV corpora's unique speakers
"""
import database_backend as backend
from sqlalchemy.orm import sessionmaker
import operator,re
from configparser import ConfigParser

def speakers_key(speakerlist):
	"""
		Helper function to create new entry in ini file of unique ids. Calculates the key
		of a speaker entry in the unique_ids.ini file

		Args:
			speaker: a list with the necessary speaker information for unique identification
	"""
	key = ''
	for i in speakerlist:
		if i == None:
			i = 'None'
		key += i+','
	key = key[:-1]

	return key

def new_entry(speaker):
	"""
		Every new unique speaker gets a new entry with an unique id in the unique_ids.ini
		file

		Args:
			speaker: a list with the necessary speaker information for unique identification

	"""
	cfg_mapping = ConfigParser(delimiters=('='))
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
		
	while id in cfg_mapping[corpus].values():
		num = int(id[3:])+1
		id = id[:3]+ (5-len(str(num)))*'0' + str(num)

	key = speakers_key(speaker[1:])
	try:
		cfg_mapping[corpus][key] = id
	except KeyError:
		cfg_mapping[corpus] = {}
		cfg_mapping[corpus][key] = id
	
	with open('unique_ids.ini','w') as configfile:
		cfg_mapping.write(configfile)


