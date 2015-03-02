import sys
import unicodedata

infile = open(sys.argv[1], "r")
outfile = open("d_"+sys.argv[1], "w")

cc = [61531, 61533, 61475, 61516]

header = ["Frequency", "Glyph", "Unicode Decimal", "Unicode Name"]
outfile.write("\t".join(header)+"\n")
for line in infile:
    result = []
    line = line.strip()
    if not line.__contains__("\t"):
        continue
    tokens = line.split("\t")
    # print(ord(tokens[0]), tokens[0])
    # continue

    # control characters
    if ord(tokens[0]) < 31 or ord(tokens[0]) == 130 or ord(tokens[0]) == 146 or ord(tokens[0]) == 141 or ord(tokens[0]) == 145 or ord(tokens[0]) == 150 or ord(tokens[0]) == 147 or ord(tokens[0]) == 148 or ord(tokens[0]) == 129 or ord(tokens[0]) > 60000:
        result.append(tokens[1])
        result.append("CC")
        result.append(str(ord(tokens[0])))
        result.append("CONTROL CHARACTER")
        print("\t".join(result))
        outfile.write("\t".join(result)+"\n")
        continue

    # higher range unicode characters (add to list for now)
    if ord(tokens[0]) in cc:
        result.append(tokens[1])
        result.append(tokens[0])
        result.append(str(ord(tokens[0])))
        result.append("UNASSIGNED CHARACTER")
        print("\t".join(result))
        outfile.write("\t".join(result)+"\n")
        continue

    result = [tokens[1]]
    result.append(tokens[0])
    result.append(str(ord(tokens[0])))
    result.append(unicodedata.name(tokens[0]))
    print("\t".join(result))
    outfile.write("\t".join(result)+"\n")
    
