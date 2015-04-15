import collections

# class for dictionaries with autovivification
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value



# correspondences between XML standard dependent tiers (shared across corpora) and JSON
xml_dep_correspondences = {
    'actions' : 'comments',
    'addressee' : 'addressee',
    'arg' : 'argument structure', 
    'comments' : 'comments',
    'english translation' : 'english',
    'errcoding' : 'error_coding',
    'explanation' : 'comments',
    'gesture' : 'gestures',
    'orthography' : 'orthographic',
    'situation' : 'comments',
    'time stamp' : 'starts_at'
}

# correspondences between XML extended dependent tiers and JSON
xml_ext_correspondences = {
    'pho' : 'phonetic',
    'arg' : 'argument_coding'
}
# correspondences between other XML elements and JSON
xml_other_correspondences = {
    'actmor' : 'segments',
    'actual' : 'phonetic',
    'model' : 'phonetic_target',
    'mormea' : 'glosses_target',
    'mortyp' : 'pos_target',
    'tarmor' : 'segments_target'
}

# correspondences between values of XML <t> (= sentence type) and JSON
t_correspondences = {
    'p' : 'default', # CHAT .
    '.' : 'default',
    'q' : 'question', # CHAT ?
    '?' : 'question', 
    'e' : 'exclamation', # CHAT !
    '!' : 'exclamation',
 	'trail off' : 'trail off', # CHAT +...
 	'interruption' : 'interruption', # CHAT +/.
 	'self interruption' : 'self interruption', # CHAT +//.
 	'quotation precedes' : 'quotation precedes', # CHAT +".
 	'quotation next line' : 'quotation next line', # CHAT +"/.
 	'interruption question' : 'interruption question', # CHAT +/?
    'broken for coding' : 'default' # Inuktitut corpus only, = not glossed
}

# correspondences between Toolbox utterance-level tiers and JSON
# a simple dictionary isn't enough here because the meaning of tiers changes according to the corpus
tbx_utt_tier_correspondences = Vividict()
tbx_utt_tier_correspondences['Chintang']['comm'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['Comment'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['comment'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['context'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['cxt'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['ELANBegin'] = 'starts_at'
tbx_utt_tier_correspondences['Chintang']['ELANEnd'] = 'ends_at'
tbx_utt_tier_correspondences['Chintang']['ELANParticipant'] = 'speaker_id'
tbx_utt_tier_correspondences['Chintang']['eng'] = 'english'
tbx_utt_tier_correspondences['Chintang']['eth'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['EUDICOp'] = 'speaker_id'
tbx_utt_tier_correspondences['Chintang']['EUDICOt0'] = 'starts_at'
tbx_utt_tier_correspondences['Chintang']['EUDICOt1'] = 'ends_at'
tbx_utt_tier_correspondences['Chintang']['gram'] = 'comments'
tbx_utt_tier_correspondences['Chintang']['nep'] = 'nepali'
tbx_utt_tier_correspondences['Chintang']['tx'] = 'phonetic'
tbx_utt_tier_correspondences['Indonesian']['begin'] = 'starts_at'
tbx_utt_tier_correspondences['Indonesian']['ft'] = 'english'
tbx_utt_tier_correspondences['Indonesian']['nt'] = 'comments'
tbx_utt_tier_correspondences['Indonesian']['pho'] = 'phonetic'
tbx_utt_tier_correspondences['Indonesian']['sp'] = 'speaker_id'
tbx_utt_tier_correspondences['Russian']['act'] = 'comments'
tbx_utt_tier_correspondences['Russian']['add'] = 'addressee'
tbx_utt_tier_correspondences['Russian']['com'] = 'comments'
tbx_utt_tier_correspondences['Russian']['ct'] = 'comments'
tbx_utt_tier_correspondences['Russian']['ELANBegin'] = 'starts_at'
tbx_utt_tier_correspondences['Russian']['ELANEnd'] = 'ends_at'
tbx_utt_tier_correspondences['Russian']['ERR'] = 'comments'
tbx_utt_tier_correspondences['Russian']['err'] = 'comments'
tbx_utt_tier_correspondences['Russian']['EUDICOp'] = 'speaker_id'
tbx_utt_tier_correspondences['Russian']['ph'] = 'phonetic'
tbx_utt_tier_correspondences['Russian']['PHO'] = 'phonetic'
tbx_utt_tier_correspondences['Russian']['pho'] = 'phonetic'
tbx_utt_tier_correspondences['Russian']['sit'] = 'comments'

# correspondences between Toolbox word-level tiers and JSON
tbx_word_tier_correspondences = Vividict()
tbx_word_tier_correspondences['Chintang']['gw'] = 'full_word'
tbx_word_tier_correspondences['Indonesian']['tx'] = 'full_word'
tbx_word_tier_correspondences['Russian']['text'] = 'full_word'

# correspondences between Toolbox morpheme-level tiers and JSON
tbx_mor_tier_correspondences = Vividict()
tbx_mor_tier_correspondences['Chintang']['mgl'] = 'glosses_target'
tbx_mor_tier_correspondences['Chintang']['mph'] = 'segments_target'
tbx_mor_tier_correspondences['Chintang']['ps'] = 'pos_target'
tbx_mor_tier_correspondences['Indonesian']['ge'] = 'glosses_target'
tbx_mor_tier_correspondences['Indonesian']['mb'] = 'segments_target'
tbx_mor_tier_correspondences['Russian']['lem'] = 'segments' # Actually there are no segmentations in the Russian corpus, so the levels word and morpheme cannot be separated. However, for consistency across corpora it's best to treat the elements on this tier and on \mor as morphemes (because only morphemes can have glosses). The corresponding "word" tier is \text. 
tbx_mor_tier_correspondences['Russian']['mor'] = 'glosses'
