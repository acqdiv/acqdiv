"""
Script to get session level metadata from CHILDES XML files using NLTK.

Steven Moran <steven.moran@uzh.ch>
October 2014

$ python sessions.py path/to/corpora/

"""
import sys
import csv
import collections
import nltk
from nltk.corpus.reader import CHILDESCorpusReader
from xml.etree import ElementTree


def extract_session_metadata(corpus_root, language, extension):
    """
    Extract session level metadata and participant metadata
    """
    corpus = CHILDESCorpusReader(corpus_root, language+extension)
    
    # get the other nltk accessible data (return lists of various data types)
    corpora = corpus.fileids() # list of strings

    corpus_data = corpus.corpus(corpus.fileids()) # list of dicts
    ages = corpus.age() # list of strings
    months = corpus.age(month=True) # list of ints
    participants = corpus.participants() # list of key-defaultdicts values

    # combine the session-level extract-able xml
    for i in range(0, len(corpora)):
        print(corpus_data[i])
        corpus_data[i]["age"] = ages[i]
        corpus_data[i]["filename"] = corpora[i]
        corpus_data[i]["age_in_months"] = months[i]

    # write output to csv file
    # NOTE: this method ignores dict keys not present in all dicts
    with open("Sessions.csv", "w") as outfile:
        fp = csv.DictWriter(outfile, corpus_data[0].keys(), restval="", extrasaction="ignore")
        fp.writeheader()
        fp.writerows(corpus_data)


    # Print the participants data - brute force approach
    #  - loop all session files; get the metadata into a header and sort it
    #  - loop through the sessions 

    # participant data stored in list of defaultdicts
    header = collections.defaultdict(int)
    for i in range(0, len(participants)):
        for k, v in participants[i].iteritems():
            for k2, v2 in v.iteritems():
                header[k2] += 1

    # first we got to print the header's contents
    header_labels = []
    for k, v in sorted(header.iteritems()):
        header_labels.append(k+" ("+str(v)+")")
    header_labels.append("filename")
    header_labels.append("language")

    outputfile = open("Participants.csv", "w")
    outputfile.write(",".join(header_labels)+"\n")

    # print("\t".join(header_labels))
    for i in range(0, len(participants)):
        for k, v in participants[i].iteritems(): # v is defaultdict of {id:CHI, sex:MALE, ...}
            result = []
            for k2, v2 in sorted(header.iteritems()):
                if k2 in v:
                    result.append(v[k2])
                else:
                    result.append("")
            result.append(corpora[i]) # grab extra data
            result.append(language)
            outputfile.write(",".join(result)+"\n")
            # print("\t".join(result))


if __name__=="__main__":    
    # directory where language-specific folders are
    corpus_root = sys.argv[1] # e.g. ../../../Corpora/
    extension = ".*.xml"
    
    # process language by language or leave language blank to process all
    language = "Indonesian/"
    language = "Sesotho/"
    language = "Cree/"
    language = "Japanese/"
    language = ""

    extract_session_metadata(corpus_root, language, extension)
