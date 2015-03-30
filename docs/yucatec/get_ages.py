
''' Script to calcualte the age of the participants from a csv-file, prints output to another csv-file.

    Usage: $python3 get_ages.py <inputfile.csv>
    
    Author: Danica Pajovic <danica.pajovic@uzh.ch>
'''

import sys, codecs, re, csv
from collections import defaultdict, OrderedDict
from datetime import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta


## open csv file and loop through every line; check if either "birthday" or "recording.date" information is available.
## if "birthday" and "recording.date" info is available, add calcualte age and insert it to the "age" column.

##TODO: Print error warnings to log-file, not terminal!

def calculate_age(infile):
    counter = 1
    all_lines = []
    column_names1 = []
    column_names2 = []
    outfile = codecs.open('metdat_rec_age.csv', 'w', 'utf-8')
    
    for line in csv.reader(infile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
        all_lines.append(line)
    
    ## get column names from header line.
    for first_line in all_lines[:1]:
        column_names1.append(first_line)
    
    for col_name in column_names1:
        for elem in col_name:
            column_names2.append(elem)
    
    ## loop through all the rows of the infput file    
    for line in all_lines:
        counter += 1
        for i in range(0,len(line)):
            if column_names2[i] == "birthdate":
                #print('hello')
               birthday = str(line[i]).replace('JAN', '01').replace('FEB', '02').replace('MAR', '03').replace('APR', '04').replace('MAY','05').replace('JUN','06').replace('JUL','07').replace('AUG','08').replace('SEP','09').replace('OCT','10').replace('NOV','11').replace('DEC','12').replace('"','')
            elif column_names2[i] == 'recording.date':
                rec_date = str(line[i]).replace('JAN', '01').replace('FEB', '02').replace('MAR', '03').replace('APR', '04').replace('MAY','05').replace('JUN','06').replace('JUL','07').replace('AUG','08').replace('SEP','09').replace('OCT','10').replace('NOV','11').replace('DEC','12').replace('"','')        
            
        ## calculate ages and print to chat format        
        def childes_age_format(d1, d2):
            d1 = datetime.strptime(d1, "%Y-%m-%d")
            d2 = datetime.strptime(d2, "%Y-%m-%d")
            #return abs((d2 - d1).days)
            diff = relativedelta(d2, d1)
            return("%d;%d.%d" % (diff.years, diff.months, diff.days))
        
        ## insert calcualted age to "age" column.
        for i in range(0,len(line)):
            if column_names2[i] == "age":
                try:
                    age_at_rec_date = childes_age_format(birthday,rec_date)
                    line[int(i)] = age_at_rec_date
                except ValueError:
                    print('Warning: line ', counter, ' does not contain enougth speaker information to calculate the age.')
                    continue
        
        writer = csv.writer(outfile, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        writer.writerow(line)
    
    #infile.close()
    #outfile.close()

    
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        infile = codecs.open(sys.argv[1], 'r', 'utf-8')
        #outfile = codecs.open(sys.argv[2], 'w', 'utf-8')
    else:
        print('\nPlease indicate the infile as command line arguments.\n')
    calculate_age(infile)
    

