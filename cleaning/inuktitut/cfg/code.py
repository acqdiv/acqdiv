def clean_filename(fname): 
    return fname.rstrip(".NAC").rstrip(".XXS").rstrip(".XXX").rstrip(".MAY")

def clean_chat_line(s):

    import difflib
    def diff(a, b):
        print('{} => {}'.format(a,b))  
        for i,s in enumerate(difflib.ndiff(a, b)):
            if s[0]==' ': continue
            elif s[0]=='-':
                print(u'Delete "{}" from position {}'.format(s[-1],i))
            elif s[0]=='+':
                print(u'Add "{}" to position {}'.format(s[-1],i))    
        print() 

    def fixpoint_regex(str_match, str_replace, s):
        s1 = s
        #print(s)
        while (True):
            s = re.sub(str_match, str_replace, s)
            if s1 == s:
                break
            #else:
            #    diff(s1,s)
            s1 = s

        return s

    """ Removes all punctuation chunks except the last one """
    def remove_punctuations(s):
        inside = 0
        ending = ''
        out = ''
        for i in s:
            if i in '[(':
                inside += 1
                out += i
                ending = ''
            elif i in ')]':
                inside -= 1
                out += i
                ending = ''
            elif inside > 0:
                out += i
                ending = ''
            elif i in '.!?+/':
                ending += i
            else:
                out += i
                ending = ''

        return out + " " + ending

    def remove_unmatched_brackets(s):
        index_stack = []
        output_list = []
        curr_str = ''
        index = 0
        for i in s:
            if i in '<':
                # Inserts current output in stack
                output_list.append(curr_str)
                output_list.append(i)
                index += 1

                # Inserts bracket in stack
                index_stack.append(index)
                index += 1
                curr_str = ''
            elif i in '>':
                output_list.append(curr_str)
                index += 1
                if (len(index_stack) > 0):
                    index_stack.pop()
                    output_list.append(i)
                    index += 1
                curr_str = ''
            else:
                curr_str += i

        output_list.append(curr_str)

        # Now, removes index for last to first
        for i in reversed(index_stack):
            del output_list[i]

        return ''.join(output_list)


    def check_for_letters(s):
        splitted = s.split(":",1)
        if len(splitted) == 1:
            # There should be something very wrong with this one
            return ''

        utterance = splitted[1]
        if all(not i.isalpha() for i in utterance):
            return splitted[0] + ':\t0.'

        utterance = re.sub('\w\w+', lambda m: m.group(0)[0] +
                                    m.group(0)[1:].lower(), utterance)

        utterance = re.sub('\u201C\w+', lambda m: m.group(0)[0] + m.group(0)[1:].lower(), utterance)
        #if '\u201C' in utterance:
        #    print("Utterance: " + utterance)


        return splitted[0] + ':' + utterance

    def clean_main_line(s):
        # Changes, e.g., "2x" and "x2" into "x 2"
        #s = re.sub("(\d+)\s?(x)", "(\\2 \\1)", s)
        #s = re.sub("(x)\s?(\d+)", "(\\1 \\2)", s)

        s = remove_unmatched_brackets(s)
        s = check_for_letters(s)

        # Idiossyncratic strings fixed by hand
        s = re.sub("\(repeated six times\)", "[x 6]", s)
        s = re.sub("\( i don't like it \)", ", i don't like it", s)
        s = re.sub("nirigiartulangavit xxx \(pipungupualugamai\?\)",
                   "nirigiartulangavit <pipungupualugamai> [?] ?", s)
        s = re.sub("walrus -xxx", "walrus-xxx", s)
        s = re.sub("<susaa> qaigit", "susaa qaigit", s)
        s = re.sub("<i>\.", "i.", s)
        s = re.sub("<situragiatuqanniqin>", "situragiatuqanniqin", s)
        s = re.sub("<ping>", "ping", s)

        # Changes "(2 x)" and "(x 2)" (with or without parenthesis) into
        # "[x 2]"
        s = re.sub("\s\(?(\d+)\s*x\)?(\s|$|\.|,|!|\?|\[)", " [x \\1] ", s)
        s = re.sub("\s\(?x\s*(\d+)\)?(\s|$|\.|,|!|\?|\[)", " [x \\1] ", s)

        s = re.sub('XXX', 'xxx', s)
        s = re.sub('&', '', s)
        s = re.sub('\"(.*)\"', '\u201C\\1\u201D', s)
        s = re.sub('\s\((.*)\)(\s|\.|$)', ' [= \\1] ', s)
        s = re.sub('\[=!(\w+)\]', '[=! \\1]', s)

        s = check_for_letters(s)

        s = re.sub('\[\"\]', '[% Direct speech]', s)

        # These characters are not allowed in the Main Line.
        s = re.sub(' - ', ' (.) ', s)

        #s1 = s
        s = re.sub(' / ', ' (.) ', s)
        #if s1 != s:
        #    print('s')
        #    print(s)
        #    print('s1')
        #    print(s1)

        # Removes the #. Three cases:
        # 1) Beginning of utterance: suppressed
        # 2) Between words: transformed in pause
        # 3) Inside words: transformed in syllable prolongation
        s = re.sub('(?<=:\t)\s*#\s*', ' ', s)
        s = re.sub('\s+#\s*', ' (.) ', s)
        s = re.sub('\s*#\s+', ' (.) ', s)
        s = re.sub('\w#\w', ':', s)

        # In case there are too many pauses now
        #s = re.sub('(\s*\(\.\)\s*)*', ' (.) ', s)

        # "+... [something]" --> "[something] +..."
        s = re.sub("(\+\.*)\s*(\[.*\])", " \\2 \\1 ", s)
        # ". [something]" --> "[something] ."
        s = re.sub("(\.|\?|!)\s*(\[.*\])", " \\2 \\1 ", s)

        # Takes punctuation in the end of <...> out of it
        #s = re.sub("<((\s|\w)*)((\.|\?|!|\+)+)>\s*\[((.)*)\]",
	#				"<\\1> [\\5] \\3", s)

        s = fixpoint_regex("<((\s|\w)*)((\.|\?|!|\+)+)>\s*\[((.)*)\]",
                            "<\\1> [\\5] \\3", s)

        # Removes "," in the end of the line
        s = re.sub("((\.|\?|!)*)\s*,\s*$", "\\1", s)

        # If it doesn't end with ".", "!" or "?", puts a "."
        s = re.sub("([^\.\?!]\s*$)", "\\1 .", s)

        # If there is a "." after a "!" or a "?", give preference to the "!"/"?"
        s = re.sub("([\?!])\s*.\s*$", "\\1", s)

        # Inserts space after ","
        s = re.sub(",(\S+)", ", \\1", s)

        # Removes repeated (redundant) uterrance delimiters
        #s = re.sub("(?<=\\w|\])(!\s*)+", " ! ", s)
        #s = re.sub("(?<=\\w|\])(\?\s*)+", " ? ", s)
        #s = re.sub("(?<=\\w|\])\s*(\s+\.)+", " .", s)
        s = fixpoint_regex("!\s*!", "!", s)
        s = fixpoint_regex("\?\s*\?", "\?", s)
        s = fixpoint_regex("\.\s+\.", " .", s)

        # ?! --> +?!
        #s = re.sub('(?<=\\w)\?!', '+?!', s)
        s = re.sub('!\?!', '!?', s)
        s = re.sub('!\?', ' +!?', s)
        s = re.sub('\?!', ' +!?', s)

        # "+. ." --> "+." (i.e., removes the second "." after "+.")
        s = re.sub('(?<=\\w)\s*\+\.\\s+\.$', ' +.', s)

        # "..", "...", ". ." --> "+..."
        s = re.sub('\s*\.\s*(\.\s*)+$', ' +...', s)
        s = re.sub('\+\s*\+', ' +', s)

        # ", ." --> "."
        s = re.sub(',\s*\.$', '.', s)

        # "wordword+..." --> "wordword +..."
        s = re.sub('(?<=\\w)\+\.\.\.', ' +...', s)

        # Removes punctuation just before "(.)"
        s = re.sub("(\.|!|\+!\?|\?)+\s*\(\.\)\s*", " (.) ", s)

        # If no punctuation fix worked so far, simply remove it
        s = remove_punctuations(s)

        # If it doesn't end with ".", "!" or "?", puts a "."
        # FIXME: Check why the dot was removed, if I had already put it before
        s = re.sub("([^\.\?!]\s*$)", "\\1 .", s)

        ### removes ","
        #s = re.sub(",", "", s)

        # added by rabart
        # NEVER MATCHED!!!
	# These would remove "+." and "+...", if they worked
        #s = re.sub('(?<=\\w)\+[\.,\/]*$', '', s)
        #s = re.sub('(?<=\\w)\+\.\.\.\s+(?=\\w)', ' ', s)


        # "wordword+. wordword" --> "&wordword wordword" (& indicates
        # incomplete word)
        s = re.sub('(\\S+)\+\.(?=\\s\\w)', '&\\1', s)

        s = re.sub('(?<=\\s)xx(?=\\s)', 'xxx', s) # xx -> xxx
        return s



















    # Puts a tab after tier name
    s = re.sub("(^\*[A-Z0-9]{3}:)(\s+)", r"\1\t", s)
    s = re.sub("(^\%[a-z0-9]{3}:)(\s+)", r"\1\t", s)
    s = re.sub("(^\*\?\?\?:)(\s+)", r"\1\t", s) # shouldn't be necessary anymore

    # Some generic cleaning
    s = re.sub("\u001A", r"", s)
    s = re.sub("\*xxx:\s", r"*UNK:\t", s)
    s = re.sub("%COM:", "%com:", s)
    s = re.sub("%tim:0:20:00", "", s)
    s = re.sub("@End\s+_", "@End", s)

    # Care with the order of these two
    s = re.sub("@Break", "@New Episode", s)
    s = re.sub("@New Episode:", "@New Episode\n@Situation:", s)
    s = re.sub("@Comments:", "@Comment:", s)
    s = re.sub("@TIME WARP. SOUND IS ON", "@Comment: TIME WARP. SOUND IS ON", s)

    s = re.sub("@ŽIP0,16Ż", "", s)
    s = re.sub("@ŽIP0,8Ż", "", s)
    s = re.sub("ŽIP0,16Ż", "", s)
    s = re.sub("ŽIP0,8Ż", "", s)
    s = re.sub("ŽIP0DI,15DIŻ", "", s)
    s = re.sub("®IP0DI,15DI¯", "", s)
    s = re.sub("®IP0,16¯:", "", s)
    s = re.sub("@оIP0,16п", "", s)
    s = re.sub("оIP0,16п", "", s)
    s = re.sub("@оIP0,8п", "", s)

    # Removes trash lines like "~" or "~"
    s = re.sub("^_$", "", s)
    s = re.sub("^\.$", "", s)
    s = re.sub("^~$", "", s)
    s = re.sub("^%$", "", s)
    s = re.sub("^\*$", "", s)

    # Removes empty utterances of "LIZ" and "DAI"
    s = re.sub("^\*LIZ:$", "", s)
    s = re.sub("^\*DAI:$", "", s)

    # Simple character cleaning
    s = re.sub("^%rr:$", "%err:", s)
    s = re.sub("^%it:$", "%sit:", s)
    s = re.sub("^sit:$", "%sit:", s)
    s = re.sub("@tim:", "%tim:", s) 
    s = re.sub("^v%tim:\s", "%tim:\t", s)
    s = re.sub("^xxx:\s", "%tim:\t", s)
    s = re.sub("^\|%mor:\s", "%mor:\t", s)


    s = re.sub("~~~%sit", "\n%sit", s)
    s = re.sub("~", "", s)




    # Puts a space before "!", "?" or "."
    # If the utterance ends with, e.g., "+." or "+/?", it will break
    #s = re.sub("(\S)([!\?\.])$", "\\1 \\2", s)

    # Removes "," or "." that occur after non-final characters
    #s = re.sub("(\S)[,\.]", "\\1", s)

    # Removes "--"
    s = re.sub("\-\-", "", s)

    # Removes empty dependent tiers.
    s = re.sub("^%.{3,4}:$", "", s)

    # Starts continuation lines with "\t"
    s = re.sub("\n ", "\n\t", s, re.M)

    # Removes tabs in the middle of the lines
    # (Couldn't find a way to do this with only one string)
    l = s.split('\t', 1)
    if (len(l) == 2):
        s2 = re.sub("\s+", " ", l[1])
        s = l[0] + '\t' + s2

    # Replace morphosyntactic annotation by xmor, xcod etc.
    s = re.sub("^%(mor|arg|cod|snd):", "%x\\1:", s)

    # Delete single "#" on any tier (they probably mark some break)
    #s = re.sub("\\s*#\\s*", " ", s)


    if s.startswith("*") or s.startswith("%eng"):
        s = clean_main_line(s)


    # There are two more cases for the removal of "#":
    # 1) When it appears as [#], remove the three characters
    # 2) Else, just remove it
    s = re.sub("\\s*\[#\]\\s*", " ", s)
    s = re.sub("\\s*#\\s*", " ", s)

    # If we ended up putting a space after tier name, removes it
    s = re.sub("(^\*[A-Z0-9]{3}:)(\s+)", r"\1\t", s)
    s = re.sub("(^\%[a-z0-9]{3}:)(\s+)", r"\1\t", s)

    # Puts a tab after tier name (shouldn't be necessary at this point)
    # (some tiers names have more than only 3 or 4 letters)
    s = re.sub(":\s+", ":\t", s, 1)


    if s.startswith("%sit"):
        # Suppresses parenthesis in situation -- CHAT thinks it is a symbol
        s = re.sub('\t\((.*)\)', '\t\\1', s)
        s = re.sub(' \((.*)\)', ' \\1', s)
        s = re.sub('&', 'and', s)
        s = re.sub('-', 'and', s)

    if s.startswith("%err"):
        s = re.sub('-', 'and', s)
        s = re.sub('/', 'and', s)
        s = re.sub('=(\w)', '= \\1', s)

    if s.startswith("%tim"):
        s = re.sub('-', 'and', s)


    if s.startswith("%add"):
        s = re.sub("\*", "", s)
        s = re.sub("([A-Z]{3})(,)([A-Z]{3})", "\\1\\2 \\3", s)

    return s

