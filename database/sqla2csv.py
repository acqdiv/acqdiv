""" writes csv files from the sqlite database tables

tables are the same names, e.g. sessions -> sessions.csv

csv files are comma delimited quote escaped

call: python3 sqla2csv.py databasename.sqlite3 
"""

import sqlite3
import csv
import sys
import os

def write_table(table_name):
    outfile = open('csv/'+table_name+'.csv', 'w')
    outcsv = csv.writer(outfile, quotechar='"', quoting=csv.QUOTE_NONNUMERIC,delimiter=',')
    cursor = con.execute('select * from '+table_name)
    # dump column titles (optional)
    outcsv.writerow(x[0] for x in cursor.description)
    # dump rows
    outcsv.writerows(cursor.fetchall())
    outfile.close()

if __name__=="__main__":
    os.makedirs('csv', exist_ok=True)
    con = sqlite3.connect(sys.argv[1])
    write_table("sessions")
    write_table("speakers")
    write_table("uniquespeakers")
    write_table("utterances")
    write_table("warnings")
    write_table("words")
    write_table("morphemes")    
