
'''
Script that creates participants.csv file by using the filename as ID and the columns code, name and role from the ids.tsv file.

Usage: python3 get_participants.py <filename>.tsv

Author: Danica Pajovic <danica.pajovic@uzh.ch>
'''

import codecs, re, csv
from collections import defaultdict, OrderedDict



def participants_csv(infile):
    
    infile = codecs.open(infile, 'r', 'utf-8')
    outfile = codecs.open('participants.csv', 'w', 'utf-8')
    participants_hash = defaultdict(list)   ## hash where @Participants for every file will be sotred
    all_lines = []
    column_names1 = []
    column_names2 = []
    
    ## read tsv file
    for line in csv.reader(infile, quotechar='"', delimiter='\t', quoting=csv.QUOTE_ALL, skipinitialspace=True):
        all_lines.append(line)
        

    ## get column names from header line.
    for first_line in all_lines[:1]:
        column_names1.append(first_line)
        
    for col_name in column_names1:
        for elem in col_name:
            column_names2.append(elem)
    
    ## get columns filename, code, name and role and save them to participants.csv
    for line in all_lines:
        for i in range(0,len(line)):
            if column_names2[i] == "filename":
                iD = line[int(i)]
            elif column_names2[i] == "code":
                code = line[int(i)]
            elif column_names2[i] == "name":
                participant_name = line[int(i)]
            elif column_names2[i] == "role":
                role = line[int(i)]
        
        participants_hash[iD].append((code,participant_name,role))
    
    outfile.write('"filename","@Participants:"\n')
    participants = OrderedDict(sorted(participants_hash.items()))
    for k,v in participants.items():
        #writer = csv.writer(outfile, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        #writer.writerow(participants_hash[k])
        k = '"'+str(k).replace(' ', '')+'"'
        v1 = '"'+str(v)+'"'
        v2 = re.sub("[\[\]()]|',|'", "", v1)
        v2 = re.sub('"([a-z])','\\1',v2)
        outfile.write(str(k+','+v2+'\n'))
        
    #infile.close()
    #outfile.close()
                
    
if __name__ == "__main__":
    import sys
    try:
        participants_csv(sys.argv[1])
    except IndexError:
        print('\nIndexError: Please indicate the name of the ids file as command line argument.\nE.g. $ python3 get_participants.py ids.tsv\n')