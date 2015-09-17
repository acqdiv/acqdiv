""" THIS IS A TEST VERSION; NOT CURRENTLY USED IN THE DB PIPELINE

Incorporate Robert's corpus-specific inferences
"""

# TODO: After the word level stuff in Toolbox has been split
#  apply the corpus-specifc rules to utterances:

# https://github.com/uzling/acqdiv/blob/master/extraction/parsing/corpus_parser_functions.py#L1718-L1858

def align_morphemes(words):
    # seems like he wants a list of words pass in here
    # then apply the logic and return an aligned list of morphemes

if corpus_name in ['Chintang', 'Indonesian']:
    for tier in tbx_mor_tier_correspondences[corpus_name].keys():
        tier_name_JSON = tbx_mor_tier_correspondences[corpus_name][tier]
        if tier in record.keys():
            word_index = 0
            morphemes = re.split('\\s+', record[tier])
            word_might_end_here = False

            # corpus[text_id][utterance_index]['words'][word_index]['morphemes'] is a list of morphemes; initial index is 0
            if not corpus[text_id][utterance_index]['words'][word_index]['morphemes']:
                corpus[text_id][utterance_index]['words'][word_index]['morphemes'] = []
            morpheme_index = 0

            for m in morphemes:
                print("m:", m)
                # prefix
                if re.search('.\-$', m):
                    # if last morpheme was stem or suffix, start a new word
                    if word_might_end_here == True:
                        # count up word index, extend list if necessary
                        word_index = list_index_up(word_index, corpus[text_id][utterance_index]['words'])
                        if not corpus[text_id][utterance_index]['words'][word_index]['morphemes']:
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'] = []
                        morpheme_index = 0
                    # add morpheme to corpus dic, overwriting existing POS. Indonesian doesn't have POS, so keep separator!
                    ext_vivi(morpheme_index, corpus[text_id][utterance_index]['words'][word_index]['morphemes'])
                    if corpus_name == 'Chintang':
                        m = re.sub('\-', '', m)
                    if tier_name_JSON in ['pos', 'pos_target']:
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index][tier_name_JSON] = 'pfx'
                    else:
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index][tier_name_JSON] = m
                    # count up morpheme index
                    morpheme_index += 1
                    # set terminator flag
                    word_might_end_here = False

                # stem
                elif not re.search('^\-|\-$', m):
                    # if last morpheme was stem or suffix, start a new word
                    if word_might_end_here == True:
                        # count up word index, extend list if necessary
                        word_index = list_index_up(word_index, corpus[text_id][utterance_index]['words'])
                        if not corpus[text_id][utterance_index]['words'][word_index]['morphemes']:
                            corpus[text_id][utterance_index]['words'][word_index]['morphemes'] = []
                        morpheme_index = 0
                    # add morpheme to corpus dic
                    ext_vivi(morpheme_index, corpus[text_id][utterance_index]['words'][word_index]['morphemes'])
                    corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index][tier_name_JSON] = m
                    # count up morpheme index
                    morpheme_index += 1
                    # set terminator flag
                    word_might_end_here = True

                # suffix
                elif re.search('^\-.', m):
                    # add morpheme to corpus dic, overwriting existing POS. Indonesian doesn't have POS, so keep separator!
                    ext_vivi(morpheme_index, corpus[text_id][utterance_index]['words'][word_index]['morphemes'])
                    if corpus_name == 'Chintang':
                        m = re.sub('\-', '', m)
                    if tier_name_JSON in ['pos', 'pos_target']:
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index][tier_name_JSON] = 'sfx'
                    else:
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][morpheme_index][tier_name_JSON] = m
                    # count up morpheme index
                    morpheme_index += 1
                    # set terminator flag
                    word_might_end_here = True

                # floating hyphen (single hyphen before word-medial prefixes and stems)
                elif m == '-':
                    # set terminator flag, do nothing else
                    word_might_end_here = False

        # Russian (no segmentations!) is dealt with differently; \text is used for the word tier while \lem and \mor go to pseud-morpheme tiers (only ever 1 morpheme per word, so morpheme_index is always 0)
# EOF Chintang/Indonesian morpheme tiers

elif corpus_name is 'Russian':
    # TODO Russian has clitics, marked by the separator ~

    for tier in tbx_mor_tier_correspondences[corpus_name].keys():
        tier_name_JSON = tbx_mor_tier_correspondences[corpus_name][tier]
        if tier in record.keys():

            # remove any trailing spaces to make split work correctly
            record[tier] = re.sub('^\\s+|\\s+$', '', record[tier])

            morphemes = re.split('\\s+', record[tier])
            word_index = -1
            # corpus[text_id][utterance_index]['words'][word_index]['morphemes'] is a list of morphemes; initial index is 0
            if not corpus[text_id][utterance_index]['words'][word_index]['morphemes']:
                corpus[text_id][utterance_index]['words'][word_index]['morphemes'] = []

            for m in morphemes:

                # ignore punctuation
                if re.search('^([\.,;!:\"\+\-\/]+|\?)$|PUNCT|ANNOT', m):
                    continue
                # count up word index, extend list if necessary
                else:
                    word_index = list_index_up(word_index, corpus[text_id][utterance_index]['words'])
                    if not corpus[text_id][utterance_index]['words'][word_index]['morphemes']:
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'] = []

                # tier \lem contains lemmas - take every lemma as the first morpheme of the corresponding word
                if tier is 'lem':
                    ext_vivi(0, corpus[text_id][utterance_index]['words'][word_index]['morphemes'])
                    corpus[text_id][utterance_index]['words'][word_index]['morphemes'][0][tier_name_JSON] = m
                # tier \mor may contain POS and glosses - split and assign
                elif tier is 'mor':
                    # first check if there are both POS and glosses. "-" separates subPOS, ":" separates different glosses
                    match_pos_or_gloss = re.search(':', m)
                    if match_pos_or_gloss is not None:
                        # in the case of verbs and adjectives, the cutoff point between POS and glosses is the first "-", e.g. V-PST:SG:F:IRREFL:IPFV -> POS V, gloss PST.SG.F.IRREFL.IPFV
                        match_pos_exceptions = re.search('^(V|ADJ)\-(.*)', m)
                        if match_pos_exceptions is not None:
                            pos = match_pos_exceptions.group(1)
                            gloss = match_pos_exceptions.group(2)
                        # in all other cases, the cutoff point is the first ":", e.g. PRO-DEM-NOUN:NOM:SG -> POS PRO.DEM.NOUN, gloss NOM.SG
                        else:
                            match_pos_and_gloss = re.search('^(.*?):(.*)', m)
                            pos = match_pos_and_gloss.group(1)
                            gloss = match_pos_and_gloss.group(2)
                        pos = re.sub('\-', '.', pos)
                        gloss = re.sub(':', '.', gloss)
                        ext_vivi(0, corpus[text_id][utterance_index]['words'][word_index]['morphemes'])
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][0][tier_name_JSON] = gloss
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][0]['pos_target'] = pos

                    # if there is no ":", POS and gloss are identical (e.g. for particles PCL)
                    else:
                        ext_vivi(0, corpus[text_id][utterance_index]['words'][word_index]['morphemes'])
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][0][tier_name_JSON] = m
                        corpus[text_id][utterance_index]['words'][word_index]['morphemes'][0]['pos_target'] = m

            # EOF word/morpheme loop
