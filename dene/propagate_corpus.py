"""
@author: Anna Jancso
"""
import logging
import os
import re
import sys
from collections import OrderedDict


class CorpusPropagater:
    
    # paths to dictionary, log and corpus files
    org_cp_path = "cp/corpus"
    new_cp_path = "cp/corpus_new"
    dic_path = "cp/DeneDic.txt"
    vtdic_path = "cp/DeneVTDic.txt"
    log_path = "cp/DeneLog.txt"
    vtlog_path = "cp/DeneVTLog.txt"

    def __init__(self):
        self.vtdic = {}
        self.dic = {}
        self.logs = {}
        self.vtlogs = {}
   
        # create directory for the new corpus files
        if not os.path.isdir(self.new_cp_path):
            try:
                os.mkdir(self.new_cp_path)
            except FileNotFoundError:
                print("Corpus directory couldn't be created at",
                      self.new_cp_path)
                sys.exit(1)

    def activate_logger(self):
        """Activate logger."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler("cp.log", mode="w")
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(funcName)s|%(levelname)s|%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_dic_data(self, is_vtdic=False):
        """Collect data from a dictionary.

        is_vtdic: specify if it is a verb theme dictionary
        """
        # check which dictionary type should be processed
        if is_vtdic:
            dic = self.vtdic
            path = self.vtdic_path
        else:
            dic = self.dic
            path = self.dic_path

        with open(path, "r") as dic_file:

            # iterate file line by line
            for line in dic_file:

                line = line.rstrip()

                # if start of lemma entry is found
                if "\\lem" in line:
                    if is_vtdic:
                        # get lemma which becomes the id
                        id = line.split()[1]
                        # create entry in dic with this lemma as key
                        dic[id] = {}
                    else:
                        # get id of this lemma which is the next line
                        id = next(dic_file).split()[1]
                        # create entry in dic with this id as key
                        dic[id] = {}
                        # add the lemma
                        dic[id]["lemma"] = line.split()[1]

                    # initialize glosses as empty list
                    dic[id]["glosses"] = []

                elif "\\glo" in line:
                    dic[id]["glosses"].append(line.split()[1])

    def get_log_data(self, is_vtlog=False):
        """Collect data from log file."""
        if is_vtlog:
            path = self.vtlog_path
            logs = self.vtlogs
        else:
            path = self.log_path
            logs = self.logs

        with open(path, "r") as log_file:

            for line in log_file:
                # get log as a list of data
                log = line.rstrip().split("|")

                # UPDATE/MERGE/SPLIT
                action = log[0].upper()
                # affected id (log) or lemma (vtlog)
                id = log[1]
                # initialze log hash with id/lemma as key
                logs[id] = []

                # read rest of data
                if action == "UPDATE":
                    # old string gets replaced by new string
                    old, new = log[3].split(">")
                    # add under correct id to logs
                    logs[id].append({"action": action, "tier": log[2],
                                     "old": old, "new": new})
                elif action == "MERGE":
                    logs[id].append({"action": action, "merged_id": log[2]})

                elif action == "SPLIT":
                    logs[id].append({"action": action, "split_id": log[2],
                                     "tier": log[3], "word": log[4]})
                else:
                    self.logger.error("Action {} not defined.".format(action))

    def collect_data(self):
        """Collect data from dictionary and log file"""
        self.get_dic_data()
        self.get_dic_data(is_vtdic=True)
        self.get_log_data()
        self.get_log_data(is_vtlog=True)

    def process_corpus(self):
        """Adapt corpus data if necessary."""

        # go through each original corpus file
        for file in os.listdir(self.org_cp_path):

            # get path of this original file
            org_file_path = os.path.join(self.org_cp_path, file)

            # check if it is really a file, not a dictionary
            if os.path.isfile(org_file_path):

                # get path for new corpus file
                new_file_path = os.path.join(self.new_cp_path, file)

                # then open original file for reading and new file for writing
                with open(org_file_path, "r") as org_file, \
                     open(new_file_path, "w") as new_file:

                    # save data of one utterance using a sorted
                    # dictionary because order is important
                    # key is the fieldmarker, value the whole line (including
                    # field marker label) except for \glo, \seg, \id which are
                    # are temporarily saved in a special data structure under
                    # "words" (see below)
                    ref_dict = OrderedDict()

                    # go through all data from the corpus file
                    # and save data per utterance unter ref_dict
                    for line in org_file:

                        # throw away the newline at the end of a line
                        line = line.rstrip("\n")

                        # if new utterance starts
                        if line.startswith("\\ref"):

                            # check if there is a previous utterance
                            if ref_dict:
                                # check it for any changes
                                self.check_utterance()

                            # delete data of previous utterance
                            ref_dict.clear()
                            # add \ref to hash
                            ref_dict["\\ref"] = line

                        # if fieldmarker \full of utterance starts
                        elif line.startswith("\\full"):
                            # create "words" in ref-dict containing morpheme
                            # data for each word in a list structure because
                            # the same word can occur several times, ex.:
                            # [(word1, {"\\seg": [seg1, seg2]
                            #           "\\glo": [glo1, glo2],
                            #           "\\id": [id1, id2]})
                            #  (word2, {...})]
                            ref_dict["words"] = []

                            word_iterator = re.finditer(r"\S+", line)
                            # skip the field marker label
                            next(word_iterator)

                            n_words = 0
                            # add every word from this utterance
                            for word in word_iterator:
                                ref_dict["words"].append((word.group(), {}))
                                n_words += 1

                        # add morpheme data from \seg, \glo and \id
                        elif (line.startswith("\\seg") or
                              line.startswith("\\glo") or
                              line.startswith("\\id")):

                            # get regex & iterator for getting units per word
                            regex = re.compile(r"((\S+-\s+)*\S+(\s+-\S+)*)")
                            unitgroup_iterator = regex.finditer(line)

                            # get field marker label which is the first unit
                            label = next(unitgroup_iterator).group()

                            n_unitgroups = 0
                            # go over those units per word
                            for i, unitgroup in enumerate(unitgroup_iterator):

                                # add units to the right word (via index)
                                # to morpheme dictionary (-> 1)
                                # under the right label (\seg, \glo or \id)
                                ref_dict["words"][i][1][label] = \
                                    re.split("\s+", unitgroup.group())

                                n_unitgroups += 1

                            if n_words != n_unitgroups:
                                self.logger.error(
                                    "number of {}s and words unequal for {}".
                                    format(label, ref_dict["\\ref"]))

                        # if any other new fieldmarker starts
                        elif line.startswith("\\"):
                            # extract field marker label and its data
                            match = re.match(r"(\\\w+)(.*)", line)
                            if match:
                                label = match.group(1)
                                data = match.group(2)

                                # check if there are several defintions of the
                                # same fieldmarker in one \ref
                                if label in ref_dict:
                                    # concatenate with hash content
                                    ref_dict[label] += data
                                else:
                                    # add to hash
                                    ref_dict[label] = line

                        # if line does not start with \\, its data must belong
                        # to the fieldmarker that directly comes before
                        elif line:
                            # get last added fieldmarker
                            label = next(reversed(ref_dict))
                            # concatenate content
                            ref_dict[label] += line

                    # check last ref inserted
                    self.check_utterance()

    def check_utterance(self):
        pass

    def write_file(self, ref_dict):
        """Write data of a utterance to a file."""
        pass

    def run(self):
        """"""
        self.activate_logger()
        self.collect_data()
        self.process_corpus()


def main():
    cp = CorpusPropagater()
    cp.run()
#    print(cp.dic)
#    print(cp.vtdic)
#    print(cp.logs)
#    print(cp.vtlogs)


if __name__ == "__main__":
    main()
