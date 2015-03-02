import sys
from path import path

obligatory = ["@UTF8", "@Begin", "@Languages:", "@Participants:", "@Options:", "@ID:", "@Media:", "@Angles:", "@End"]
no_tab = ["@UTF8", "@Begin", "@End", "@New Episode"]
changeables = ["@Activities:", "@Bck:", "@Bg", "@Bg:", "@Blank", "@Comment:", "@Date:", "@Eg", "@Eg:", "@EndTurn", "@G:", "@New Episode", "@New Language:", "@Page", "@Situation:", "@T:"]


def main(path):
    infile = open(path, "r")
    n = 0
    fields = [path.basename()]
    for line in infile:
        n += 1
        line = line.strip()

        # header errors
        if line.startswith("@") and not line in no_tab:
            # now skip indvidual stuff
            if line.__contains__("@Font"):
                continue
            if line.__contains__("@Language"):
                continue
            if line.endswith(":"):
                continue

            line = line.replace("\t", " ")
            fields.append(line)
            # print(path.basename()+"\t"+line)

            """
            if not line in no_tab and not line in changeables:
                # catch empty header lines
                if line.endswith(":"):
                    logging.debug(str(path)+":"+str(n)+"\tEMPTY HEADER LINE\t"+line)
                # catch missing tabbed lines
                elif not line.__contains__("\t"):
                    logging.debug(str(path)+":"+str(n)+"\tNO TAB IN LINE\t"+line)
                    tokens = line.split(":")
                    print("\t".join(tokens))
                    """
    print("\t".join(fields))
    infile.close()

if __name__=="__main__":
    dir = sys.argv[1]
    type = sys.argv[2]
    for f in path(dir).files(type):
        if not f.basename().startswith('.'):
            main(f)


