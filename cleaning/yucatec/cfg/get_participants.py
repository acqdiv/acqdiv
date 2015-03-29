#!/usr/bin/env python3

'''
Script that creates participants.csv file by using the filename as ID and the columns code, name and role from the ids.tsv file.

Usage: python3 get_participants.py <filename>.tsv

Author: Danica Pajovic <danica.pajovic@uzh.ch>
'''

import sys, codecs, re
from collections import defaultdict, OrderedDict




def participants_csv(infile):
    
    infile = codecs.open(infile, 'r', 'utf-8')
    outfile = codecs.open('participants.csv', 'w', 'utf-8')
    participants_hash = defaultdict(list)   ## hash where @Participants for every file will be sotred
    counter = 1
    
    ## get info that is needed from ids.tsv file (i.e. columns file ID, code, name, role)
    for line in infile:
        counter +=1 
        line = line.rstrip()
        line_list = line.split('\t')
        
        ## skip lines with incomplete information
        if len(line_list) < 11:
            print('\nAttention: line ',counter, ' from the input file has only ', len(line_list), 'arguments. It doesn not contain all information. Skipping it.')
            ## e.g. line 438 in acqdiv/cleaning/yucated/cfg/ids.tsv has only 9 arguments
        else:
            iD = line_list[0]
            code = line_list[3]
            name = line_list[11]
            role = line_list[8]
            
            ## participants_hash is {"fileiD":"code name role, (...)"}
            participants_hash[iD].append((code, name, role))   
    
    outfile.write('"filename","@Participants:"\n')

    participants = OrderedDict(sorted(participants_hash.items()))
    for k, v in participants.items():
        k = '"'+str(k).replace(' ', '')+'"'
        v1 = '"'+str(v)+'"'
        v2 = re.sub("[\[\]()]|',|'", "", v1)
        outfile.write(str(k+','+v2+'\n'))
    
    print('\nThe participants info for every file has been written to "participants.csv"\n')

    infile.close()
    outfile.close()
    
    
if __name__ == "__main__":
    try:
        participants_csv(sys.argv[1])
    except IndexError:
        print('\nIndexError: Please indicate the name of the ids file as command line argument.\nE.g. $ python3 get_participants.py ids.tsv\n')
          
    
