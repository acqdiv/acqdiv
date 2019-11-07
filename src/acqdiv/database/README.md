Database directory
==================

The result of the ACQDIV ETL pipeline (the sqlite database file) is written to this directory. It is currently transformed with the script `sqla2r.sh` into an `.rda` file by calling:

`sh sqla2r.sh path/to/db`

which calls the helper scripts:

`sqla2csv.py`
`csv2r.R`

and dumps the database tables, combines them into one `all_data` table, and puts the results into a large `.rda` data file.

We are in the process of updating the sqlite-to-R conversion, but note that `sqla2r.sh` makes some assumptions beyond simply joining all the tables at the morpheme level. This issue needs to be revisited when we update the conversion script(s).

For example, these scripts simply dump the database as one large CSV file:

`dump_production.sh`
`dump_test.sh`

But they do not yet stay faithful to the joining mechanism above. This is a work-in-progress.

The script `dbchecks.R` runs data integrity checks on the database. It should be better integrated with tests. TODO.



Database checks
=============== 

general ideas
-------------

* < Damián: count number of NAs per corpus and table, compare to last version

utterances
----------

* ~~fields that can never be NULL: id, session_id_fk, corpus, language, utterance_id, speaker_label, utterance_raw, utterance, sentence_type~~
* ~~possible values for sentence_type: NULL, default, question, exclamation, imperative, action, trail off, interruption, trail off question, self interruption, quotation precedes, interruption question. (The types after "action" are only found in some CHAT corpora and could be normalized at some point. But they're not very frequent, anyways.)~~
* ~~the following fields may be NULL but there must be at least one row in every corpus that's not NULL: word, morpheme, gloss_raw, pos_raw~~

words
-----

* ~~fields that can never be NULL: id, session_id_fk, utterance_id_fk, corpus, language, word~~
* in words_target and words_actual, either one row should contain only NULL, or there should be more than one but less than all rows where word_actual != word_target (i.e. either the distinction is not coded at all in a corpus, or if it is coded, instances can be found where it's been applied)
* word should be something or NULL, plus the following additional rules: 
	* word shouldn't be ^\s*$
	* word should not contain [\'\(\)\*\"\^_\[\]]
	* word should not start with [\-\.̃]
	* word should be "???" or not contain any "?" at all

morphemes
---------

* fields that can never be NULL: type
* ~~possible values for gloss (cf. corpus manual): 0, 1, 2, 3, 4, 4SYL, A, ABIL, ABL, ABS, ACC, ACROSS, ACT, ADESS, ADJ, ADJZ, ADN, ADV, ADVZ, AFF, AGT, AGR, ALL, ALT, AMBUL, ANIM, ANTIP, AOR, APPL, ART, ASP, ASS, ASSOC, ATTN, AUTOBEN, AUX, AV, BABBLE, BEN, CAUS, CHOS, CLF, CLIT, CM, COM, COMP, COMPAR, COMPL, CONC, COND, CONJ, CONJ, CON, CONT, CONTEMP, CONTING, CONTR, COP, CVB, DAT, DECL, DEF, DEICT, DEM, DEP, DEPR, DESID, DESTR, DET, DETR, DIM, DIR, DIR, DIST, DISTR, DOWN, DU, DUB, DUR, DYN, ECHO, EMPH, EQU, ERG, EVID, EXCL, EXCLA, EXIST, EXT, F, FILLER, FOC, FUT, GEN, HAB, HES, HHON, HON, HORT, IDEOPH, IMIT, IMP, IMPERS, INAL, INAN, INCEP, INCH, INCL, INCOMPL, IND, INDF, INDIR, INF, INS, INSIST, INTJ, INTR, INTRG, INV, IPFV, IRR, LNK, LOC, M, MED, MHON, MIR, MOD, MOOD, MV, N, N, N, NAG, NAME, NC, NEG, NICKNAMER, NMLZ, NOM, NPST, NSG, NTVZ, NUM, OBJ, OBJVZ, OBL, OBLIG, OBV, ONOM, OPT, ORD, P, PARTIT, PASS, PEJ, PERL, PERMIS, PERSIST, PFV, PL, POL, POSS, POT, PRAG, PRED, PREDADJ, PREP, PREP, PRF, PRO, PROB, PROG, PROH, PROP, PROX, PRS, PST, PTCL, PTCP, PURP, PV, PVB, Q, QUANT, QUOT, RECENT, RECNF, RECP, REF, REFL, REL, REM, REP, RES, REVERS, S, SBJ, SBJV, SEQ, SG, SIM, SOC, SPEC, STAT, STEM, SUPERL, SURP, TEASER, TEL, TEMP, TENSE, TERM, TOP, TR, UP, V, V2, V.AUX, V.CAUS, V.IMP, V.ITR, V.PASS, V.POS, V.TR, VBZ, VOICE, VN, VOC, VOL, WH, ???~~
* ~~possible values for pos (cf. corpus manual): ADJ, ADV, ART, AUX, CLF, CONJ, IDEOPH, INTJ, N, NUM, pfx, POST, PREP, PRODEM, PTCL, QUANT, sfx, stem, V, ???~~
* ~~the following fields may be NULL but there must be at least one row in every corpus that's not NULL: morpheme, gloss, pos~~

sessions
--------

* ~~fields that can never be NULL: id, session_id, corpus, language, date~~
* date is ^((19|20)\d\d(\-(0[1-9]|1[012])\-([012][1-9]|3[01]))?)$
* every session should have exactly 1 Target_Child (not less, not more)

speakers
--------

* ~~fields that can never be NULL: session_id_fk, uniquespeaker_id_fk, corpus, language, speaker_label, name, macrorole~~
* speaker_label should be [a-zA-Z\d]{2,}
* name can be anything or "Unknown" but not "Unspecified" or "None" (the problem with these values is that they can create additional unique pseudo-speakers)
* age is ^(\d\d?(;([0-9]|1[01])\.([12]?[0-9]|30))?)$ or NULL
* speaker_label and name can't contain numerals
* birthdate is like sessions.date or "Unknown"
* ~~possible values for gender: Female, Male, Unknown~~
* ~~possible values for role: Adult, Aunt, Babysitter, Brother, Caller, Caretaker, Cousin, Daughter, Family_Friend, Father, Friend, Grandfather, Grandmother, Great-Grandmother, Host, Housekeeper, Mother, Neighbour, Niece, Non_Human, Playmate, Research_Team, Sibling, Sister, Sister-in-law, Son, Speaker, Student, Subject, Target_Child, Teacher, Toy, Twin_Brother, Uncle, Unknown, Visitor~~
* ~~possible values for macrorole: Adult, Child, Target_Child, Unknown~~
* ~~the following fields may be NULL but there must be at least one row in every corpus that's not NULL: age, age_in_days, gender, role, macrorole, birthdate~~
* the majority of rows should not have NULL in macrorole. A threshold of 15% should be realistic.

uniquespeakers
--------------

* ~~fields that can never be NULL: id, speaker_label, name, corpus~~
* birthdate is like sessions.date or "Unknown"
* gender is like speakers.gender
* extract list of all speakers where out of {speaker_label, name, birthdate} two are identical. Sort by speaker label and check manually for mistakes (two speakers as one, one speaker as two)

Known issues
------------

* Yucatec always has "???" in words.word_actual. Better NULL (for consistency). 
* utterances.morpheme/gloss_raw/pos_raw are always NULL in Cree, Inuktitut, Japanese_MiiPro, Japanese_Miyata, Sesotho, Turkish_KULLD(D), Yucatec. For Russian, only gloss_raw is always NULL. 
* utterances.word is always NULL in Cree, Indonesian, Russian
* morphemes.word_id_fk is always NULL
* morphemes.pos is always NULL
* Chintang sometimes has outdated language codes in speakers.languages_spoken (x-sil-BAP etc.)
* speakers.birthdate has "Unspecified" and "None" in some cases (Chintang, Russian) -> change to "Unknown"
* speakers that are classified as different but are possibly identical:
        * Russian.TAN (name Tanja/TAN -> typo)
	* Turkish.CA1/CA2/CAM (name Dilara)
	* Turkish.CA2/CAM (name Ece)
	* Turkish.CA1/CAM (name Engin)
	* Turkish.CO1/CO2 (name Ezgi)
	* Turkish.VI1/VI2 (name Gülay)
	* Turkish.AUN/MOT (name Gülcan)
	* Turkish.CA2/CAM (name Petek)
	* Turkish.CA1/CAM (name Sevdil)
	* Turkish.CA2/CAM (name Özlem)
* speakers that are classified as a single speaker but are possibly distinct:
 	* Turkish.CO, GI, VI, CA, CH, BO, GR, MA, FE (distinguished by numbers - how consistent has this been applied?)
	* Turkish.MA(L), FE(M), AUN, GRA, BAB, UNI, ADU, UNC, BOY (not distinguished at all, name and birthdate Unknown)
* funny strings in words.word:
	* Russian #NAME?, #REF, $, %, %act, 
	* Turkish ', lots of .+'.+, 
	* Yucatec '
