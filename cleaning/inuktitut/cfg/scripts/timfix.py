#!/usr/bin/python3

import datetime as d
import re
import sys
import os

class Test:
    def __init__(self, start_str, end_str="0:0:0", use_end_bool=False):
        # This is ugly. Is there a better way to handle these exceptions?
        try:
            self.start = d.datetime.strptime(start_str, "%H:%M:%S")
        except ValueError:
            self.start = d.datetime.strptime(start_str, "%M:%S")

        try:
            self.end = d.datetime.strptime(end_str, "%M:%S")
        except ValueError:
            self.end = d.datetime.strptime(end_str, "%H:%M:%S")

        self.use_end = use_end_bool

    def __repr__(self):
        ret = self.start.strftime("%H:%M:%S")
        if (self.use_end):
            ret += "-" + self.end.strftime("%H:%M:%S")
        return ret

    def __str__(self):
        ret = self.start.strftime("%H:%M:%S")
        if (self.use_end):
            ret += "-" + self.end.strftime("%H:%M:%S")
        return ret

    def applyOffset(self, offset, offset_positive=True):
        delta_start = self.start - offset.start
        self.start = d.datetime.strptime("0:0:0", "%H:%M:%S") + delta_start
        if (self.use_end):
            # YES! We use the "offset.start". We want to shift both start and
            # end of "self" in the same "offset".
            delta_end = self.end - offset.start
            self.end = d.datetime.strptime("0:0:0", "%H:%M:%S") + delta_end

def get_time_offset(f):
    found = False
    for line in f:
        if (line.startswith("@Tape Location")):
            found = True
            try:
                line = re.search('File: \w+ \((.+?)[-\)]', line).group(1)
                break
            except AttributeError:
                print("ERROR: Couldn't parse tier '@Tape Location'")
                sys.exit(1)

    if not found:
        print("ERROR: Couldn't find tier '@Tape Location'")
        sys.exit(1)

    return Test(line)

def parse_tim_line(line, line_number):
    try:
        line = re.search("%tim:\t(.+)\n", line).group(1)
    except AttributeError:
        print("ERROR: Line {} badly formatted".format(line_number))
        sys.exit(1)

    tim = None
    try:
        #print("line: {}".format(line))
        parsed_start = re.search("(.+)\-(.+)", line).group(1)
        #print("parsed_start: {}".format(parsed_start))
        parsed_end = re.search("(.+)\-(.+)", line).group(2)
        #print("parsed_end: {}".format(parsed_end))
        tim = Test(parsed_start, parsed_end, True)
    except AttributeError:
        # Try creating it only with start
        tim = Test(line)

    if tim is None:
        print("ERROR: Couldn't create time representation in line {}".
                                                format(line_number))
        sys.exit(1)

    return tim

def fix_tim_tier(f, out_folder_name):
    folder_name = "output-timfix"
    if (out_folder_name is not None):
        folder_name = out_folder_name

    # Opens an output file with the same name as `f`, only in a new folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_name_without_path = os.path.basename(f.name)
    out = open(folder_name + "/" + file_name_without_path, 'w')

    # Finds out the time "offset"
    offset = get_time_offset(f)

    f.seek(0)

    # Goes through all file lines. When reach a "%tim"
    for line_number, line in enumerate(f):
        if (line.startswith("%tim")):
            # Creates a time representation based on its content
            curr_tim = parse_tim_line(line, line_number)

            # "Shifts" this time by the "offset"
            curr_tim.applyOffset(offset, False)

            line = "%tim:\t{}\n".format(curr_tim)

        # Inserts line in output file
        out.write(line)

def get_input_info(arguments):
    # If arguments, use that place to find files
    if (len(arguments) < 2):
        print_usage()
        sys.exit(1)

    try:
        f = open(arguments[1], 'r')
    except IOError:
        print("ERROR: Couldn't open file {}".format(arguments[1]))
        sys.exit(1)

    out_folder_name = None
    if (len(arguments) == 3):
        out_folder_name = arguments[2]

    return f, out_folder_name

def print_usage():
    print("Usage:")
    print("\ttimfix.py <file_to_be_fixed> <output_folder_name>")

if __name__ == "__main__":
    f, out_folder_name = get_input_info(sys.argv)
    fix_tim_tier(f, out_folder_name)


