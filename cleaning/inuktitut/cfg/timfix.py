import datetime as d
import re
import sys

def read_time_pattern(pattern, line):
    # Takes the part of the line we are interested in
    extime = re.search(pattern, line)

    try:
        extime_str = extime.group(1)
    except AttributeError:
        extime_str = ''

    end_time = d.datetime.strptime("0:0:0", "%H:%M:%S")
    try:
        end_time = d.datetime.strptime(extime_str, "%H:%M:%S")
    except ValueError:
	end_time = False

    # If this format worked, we can just return
    if (end_time):
        return end_time

    try:
        end_time = d.datetime.strptime(extime_str, "%M:%S")
    except ValueError:
        end_time = d.datetime.strptime("0:0:0", "%H:%M:%S")

    return end_time

def read_start_time(line):
    return read_time_pattern("\((\d{1,2}((:\d{1,2}){1,2}))", line)


def read_start_time_test():
    a = read_start_time("@Portion:	ALI01F02.MAR (06:08-2:03:41)")
    print a.strftime("%H:%M:%S")
    a = read_start_time("@Portion:	ALI01F02.MAR (01:06:08)-2:03:41)")
    print a.strftime("%H:%M:%S")
    a = read_start_time("@Portion:	ALI01F02.MAR (01:06:08:-2:03:41)")
    print a.strftime("%H:%M:%S")
    a = read_start_time("@Portion:	ALI01F02.MAR (01:06:080-2:03:41)")
    print a.strftime("%H:%M:%S")
    a = read_start_time("@Portion:	ALI01F02.MAR (01:06:08-2:03:41)")
    print a.strftime("%H:%M:%S")
    a = read_start_time("@Portion:	ALI01F02.MAR (1:06:08-2:03:41)")
    print a.strftime("%H:%M:%S")
    a = read_start_time("@Portion:	ALI01F03.MAR (0:00:00-0:19:46)")
    print a.strftime("%H:%M:%S")
    a = read_start_time("@Portion:	ALI02F01.APR (0:00:00-1:26:48)")
    print a.strftime("%H:%M:%S")
    a = read_start_time("@Portion:	ALI02F02.APR (1:26:52-2:03:15)")
    print a.strftime("%H:%M:%S")

def fix_tim_line(line, start_time):
    line_time = read_time_pattern("(\d{1,2}((:\d{1,2}){1,2}))", line)

    time_delta = line_time - start_time
    new_time = d.datetime.strptime("0:0:0", "%H:%M:%S") + time_delta

    #print "line_time: %s" % line_time.strftime("%H:%M:%S")
    #print "start_time: %s" % start_time.strftime("%H:%M:%S")
    #print "time_delta: %d" % time_delta.seconds
    #print "new_time: %s" % new_time.strftime("%H:%M:%S")
    #print "new_time: %s" % new_time

    # If the delta is "negative", doesn't change the line
    if (new_time.year < 1900):
        return line

    new_line = "%tim\t"
    new_line += new_time.strftime("%H:%M:%S")
    return new_line

def fix_time_line_test():
    s = read_start_time("@Portion:	ALI02F02.APR (1:26:52-2:03:15)")
    a = fix_tim_line("%foo 10:10:00", s)
    print a
    s = read_start_time("@Portion:	ALI02F02.APR (0:01:00-2:03:15)")
    a = fix_tim_line("%foo 10:10:00:", s)
    print a
    a = fix_tim_line("%foo 00:00:00", s)
    print a
    a = fix_tim_line("%foo 10:00:", s)
    print a

def fix_times(fname):
    """ Reads each line searching for the tier "@Portion".
    Extracts the starting time.
    Searches for all "%tim" lines.
    Subtracts the starting time from the time in the "%tim" line """
    f = open(fname, 'r')

    found = False
    start_time = False
    for line in f:
        if (line.startswith("@Portion:")):
            found = True
            start_time = read_start_time(line)
            break

        # @Portion should have been found in the headers.
        if (line.startswith("*")):
            break

    if (not found):
        print("ERROR: File doesn't contain the '@Portion:' header")

    f.seek(0)
    for line in f:
        newline = line
        if (line.startswith("%tim")):
            newline = fix_tim_line(line, start_time)
        sys.stdout.write(newline)

def print_usage():
    print("Usage:\n\ttimfix.py <file_to_be_fixed>")

if (len(sys.argv) < 2):
    print_usage()
    sys.exit(1)

fix_times(sys.argv[1])

