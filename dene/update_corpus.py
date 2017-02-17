"""
Module provides a class for propagating changes in corpus files made in
dictionary files which are tracked in log files.

Files used by the script and their locations:
    this script file:           Scripts/
    original corpus files:      Corpus files/
    new corpus files:           Scripts/
    dictionary files:           Dictionaries/
    corpus log files:           Dictionaries/
    script log file:            Scripts/

Run:
    python3 update_corpus
"""
import os
import re
from process_corpus import CorpusProcesser


class Propagator:
    """Class for propagating changes in dictionary in corpus."""

    # default paths
    org_cp_path = "../Corpus files"
    new_cp_path = "New Corpus files"
    dic_path = "../Dictionaries/DeneDic.txt"
    vtdic_path = "../Dictionaries/DeneVTDic.txt"
    log_path = "../Dictionaries/DeneLog.txt"
    vtlog_path = "../Dictionaries/DeneVTLog.txt"

    def __init__(self, dic_path=None, vtdic_path=None, log_path=None,
                 vtlog_path=None, org_cp_path=None, new_cp_path=None):
        """Initialize paths to dictionary and log files."""
        # initialize paths
        if dic_path is not None:
            self.dic_path = dic_path

        if vtdic_path is not None:
            self.vtdic_path = vtdic_path

        if log_path is not None:
            self.log_path = log_path

        if vtlog_path is not None:
            self.vtlog_path = vtlog_path

        if org_cp_path is not None:
            self.org_cp_path = org_cp_path

        if new_cp_path is not None:
            self.new_cp_path = new_cp_path

    def get_dic_data(self, is_vtdic=False):
        """Collect data from a dictionary.

        is_vtdic (bool): verb theme dictionary or not
        """
        # check which dictionary type should be processed
        if is_vtdic:
            self.vtdic = {}
            dic = self.vtdic
            path = self.vtdic_path
        else:
            self.dic = {}
            dic = self.dic
            path = self.dic_path

        # check if path is valid
        if not os.path.isfile(path):
            print("Path '{}' for dictionary file does not exist".format(path))
            print()
            return

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
                        dic[id]["lem"] = line.split()[1]

                    # initialize glosses as empty list
                    dic[id]["glo"] = []

                elif "\\glo" in line:
                    dic[id]["glo"].append(line.split()[1])

    def get_log_data(self, is_vtlog=False):
        """Collect data from log file.

        is_vtlog (bool): verb theme log or not
        """
        if is_vtlog:
            self.vtlogs = {}
            logs = self.vtlogs
            path = self.vtlog_path
        else:
            self.logs = {}
            logs = self.logs
            path = self.log_path

        # check if path is valid
        if not os.path.isfile(path):
            print("Path '{}' for log file does not exist".format(path))
            print()
            return

        with open(path, "r") as log_file:

            for line in log_file:
                # get log as a list of data
                log = line.rstrip().split("|")
                # UPDATE/MERGE/SPLIT
                cmd = log[0].upper()
                # affected id (log) or lemma (vtlog)
                id = log[1]
                # initialze log hash with id/lemma as key if necessary
                if id not in logs:
                    logs[id] = []

                # format for UPDATE: UPDATE|id|tier==old|new
                if cmd == "UPDATE":
                    # get tier (seg|glo|vtg) and old seg/glo/vtg value
                    tier, old = re.split("==", log[2])
                    # add under correct id to logs
                    logs[id].append({"cmd": cmd, "tier": tier,
                                     "old": old, "new": log[3]})
                # format for MERGE: MERGE|old_id|new_id
                elif cmd == "MERGE":
                    logs[id].append({"cmd": cmd, "new_id": log[2]})

                # format for SPLIT: SPLIT|old_id|new_id|tier==criterion
                elif cmd == "SPLIT":
                    # get tier (full|glo|vtg) and criterion value
                    tier, criterion = re.split("==", log[3])
                    logs[id].append({"cmd": cmd, "new_id": log[2],
                                     "tier": tier, "criterion": criterion})
                else:
                    self.logger.error("Command {} not defined.".format(cmd))

    def collect_data(self):
        """Collect data from dictionary and log files."""
        self.get_dic_data()
        self.get_dic_data(is_vtdic=True)
        self.get_log_data()
        self.get_log_data(is_vtlog=True)

    def update_utterance(self, utterance):
        """Update utterance according to the log."""
        # check all words for ids in log
        for word, morphemes in utterance["words"]:

            # go through every morpheme id of this word
            for m_pos, m_id in enumerate(morphemes["\\id"]):

                # strip '-' left and right of id (if there is)
                norm_id = m_id.strip("-")

                # do the same for the lemma in \vt
                norm_lem = morphemes["\\vt"][m_pos].strip("-")

                # go through log files
                for key, logs, vt in [(norm_id, self.logs, False),
                                      (norm_lem, self.vtlogs, True)]:

                    # check if id/lemma is in log file
                    if key in logs:

                        # go through all logs with this id/lemma
                        for log in logs[key]:

                            # get command type
                            cmd = log["cmd"].upper()

                            if cmd == "UPDATE":
                                self.update(morphemes, m_pos, log)
                            elif cmd == "MERGE":
                                self.merge(morphemes, m_pos, log, vt)
                            elif cmd == "SPLIT":
                                self.split(word, morphemes, m_pos, log, vt)

    def update(self, morphemes, m_pos, log):
        """Update data of a lemma.

        morphemes (hash): morpheme tiers of a word
        m_pos (int): morpheme position in a word
        log (hash): normal/vt log
        """
        # get glo or seg tier
        tier = morphemes["\\" + log["tier"]]
        # change tier at the right position
        if log["old"] in tier[m_pos]:
            tier[m_pos] = tier[m_pos].replace(log["old"], log["new"])

    def sub_ms(self, new, string):
        """Substitute morpheme data in a string.

        new (str): new morpheme value
        string (str): where old morpheme value is replaced by new one
        """
        # regex for replacing morpheme data
        rgx = re.compile(r"(-)?(.*?)(-)?$")
        # replace string (note: \g<> is needed because ids are also integers)
        repl = r"\g<1>{}\g<3>".format(new)

        return rgx.sub(repl, string)

    def merge(self, morphemes, m_pos, log, vt=False):
        """Merge lemma into another.

        morphemes (hash): morpheme tiers of a word
        m_pos (int): morpheme position in a word
        log (hash): normal/vt log
        vt (bool): verbe theme or not
        """
        # id/lemma into which lemma is merged
        key = log["new_id"]

        if vt:
            # check if lemma has an entry in the vt-dictionary
            if key not in self.vtdic:
                self.logger.error("Lemma {} not in vt-dictionary".format(key))
                return

            # adjust \vt
            morphemes["\\vt"][m_pos] = self.sub_ms(key,
                                                   morphemes["\\vt"][m_pos])

            # if original vtg is not in the new dictionary entry
            if morphemes["\\vtg"][m_pos] not in self.vtdic[key]["glo"]:

                # replace by the first vtg of the new dictionary entry
                morphemes["\\vtg"][m_pos] = self.sub_ms(
                    self.vtdic[key]["glo"][0], morphemes["\\vtg"][m_pos])

        else:
            # check if id has an entry in the dictionary
            if key not in self.dic:
                self.logger.error("Id {} not in dictionary".format(key))
                return

            # adjust id and seg
            morphemes["\\id"][m_pos] = self.sub_ms(key,
                                                   morphemes["\\id"][m_pos])

            morphemes["\\seg"][m_pos] = self.sub_ms(self.dic[key]["lem"],
                                                    morphemes["\\seg"][m_pos])

            # if original glo is not in the new dictionary entry
            if morphemes["\\glo"][m_pos] not in self.dic[key]["glo"]:

                # replace by the first gloss of the new dictionary entry
                morphemes["\\glo"][m_pos] = self.sub_ms(
                    self.dic[key]["glo"][0], morphemes["\\glo"][m_pos])

    def split(self, word, morphemes, m_pos, log, vt=False):
        """Split lemma entry into two separate ones.

        word (str): concerned word
        morphemes (hash): morpheme tiers of a word
        m_pos (int): morpheme position in a word
        log (hash): normal/vt log
        vt (bool): verbe theme or not
        """
        # check if criterion for disambiguation is in \full or \glo
        if log["criterion"] in [word, morphemes["\\glo"][m_pos].strip("-")]:

            # merge with data from new entry
            self.merge(morphemes, m_pos, log, vt=vt)

    def propagate(self):
        """Propagate changes in dictionary in corpus."""
        # get dictionary and log data
        self.collect_data()

        # get a corpus processer
        cp = CorpusProcesser(self.org_cp_path, self.new_cp_path)

        # go through each utterance of all corpus files
        for utterance in cp:
            # if there are no errors in the utterance
            if not cp.has_errors:
                # change data if necessary
                self.update_utterance(utterance)

            # write (un)changed utterance back to file
            cp.write_file()


def main():
    cp = Propagator()
    cp.propagate()

if __name__ == "__main__":
    main()
