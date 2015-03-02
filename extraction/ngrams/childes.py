#!/usr/bin/python

"""
Module to do some basic cleaning and parsing of CHILDES files

Requires that all .cha files (for a particular language) are 
concatenated together into one file.

@date: 2010-12-01
@author: Steven Moran
"""

import sys
import collections
import operator
import unicodedata
import regex as re

def parse_words(file):
    # parse words
    words = collections.defaultdict(int)
    for line in file:
        line = line.strip()
        if line.startswith("@") or line == "":
            continue
        if not line.startswith("*"):
            continue

        tokens = line.split()
        for token in tokens:
            words[token] += 1
    words_sorted = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
    for word in words_sorted:
        word, count = word[0], word[1]
        print(word+"\t"+str(count))
    print(len(words))

def get_hapax_legomenon(file):
    """
    Get the hapax legomenon
    """
    words = collections.defaultdict(int)
    for line in file:
        line = line.strip()
        if line.startswith("@") or line == "":
            continue
        if not line.startswith("*"):
            continue

        tokens = line.split()
        for token in tokens:
            words[token] += 1

    count = 0
    for k, v in words.items():
        if v == 1:
            count += 1
            print(k+"\t"+str(v))
    print("total hapax legomenon:", str(count))


def clean_german_corpus(file):
    """
    Clean the concatenated German .cha files from CHILDES website (Leo files).
    """
    words = collections.defaultdict(int)
    parens_forms = collections.defaultdict(int)
    brackets_forms = collections.defaultdict(int)


    word_match = re.compile("\w+")
    parens_match = re.compile("\(.+?\)")
    brackets_match = re.compile("(\[.+?\])")
    recording_count_match = re.compile("\d+_\d+")

    learner_word_pattern = re.compile("\s\w+@\w+\s")
    learner_pattern = re.compile("@\w+\s")

    for line in file:
        result = ""
        line = line.strip()
        if not line.startswith("*"):
            print(line)
            continue

        # skip any utterances that contain "xxx"; keep lines but write %% before them
        if line.__contains__("xxx"):
            print("%%%", line)
            continue

        # get just the utternace part of the line
        split_line = line.partition(":")
        result += split_line[0]+split_line[1]+"\t"
        utterance = split_line[2].strip()


        # remove the learner crap (see page 21 in MacWhinney book)
        if utterance.__contains__("@"):
            utterance = re.sub(learner_pattern, " ", utterance)

        word_matches = word_match.findall(utterance)
        word_split = word_match.split(utterance)

        # get "words" before cleaning
        tokens = line.split()
        for token in tokens:
            words[token] += 1
        
        # find all matches in parentheses
        parens = parens_match.findall(utterance)
        if parens:
            for match in parens:
                parens_forms[parens[0]] += 1

        # find all matches in brackets
        brackets = brackets_match.findall(utterance)
        if parens:
            for match in brackets:
                brackets_forms[brackets[0]] += 1

        # remove recording numberings (for German)
        utterance = re.sub(recording_count_match, "", utterance)

        # remove brackets and stuff in brackets
        utterance = re.sub(brackets_match, "", utterance)

        # remove parentheticals
        utterance = utterance.replace("(.)", "")
        utterance = utterance.replace("(..)", "")
        utterance = utterance.replace("(...)", "")
        utterance = utterance.replace("(", "")
        utterance = utterance.replace(")", "")

        # remove all non-word stuff
        utterance = re.findall("\w+", utterance)
        
        # deal with the "0" marker
        if len(utterance) == 1 and utterance[0] == "0":
            result = "%%% "+result
        elif utterance[0] == "0":
            utterance = utterance[1:]

        result += " ".join(utterance).lower()
        print(result)

    # print_sorted_hash(parens_forms)
    # print_sorted_hash(brackets_forms)

def clean_english_corpus(file):
    """
    Clean the concatenated English .cha files (Manchester corpus) from CHILDES website (Leo files).
    """

    # keep track of the words and forms in parens and brackets for debugging
    words = collections.defaultdict(int)
    parens_forms = collections.defaultdict(int)
    brackets_forms = collections.defaultdict(int)

    word_match = re.compile("\w+")
    parens_match = re.compile("\(.+?\)")
    brackets_match = re.compile("(\[.+?\])")
    recording_count_match = re.compile("\d+_\d+")

    for line in file:
        result = ""
        line = line.strip()
        if not line.startswith("*"):
            print(line)
            continue

        # skip any utterances that contain "xxx"; keep lines but write %% before them
        if line.__contains__("xxx"):
            print("%%%", line)
            continue

        # get just the utternace part of the line
        split_line = line.partition(":")
        result += split_line[0]+split_line[1]+"\t"
        utterance = split_line[2].strip()

        word_matches = word_match.findall(utterance)
        word_split = word_match.split(utterance)

        # get "words" before cleaning
        tokens = line.split()
        for token in tokens:
            words[token] += 1

        # find all matches in parentheses
        parens = parens_match.findall(utterance)
        if parens:
            for match in parens:
                parens_forms[parens[0]] += 1

        # find all matches in brackets
        brackets = brackets_match.findall(utterance)
        if parens:
            for match in brackets:
                brackets_forms[brackets[0]] += 1

        # remove recording numberings (for German)
        utterance = re.sub(recording_count_match, "", utterance)

        # remove brackets and stuff in brackets
        utterance = re.sub(brackets_match, "", utterance)

        # remove parentheticals
        utterance = utterance.replace("(.)", "")
        utterance = utterance.replace("(..)", "")
        utterance = utterance.replace("(...)", "")
        utterance = utterance.replace("(", "")
        utterance = utterance.replace(")", "")

        # remove all non-word stuff - adapted for English apostrophe
        utterance = re.findall("[\'\w\-]+", utterance)
        result += " ".join(utterance).lower()

        print(result)

    # print_sorted_hash(parens_forms)
    # print_sorted_hash(brackets_forms)

def clean_russian_corpus(file):
    """
    Clean the concatenated Russian .cha files (from Sabine Stoll, not CHILDES website).

    Note: JAS is not a child within the age range, therefore I replace "*JAS" with "%JAS".

    """
    children = {"*ALJ":1, "*ALA":1, "*ANJ":1, "*PAS":1, "*VAN":1}
    line_number = 0

    words = collections.defaultdict(int)
    parens_forms = collections.defaultdict(int)
    brackets_forms = collections.defaultdict(int)

    word_match = re.compile("\w+")
    parens_match = re.compile("\(.+?\)")
    brackets_match = re.compile("(\[.+?\])")
    recording_count_match = re.compile("\d+_\d+")

    for line in file:
        result = ""
        line = line.strip()

        # print the other lines that aren't cleaned below
        if not line.startswith("*"):
            print(line)
            continue

        # skip any utterances that contain "xxx"; keep lines but write %% before them
        if line.__contains__("xxx"):
            print("%%%", line)
            continue

        # some lines in the Russian corpus contain extra info about the recording in .mpg files, e.g.:
        # *ALJ: vse . %mov:"A003_10903.mpg"_74760000_74763000
        # take only the left part of the line
        if line.startswith("*") and line.__contains__("%mov:"):
            line_recording_info = line.partition("%mov:")
            line = line_recording_info[0]

        # get just the utternace part of the line
        split_line = line.partition(":")
        utterance = split_line[2].strip()

        # for Russian .cha files flip children 3 letter IDs to CHI
        # instead of the myriad of names listed above
        # for 2-2.6 ages, flip *JAS to %JAS because his speech shouldn't be included (he's 3+ years)
        if split_line[0] in children:
            result += "*CHI"+split_line[1]+"\t"
        elif split_line[0] == "*JAS":
            result += "%JAS"+split_line[1]+"\t"
        else:
            result += split_line[0]+split_line[1]+"\t"

        word_matches = word_match.findall(utterance)
        word_split = word_match.split(utterance)

        # get "words" before cleaning
        tokens = line.split()
        for token in tokens:
            words[token] += 1
        
        # find all matches in parentheses
        parens = parens_match.findall(utterance)
        if parens:
            for match in parens:
                parens_forms[parens[0]] += 1
                # print(utterance)
                # print(parens)
                # print(parens[0])

        # find all matches in brackets
        brackets = brackets_match.findall(utterance)
        if parens:
            for match in brackets:
                brackets_forms[brackets[0]] += 1

        # remove recording numberings (for German)
        utterance = re.sub(recording_count_match, "", utterance)

        # remove brackets and stuff in brackets
        utterance = re.sub(brackets_match, "", utterance)

        # remove parentheticals
        utterance = utterance.replace("(.)", "")
        utterance = utterance.replace("(..)", "")
        utterance = utterance.replace("(...)", "")
        utterance = utterance.replace("(", "")
        utterance = utterance.replace(")", "")

        # remove all non-word stuff
        utterance = re.findall("\w+", utterance)
        result += " ".join(utterance).lower()
        
        print(result)

    # print_sorted_hash(parens_forms)
    # print_sorted_hash(brackets_forms)

def print_sorted_hash(hash):
    """
    Convenience function to sort a hash into a list and print it
    """
    sorted_hash = sorted(hash.items(), key=operator.itemgetter(1), reverse=True)
    for tuple in sorted_hash:
        key, value = tuple[0], tuple[1]
        print(key+"\t"+str(value))
    print("total"+"\t"+str(len(hash)))


def parse_character_counts(file):
    """
    Parse character counts into a unigram model
    """
    chars = collections.defaultdict(int)
    for line in file:
        line = line.strip()
        if not line.startswith("*"):
            continue
        # if line.startswith("@") or line == "":
        #    continue

        for char in line:
            chars[char] += 1

    # sort the hash and print the list
    segments_sorted = sorted(chars.items(), key=operator.itemgetter(1), reverse=True)
    print("character"+"\t"+"count"+"\t"+"decimal"+"\t"+"char name")
    for segment in segments_sorted:
        segment, count = segment[0], segment[1]
        print(segment+"\t"+str(count)+"\t"+str(ord(segment)))# +unicodedata.name(segment))
    print("total distinct characters:", len(chars))


def parse_participants(file):
    """
    Parse out the participants from the header data in .cha file.
    """
    participants = collections.defaultdict(int)
    utterances = 0
    for line in file:
        line = line.strip()

        # skip non-header lines in the file
        if not line.startswith("*"):
            continue
        utterances += 1

        tokens = line.partition(":")
        participant_code = tokens[0].replace("*", "")
        participants[participant_code] += 1

    # sort the hash into a list and then print it
    participants_sorted = sorted(participants.items(), key=operator.itemgetter(1), reverse=True)    
    for participant in participants_sorted:
        participant, count = participant[0], participant[1]
        print(participant+"\t"+str(count))
    print("total utterances:"+"\t"+str(utterances))


def parse_headers(file):
    """
    Parse header information from .cha file.
    """
    num_files = 0
    result = ["count", "filename"]

    for line in file:
        line = line.strip()

        # identify the filebane
        if line.startswith("@Filename"):
            tokens = line.split()
            result[1] = tokens[1]
            # print("filename:", tokens)

        # identify the participants
        if line.startswith("@Participants"):
            if line.__contains__("Target Child"):
                line = line.replace("Target Child", "Target_Child")
            comma_split = line.split(",")
            for token in comma_split:
                print(token, end="")
            print()
            # print("participants:", line.split(","))

            participants = line.split()

            # add to result list
            for token in particiPants:
                result.append(token)

        # identify the ID
        # if line.startswith("@ID:"):
            # print("id:", line)

        # .cha files can have different ways of denoting the end of file
        if line.__contains__("@END") or line.__contains__("@End"):
            num_files += 1
            result[0] = str(num_files)
            # print(result)

            """
            for token in result:
                print(token, "\t", end="")
            print()
            result = ["count", "filename"]
            """

def get_word_count_by_participant(file, participant):
    """
    pass this method a cleaned corpus
    """
    words = collections.defaultdict(int)
    grams = 0
    for line in file:
        line = line.strip()
        if line.startswith("@") or line == "":
            continue
        if not line.startswith("*"):
            continue

        if line.startswith(participant):
            tokens = line.split()
            for token in tokens:
                words[token] += 1
                grams += 1

    words_sorted = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
    for word in words_sorted:
        word, count = word[0], word[1]
        print(word+"\t"+str(count))
    print("unique words:", len(words))    
    print("total words: ", str(grams))

def get_single_word_utterances(file, participant):
    """
    pass this method a cleaned corpus
    """
    words = collections.defaultdict(int)
    grams = 0
    for line in file:
        line = line.strip()
        if line.startswith("@") or line == "":
            continue
        if not line.startswith("*"):
            continue

        if line.startswith(participant):
            tokens = line.partition(":")
            if len(tokens[2].split()) == 1:
                # print(tokens[2])
                grams += 1

    print("total words: ", str(grams))



if __name__=="__main__":
    file = open(sys.argv[1], "r") # pass it a .cha file
    # parse_character_counts(file)
    parse_words(file)
    # get_hapax_legomenon(file)
    # parse_participants(file)
    # clean_english_corpus(file)
    # clean_german_corpus(file)
    # clean_russian_corpus(file)
    # get_word_count_by_participant(file, "*MOT")
    # get_single_word_utterances(file, "*CHI")
