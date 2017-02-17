"""
Module provides a class for reading and writing toolbox files. Data is read
and written utterance-by-utterance.
"""
import os
import re
import sys
import logging
from collections import OrderedDict


class CorpusProcesser():
    """Reads and writes toolbox files."""

    def __init__(self, org_cp_path, new_cp_path, logger=True, mkdir=True):
        """Initialize paths for corpus files.

        org_cp_path (str): path to corpus file for reading
        new_cp_path (str): path to corpus file for writing
        logger (bool): logger is used or not
        mkdir (bool): directory for new files is created or not
        """
        # set paths
        self.org_cp_path = org_cp_path
        self.new_cp_path = new_cp_path

        # decide if a logger should be used
        if logger:
            self.get_logger()
        else:
            self.get_logger(activate=False)

        # decide if a directory should be created
        if mkdir:
            self.create_dir()

        # save data of one utterance using a sorted dict because order is
        # important; key is the fieldmarker, value the whole line (including
        # field marker label); tiers \glo, \seg, \id, \vt and \vtg are
        # additionally saved in a special data structure called "words"
        self.ref_dict = OrderedDict()
        # keep track of errors in the utterance
        self.has_errors = False

    def __iter__(self):
        """Iterate all utterances of all corpus files."""
        # Go through each corpus file
        for _ in self.iter_files():

            # go through each utterance in the file
            for utterance in self.iter_utterances():

                # check utterance
                self.check()

                yield utterance

            self.org_file.close()
            self.new_file.close()

    def get_logger(self, activate=True):
        """Get a logger.

        activate (bool): activates the logger
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        if activate:
            handler = logging.FileHandler("cp.log", mode="w")
            handler.setLevel(logging.WARNING)

            formatter = logging.Formatter(
                "%(funcName)s|%(levelname)s|%(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        else:
            self.logger.propagate = False

    def create_dir(self):
        """Create directory for the new corpus files."""
        if not os.path.isdir(self.new_cp_path):
            try:
                os.mkdir(self.new_cp_path)
            except FileNotFoundError:
                print("Path '{}' for corpus directory does not exist".format(
                      self.new_cp_path))
                print()
                sys.exit(1)

    def iter_files(self):
        """Iterate and yield all corpus files for reading and writing."""
        # go through each original corpus file
        for file in os.listdir(self.org_cp_path):

            # if it is a toolbox file
            if file.endswith(".tbt"):

                # get path of this original file
                org_file_path = os.path.join(self.org_cp_path, file)

                # set file for reading
                self.org_file = open(org_file_path, "r")

                # get path for new corpus file
                new_file_path = os.path.join(self.new_cp_path, file)

                # set file for writing
                self.new_file = open(new_file_path, "w")

                yield (self.org_file, self.new_file)

    def iter_utterances(self):
        """Iterate and yield all utterances.

        org_file (file): file that is read for iterating over the utterances
        """
        org_file = self.org_file

        # delete data of previous utterance (just as a precaution)
        self.ref_dict.clear()

        # go through all data from a corpus file
        # and save data per utterance unter ref_dict
        for line in org_file:

            # throw away the newline at the end of a line
            line = line.rstrip("\n")

            # if new utterance starts
            if line.startswith("\\ref"):
                # yield data of previous utterance
                yield self.ref_dict
                # delete data of previous utterance
                self.ref_dict.clear()
                # add \ref to hash
                self.ref_dict["\\ref"] = line

            # if fieldmarker \full of utterance starts
            elif line.startswith("\\full"):

                has_label = self.add_tier(line)[2]

                # if 'words' is not yet in ref_dict
                if not has_label:
                    # save morpheme data in a special data structure
                    # words: [(word1, {"\\seg": [seg1, seg2]
                    #                  "\\glo": [glo1, glo2],
                    #                  "\\id": [id1, id2]}), (word2, {...})]
                    self.ref_dict["words"] = []

                # extract words splitting the processed line at whitespaces
                word_iterator = re.finditer(r"\S+", line)
                # skip the field marker label
                next(word_iterator)

                # add every word to the hash
                for word in word_iterator:
                    self.ref_dict["words"].append((word.group(), {}))

            # if any field marker starts
            elif line.startswith("\\"):

                label, data, has_label = self.add_tier(line)

                # deal with morpheme tiers separately
                if label in {"\\seg", "\\glo", "\\id", "\\vt", "\\vtg"}:

                    # get regex & iterator for extracting units per word
                    regex = re.compile(r"((\S+-\s+)*\S+(\s+-\S+)*)")
                    unitgroup_iterator = regex.finditer(line)

                    # get field marker label which is the first unit
                    label = next(unitgroup_iterator).group()

                    # find out no. of unit groups so far inserted for this tier
                    n_unitgroups = 0
                    if has_label:
                        for word, morphemes in self.ref_dict["words"]:
                            if label in morphemes:
                                n_unitgroups += 1

                    # go over those units per word
                    for i, unitgroup in enumerate(unitgroup_iterator,
                                                  start=n_unitgroups):

                        n_unitgroups += 1

                        # extract units of a unitgroup splitting at whitespaces
                        units = re.split("\s+", unitgroup.group())

                        try:
                            # add units to the right word (via index)
                            # to morpheme dictionary (at index 1)
                            # under the right label (\seg,\glo,\id,\vt,\vtg)
                            self.ref_dict["words"][i][1][label] = units

                        # if there are less words than unit groups
                        except IndexError:
                            # add it under an empty word
                            self.ref_dict["words"].append(("", {label: units}))

            # if line does not start with \\, its data must belong
            # to the fieldmarker that directly comes before
            elif line:
                # get last added fieldmarker
                label = next(reversed(self.ref_dict))
                # concatenate content
                self.ref_dict[label] += line

        # last utterance
        yield self.ref_dict

    def add_tier(self, line):
        """Extract label and data and add to ref_dict.

        line (str): tier
        """
        # extract field marker label and its data
        match = re.match(r"(\\\w+)(.*)", line)

        label = match.group(1)
        data = match.group(2)

        # field marker in ref_dict
        has_label = False

        # check if there are several defintions of the
        # same fieldmarker in one \ref
        if label in self.ref_dict:
            has_label = True
            # concatenate with hash content
            self.ref_dict[label] += data
        else:
            # add to hash
            self.ref_dict[label] = line

        return (label, data, has_label)

    def check(self):
        """Do various checks for the words and their morphemes."""
        self.has_errors = False

        # Check if there are words in the utterance at all
        if "words" not in self.ref_dict:
            self.has_errors = True
            return

        # for logging purposes
        ref = self.ref_dict["\\ref"]

        # do checks for word and morpheme numbers
        for words, morphemes in self.ref_dict["words"]:

            # if number of words and morpheme groups do not match
            if words == "" or len(morphemes) != 5:
                self.logger.error("word numbers don't match in {}".format(ref))
                self.has_errors = True
                return

            # if number of morphemes is not equal for all morpheme tiers
            # take number of \seg's as a random reference point
            n_units = len(morphemes["\\seg"])
            for tier in morphemes:
                if len(morphemes[tier]) != n_units:
                    self.logger.error(
                        "morpheme numbers don't match in {}".format(ref))
                    self.has_errors = True
                    return

    def write_file(self):
        """Write data of an utterance to the file.

        new_file (file): corpus file for writing
        """
        new_file = self.new_file

        # Go through every tier in an utterance
        for tier in self.ref_dict:

            # content of the tier
            content = self.ref_dict[tier]

            # if tier is a morpheme tier
            if tier in {"\\full", "\\seg", "\\glo", "\\id", "\\vt", "\\vtg"}:

                # and the morphemes tiers are unequal in number
                if self.has_errors:
                    # write its content directly to file
                    new_file.write(content)
                    # new line after every tier
                    new_file.write("\n")

            # if 'words' create its morpheme tiers first before writing
            elif tier == "words":

                # morpheme data is written unchanged (see above)
                if self.has_errors:
                    continue

                # build tiers here
                tiers = OrderedDict([("\\full", "\\full "),
                                     ("\\seg", "\\seg "),
                                     ("\\glo", "\\glo "),
                                     ("\\id", "\\id "),
                                     ("\\vt", "\\vt "),
                                     ("\\vtg", "\\vtg ")])

                # go through each word
                for word, morphemes in content:

                    # concatenate word to tier \full
                    tiers["\\full"] += word

                    # keep track of the longest unit group
                    longest_group = 0
                    # go through each slot in the word (e.g. via \seg)
                    for i, _ in enumerate(morphemes["\\seg"]):

                        # save the no. of chars for every unit in this slot
                        lens = {}

                        # keep track of the longest type of unit
                        longest_unit = 0
                        # go through every type of unit
                        for unit in morphemes:

                            # concatenate unit i to tier of this unit type
                            tiers[unit] += morphemes[unit][i]

                            # save no. of chars of this unit
                            lens[unit] = len(morphemes[unit][i])

                            # compare it to the longest unit seen so far
                            if longest_unit < lens[unit]:
                                longest_unit = lens[unit]

                        # there is one whitespace between morphemes/words
                        longest_unit += 1

                        # add it to the unit group length
                        longest_group += longest_unit

                        # add necessary whitespaces between morphemes
                        for unit in morphemes:
                            tiers[unit] += (longest_unit - lens[unit])*" "

                    # add necessary whitespaces between words
                    tiers["\\full"] += (longest_group - len(word))*" "

                for tier in tiers:
                    # write morpheme tier stripping trailing whitespaces
                    new_file.write(tiers[tier].rstrip())
                    # new line after every tier
                    new_file.write("\n")

            # any other tier
            else:
                # write its content directly to the file
                new_file.write(content)
                # new line after every tier
                new_file.write("\n")

        # insert empty line between utterances
        new_file.write("\n")
