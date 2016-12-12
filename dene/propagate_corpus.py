"""
@author: Anna Jancso
"""
import logging


class CorpusPropagater:

    original_cp_path = "cp/corpus"
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
                if "\lem" in line:

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

                elif "\glo" in line:
                    dic[id]["glosses"].append(line.split()[1])

    def get_log_data(self, is_vtlog=False):

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
        self.get_dic_data()
        self.get_dic_data(is_vtdic=True)
        self.get_log_data()
        self.get_log_data(is_vtlog=True)

    def process_corpus():
        pass

    def run(self):
        self.activate_logger()
        self.collect_data()


def main():
    cp = CorpusPropagater()
    cp.run()
#    print(cp.dic)
#    print(cp.vtdic)
#    print(cp.logs)
#    print(cp.vtlogs)

if __name__ == "__main__":
    main()
