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

        # save data of one utterance using a sorted dict because order is
        # important; key is the fieldmarker, value the whole line (including
        # field marker label) except for \glo, \seg, \id which are
        # temporarily saved in a special data structure under "words"
        self.ref_dict = OrderedDict()

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
                # initialze log hash with id/lemma as key if necessary
                if id not in logs:
                    logs[id] = []

                # format for UPDATE: UPDATE|id|glo/seg|old_glo/seg>new_glo/seg
                if action == "UPDATE":
                    # get old and new gloss/lemma
                    old, new = log[3].split(">")
                    # add under correct id to logs
                    logs[id].append({"action": action, "tier": log[2],
                                     "old": old, "new": new})
                # format for MERGE: MERGE|
                elif action == "MERGE":
                    logs[id].append({"action": action, "merging_id": log[2]})

                elif action == "SPLIT":
                    logs[id].append({"action": action, "splitting_id": log[2],
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
        """Process every corpus file."""
        # first create directory for the new corpus files
        if not os.path.isdir(self.new_cp_path):
            try:
                os.mkdir(self.new_cp_path)
            except FileNotFoundError:
                print("Corpus directory couldn't be created at",
                      self.new_cp_path)
                sys.exit(1)

        # go through each original corpus file
        for file in os.listdir(self.org_cp_path):

            # if it is a toolbox file
            if file.endswith(".tbt"):

                # get path of this original file
                org_file_path = os.path.join(self.org_cp_path, file)

                # get path for new corpus file
                new_file_path = os.path.join(self.new_cp_path, file)

                # then open original file for reading and new file for writing
                with open(org_file_path, "r") as org_file, \
                     open(new_file_path, "w") as new_file:

                    self.process_file(org_file, new_file)

    def process_file(self, org_file, new_file):
        """"""
        has_errors = False
        # go through all data fomr a corpus file
        # and save data per utterance unter ref_dict
        for line in org_file:

            # throw away the newline at the end of a line
            line = line.rstrip("\n")

            # if new utterance starts
            if line.startswith("\\ref"):
                # check previous utterance for any necessary changes
                self.check_utterance(has_errors=has_errors)
                # reset to False
                has_errors = False
                # delete data of previous utterance
                self.ref_dict.clear()
                # add \ref to hash
                self.ref_dict["\\ref"] = line

            # if fieldmarker \full of utterance starts
            elif line.startswith("\\full"):
                # save morpheme data in a special data structure
                # words: [(word1, {"\\seg": [seg1, seg2]
                #                  "\\glo": [glo1, glo2],
                #                  "\\id": [id1, id2]}), (word2, {...})]
                self.ref_dict["words"] = []

                # extract words splitting the processed line at whitespaces
                word_iterator = re.finditer(r"\S+", line)
                # skip the field marker label
                next(word_iterator)

                # count the words
                n_words = 0
                # add every word to the hash
                for word in word_iterator:
                    self.ref_dict["words"].append((word.group(),
                                                   {}))
                    n_words += 1

            # add morpheme data from \seg, \glo and \id
            elif (line.startswith("\\seg") or
                  line.startswith("\\glo") or
                  line.startswith("\\id")):

                # get regex & iterator for extracting units per word
                regex = re.compile(r"((\S+-\s+)*\S+(\s+-\S+)*)")
                unitgroup_iterator = regex.finditer(line)

                # get field marker label which is the first unit
                label = next(unitgroup_iterator).group()

                # count number of unit groups (i.e. glos, segs, ids)
                n_unitgroups = 0
                # go over those units per word
                for i, unitgroup in enumerate(unitgroup_iterator):

                    # add units to the right word (via index)
                    # to morpheme dictionary (at index 1)
                    # under the right label (\seg, \glo or \id)
                    self.ref_dict["words"][i][1][label] = \
                        re.split("\s+", unitgroup.group())

                    n_unitgroups += 1

                if n_words != n_unitgroups:
                    self.logger.error(
                        "number of {}s and words unequal for {}".
                        format(label, self.ref_dict["\\ref"]))

                    has_errors = True

            # if any other new fieldmarker starts
            elif line.startswith("\\"):
                # extract field marker label and its data
                match = re.match(r"(\\\w+)(.*)", line)
                if match:
                    label = match.group(1)
                    data = match.group(2)

                    # check if there are several defintions of the
                    # same fieldmarker in one \ref
                    if label in self.ref_dict:
                        # concatenate with hash content
                        self.ref_dict[label] += data
                    else:
                        # add to hash
                        self.ref_dict[label] = line

            # if line does not start with \\, its data must belong
            # to the fieldmarker that directly comes before
            elif line:
                # get last added fieldmarker
                label = next(reversed(self.ref_dict))
                # concatenate content
                self.ref_dict[label] += line

        # check last ref inserted
        self.check_utterance(has_errors=has_errors)

    def check_utterance(self, has_errors=False):
        """Check utterance for ids in the log."""
        # if utterance has errors or no words in it
        if has_errors or "words" not in self.ref_dict:
            # write unchanged to file
            self.write_file()
        else:
            # check all words for ids in log
            for w_pos, (word, data) in enumerate(self.ref_dict["words"]):

                # if there is morpheme data for this word
                if data:

                    # go through every lemma id of this word
                    for m_pos, m_id in enumerate(data["\\id"]):

                        # strip '-' left and right of id (if there is)
                        norm_id = m_id.strip("-")

                        # check if this id is in the log file
                        if norm_id in self.logs:

                            # go through all logs with this id
                            for l_pos, log in enumerate(self.logs[norm_id]):

                                # get function based on action name of this log
                                action = getattr(self, log["action"].lower())

                                # call it
                                action(w_pos, m_pos, norm_id, l_pos)

    def update(self, w_pos, m_pos, norm_id, l_pos):
        """Update data of a lemma."""
        # get right log data
        log = self.logs[norm_id][l_pos]
        # get glo or seg tier
        tier = self.ref_dict["words"][w_pos][1]["\\" + log["tier"]]

        # change tier at the right position
        if log["old"] in tier[m_pos]:
            tier[m_pos] = tier[m_pos].replace(log["old"], log["new"])

    def merge(self, w_pos, m_pos, norm_id, l_pos):
        """"""
        print("merge")
        pass

    def split(self, w_pos, m_pos, norm_id, l_pos):
        """"""
        print("split")
        pass

    def write_file(self):
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
