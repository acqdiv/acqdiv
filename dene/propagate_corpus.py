"""
@author: Anna Jancso
"""

class CorpusPropagater:

    def __init__(self):

        self.dic_path = "DeneDic.txt"
        self.vtdic_path = "DeneVTDic.txt"

        self.logs = {}
        self.vtdic = {}
        self.dic = {}

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

    def run(self):
        self.get_dic_data()
        self.get_dic_data(is_vtdic=True)


def main():
    cp = CorpusPropagater()
    cp.run()
#    print(cp.dic)
#    print(cp.vtdic)

if __name__ == "__main__":
    main()
