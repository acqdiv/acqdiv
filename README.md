# ACQDIV

[![CircleCI](https://circleci.com/gh/uzling/acqdiv/tree/master.svg?style=svg&circle-token=86716ee9ff5bdc399d72a74096ef81ba7be0f9d0)](https://circleci.com/gh/uzling/acqdiv/tree/master)


This repository contains the code and configuration files for transforming 
the child language acquisition corpora into the ACQDIV database.

### Resources

Download the ACQDIV database (only open-source corpora):
* [SQLite]()
* [R object]()

For the complete database, please refer to ...

--------------

### Supported Corpora

We provide parsers (see `acqdiv.parsers.corpora.main`) for the 
following corpora:

* Chintang Language Corpus (Chintang)
* [Cree Child Language Acquisition Study](https://phonbank.talkbank.org/access/Other/Cree/CCLAS.html)
(Cree)
* [Manchester Corpus](https://childes.talkbank.org/access/Eng-UK/Manchester.html) 
(English)
* MPI-EVA Jakarta Child Language Database (Indonesian)
* Allen Inuktitut Child Language Corpus (Inuktitut)
* [Japanese MiiPro](https://childes.talkbank.org/access/Japanese/MiiPro.html) 
(Japanese)
* [Japanese Miyata](https://childes.talkbank.org/access/Japanese/Miyata.html) 
(Japanese)
* [Sarvasy Nungon Corpus](https://childes.talkbank.org/access/Other/Nungon/Sarvasy.html)
(Nungon)
* Qaqet
* Ku Waru
* Stoll Russian Corpus
* [Demuth Corpus](https://childes.talkbank.org/access/Other/Sesotho/Demuth.html)
(Sesotho)
* Tuatschin
* Koç University Longitudinal Language Development Database (Turkish)
* Pfeiler Yucatec Child Language Corpus (Yucatec)

--------------

### Running Pipeline

To run the pipeline yourself:

**Download the corpora:**

For the CHAT corpora, proceed as follows:
* Download the transcripts on the CHILDES TalkBank website (where available)
(see `Download transcripts` link)
* Unzip the data
* Copy the python script `src/acqdiv/util/cha_extractor.py` into the folder
* Run the script: `python cha_extractor.py`. A directory `cha/` will be created.
* Place the `cha/` directory in `src/acqdiv/corpora/<corpus_name>/` (also 
see the corresponding ini file in `src/acqdiv/ini/<corpus_name>` for which
corpus name to use).

For the toolbox corpora, proceed as follows:
* Download the toolbox and IMDI files.
* Place the toolbox files in `src/acqdiv/corpora/Tuatschin/toolbox/`
and the IMDI files in `src/acqdiv/corpora/Tuatschin/imdi/`.

**Create the database:**

First, install the `acqdiv` package, following the instructions in `INSTALL.txt`.

Run the pipeline:  
`acqdiv load -f`

Run the unittests:  
`$ pytest tests/unittests`  

Run the integrity tests on the database:  
`$ pytest tests/systemtests`

For more options:  
`acqdiv load -h`

The database will be created in the directory `acqdiv/database/`.
