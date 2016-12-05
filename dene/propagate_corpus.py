"""
@author: Anna Jancso
"""


class CorpusPropagater:

    def __init__(self):

        self.logs = {}
        self.dic = {}

    def get_dic_data(self):

        with open("DeneDic.txt", "r") as dic_file:

            # iterate file line by line
            for line in dic_file:

                # if lemma entry is found
                if "\lem" in line:

                    # get id of this lemma which is the next line
                    id = next(dic_file).split()[1]

                    # create entry in dic hash with id as key
                    self.dic[id] = {}

                    # add the lemma
                    self.dic[id]["lemma"] = line.split()[1]

                    # initialize glosses as empty list
                    self.dic[id]["glosses"] = []

                elif "\glo" in line:
                    self.dic[id]["glosses"].append(line.split()[1])


def main():
    cp = CorpusPropagater()
    cp.get_dic_data()
    print(cp.dic)

if __name__ == "__main__":
    main()
