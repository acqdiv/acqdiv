"""
Script to test the CHILDES Corpus Reader in the NLTK

Steven Moran <steven.moran@uzh.ch>
August 2014

"""
import sys
import nltk
from nltk.corpus.reader import CHILDESCorpusReader
    
def words_sents(corpus_root, folder_name):
    # count number of words and sentences in each file
    sesotho = CHILDESCorpusReader(corpus_root, folder_name+'.*.xml')
    words = 0
    sents = 0
    for this_file in sesotho.fileids(): # this_file in sesotho.fileids()[:1]:
        # print(sesotho.corpus(this_file)[0]['Corpus'], sesotho.corpus(this_file)[0]['Id'])
        # print("num of words: %i" % len(sesotho.words(this_file)))
        # print("num of sents: %i" % len(sesotho.sents(this_file)))
        words += len(sesotho.words(this_file))
        sents += len(sesotho.sents(this_file))
    print("total words: %i" % int(words))
    print("total sents: %i" % int(sents))
    print("total files: %i" % len(sesotho.fileids()))

def files(corpus_root, folder_name):
    # number of files
    print("Number of Sesotho sessions: " + str(len(sesotho.fileids())))
    # print("Filenames: " + ", ".join(sesotho.fileids()))
    print("")

if __name__=="__main__":
    # directory where language-specific folders are
    corpus_root = "../Corpora/"
    # folder_name = "Sesotho/"
    folder_name = "Indonesian/xml/"
    words_sents(corpus_root, folder_name)

    sys.exit(1)



    # get corpus data
    corpus_data = sesotho.corpus(sesotho.fileids())

    # print metadata (from first xml file in list)
    print("Metadata from first XML file in list:")
    for key in sorted(corpus_data[0].keys()):
        print(key, ": ", corpus_data[0][key])
    print("")

    # get participant data
    corpus_participants = sesotho.participants(sesotho.fileids())

    for this_corpus_participants in corpus_participants[:2]:
        for key in sorted(this_corpus_participants.keys()):
            dct = this_corpus_participants[key]
            print(key, ": ", [(k, dct[k]) for k in sorted(dct.keys())])
        print("")
    # todo: would be cool to dump this into a heat map of participant x participant with number of sents / words as intensity



    # print words, sentences, etc in an XML file
    print("Words in an XML file:")
    print(sesotho.words('Sesotho/hia.xml'))
    print("")

    print("Sentences in an XML file:")
    print(sesotho.sents('Sesotho/hia.xml'))
    print("")

    print("Words by partcipant (here CHI):")
    print(sesotho.words('Sesotho/hia.xml',speaker=['CHI']))
    print(len(sesotho.words('Sesotho/hia.xml',speaker=['CHI'])))
    print("")

    sys.exit(1)

    # if corpus is tagged
    print("Tagged words (if available):")
    print(sesotho.tagged_words('Sesotho/hia.xml')[:30])
    print("")

    print("Tagged sentences (if available):")
    print(sesotho.tagged_sents('Sesotho/hia.xml')[:10])
    print("")

    # note "stem", "replace", "relation" (and possibly other) paramenters: 

    # valian.words('Valian/01a.xml',stem=True)[:30]
    # valian.words('Valian/01a.xml')[:30]

    # valian.words('Valian/01a.xml',speaker='CHI')[247]
    # valian.words('Valian/01a.xml',speaker='CHI',replace=True)[247]
 
    # valian.words('Valian/01a.xml',relation=True)[:10]


    # age data
    print("sesotho.age():")
    print(sesotho.age())
    print("")

    # MLU (mean length utterance) -- doesn't seem to work
    print("MLU:")
    print(sesotho.MLU())
    print(sesotho.MLU('Sesotho/hia.xml'))
    print("")

