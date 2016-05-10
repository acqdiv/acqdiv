import json

file_path = "corpora/Japanese_Miyata/json/Japanese_Miyata.json"
with open(file_path) as data_file:
    data = json.load(data_file)

    x = data.keys() # in Py3 returns a dict_keys object, not a list!
    keys = list(x)
    assert(len(keys) == 1), "there is more than one key in the json file"
    key = keys[0] # should only be one top-level key per json file

    print()
    print(data)
    print()


"""
temp = self.file_path.replace(self.config['paths']['sessions_dir'], self.config['paths']['metadata_dir'])
self.metadata_file_path = temp.replace(".json", ".xml")
self.metadata_parser = Chat(self.config, self.metadata_file_path)



# TODO: config session label mapping replacement afterwards
count = 0
for record in self.data[key]:
    count += 1
    print(str(count))
    utterance = {}
    words = []
    morphemes = []

    # words_to_utterance = [] # TODO
    # MyStruct = namedtuple('MyStruct', 'utterance, words, morphemes')

    # take only valid json with us for utterance
    for k, v in record.items():
        if k in self.config['json_mappings']:
            utterance[self.config['json_mappings'][k]] = v.strip()

    if 'words' in record: # and not len(record['words']) == 0:
        for w in record['words']:
            print('w is', w)
            for w_key in w:
                print('word key is', w_key)
            if 'morphemes' in w.keys():
                for morpheme_set in w['morphemes']:
                    print('morpheme set is', w['morphemes'])
                    for m_key in w['morphemes']:
                        print('morpheme key is', m_key)


            # for m in record['words']['morphemes']:
            #    print('!!!!!!!!!!!!!!!!!!!!!', m)
        # for word in record['words']:
        #    if len(word) > 0:
        #        words.append(word)

    for word in words:
        if 'morphemes' in word:
            morphemes.append("!")
            word_keys = list(word.keys())
            for word_key in word_keys:
                print(word_key)
                # Deal with the embedded morphemes
                if word_key == 'morphemes':
                    temp = word['morphemes'].copy()
                    morphemes.append(temp)
                # Clean up the words dict
                if not word_key in self.config['json_mappings']:
                    del word[word_key]
                else:
                    word[self.config['json_mappings'][word_key]] = word.pop(word_key).strip()

            # Deal with Robert's empty {}s
            if len(word) > 0:
                words.append(word)
    utterance_keys = list(utterance.keys())
    for k in utterance_keys:
        if not k in self.config['json_mappings']:
            del utterance[k]
        else:
            utterance[self.config['json_mappings'][k]] = utterance.pop(k).strip()

    #for morpheme in morphemes:
    #    print(morpheme)
        # morpheme_keys = list(morpheme.keys())
        # Clean up the morphemes dict
        for morpheme_key in morpheme_keys:
            if not morpheme_key in self.config['json_mappings']:
                del morpheme[morpheme_key]
            else:
                morpheme[self.config['json_mappings'][morpheme_key]] = morpheme.pop(morpheme_key).strip()
        morphemes.append(morpheme)

    yield utterance, words, morphemes
"""
