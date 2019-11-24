# ACQDIV

[![CircleCI](https://circleci.com/gh/acqdiv/acqdiv.svg?style=svg)](https://circleci.com/gh/acqdiv/acqdiv)


This repository contains the code and configuration files for transforming 
the child language acquisition corpora into the ACQDIV database.

## Resources

Download the ACQDIV database (only open-access corpora):
* [SQLite]()
* [R object]()

To request access to the full database including the private corpora (for
research purposes only!), 
please refer to 
[Sabine Stoll](https://www.psycholinguistics.uzh.ch/en/stoll.html).
In case of technical questions, please open an issue on this repository.

--------------

## Corpora

Our full database consists of the following corpora 
(open-access corpora are marked with *):

* Chintang Language Corpus (Chintang)
* [Corpus of the Chisasibi Child Language Acquisition Study](https://phonbank.talkbank.org/access/Other/Cree/CCLAS.html)
(Cree) *
* [English Manchester Corpus](https://childes.talkbank.org/access/Eng-UK/Manchester.html) 
(English) *
* [MPI-EVA Jakarta Child Language Database](https://archive.mpi.nl/islandora/object/lat%253A1839_00_0000_0000_0022_6164_B) (Indonesian) *
* Allen Inuktitut Child Language Corpus (Inuktitut)
* [MiiPro Japanese Corpus](https://childes.talkbank.org/access/Japanese/MiiPro.html) 
(Japanese) *
* [Miyata Japanese Corpus](https://childes.talkbank.org/access/Japanese/Miyata.html) 
(Japanese) *
* Ku Waru Child Language Socialization Study (Ku Waru) *
* [Sarvasy Nungon Corpus](https://childes.talkbank.org/access/Other/Nungon/Sarvasy.html)
(Nungon) *
* Qaqet Child Language Documentation (Qaqet)
* Stoll Russian Corpus (Russian)
* [Demuth Sesotho Corpus](https://childes.talkbank.org/access/Other/Sesotho/Demuth.html)
(Sesotho) *
* Tuatschin Corpus (Tuatschin)
* Koç University Longitudinal Language Development Database (Turkish)
* Pfeiler Yucatec Child Language Corpus (Yucatec)

--------------

## Running the pipeline

To run the pipeline yourself:

###Install the package

Create a virtual environment [optional]:

```shell script
python3 -m venv venv
source venv/bin/activate
```

You can install the package from PyPI or directly from source:

**PyPI**

`pip install acqdiv`

**From source**

```shell script
# Clone Repository
git clone git@github.com:uzling/acqdiv.git
cd acqdiv

# Install package (for users!)
pip install .

# Developer mode (for developers!)
pip install -r requirements.txt
```

###Download the corpora

Create a directory `corpora`.

For the CHAT corpora:
* Download the CHAT files on the CHILDES TalkBank website (where available)
(see `Download transcripts` link)
* Unzip the data
* Copy the python script `src/acqdiv/util/cha_extractor.py` into the directory
* Run the script: `python cha_extractor.py`. A directory `cha/` will be created.
* Place the `cha/` directory in `corpora/<corpus_name>/` (also 
see the corresponding ini file in `src/acqdiv/ini/<corpus_name>` for which
corpus name to use as a directory name).

For the toolbox corpora:
* Download the toolbox and metadata files (IMDI/CMDI).
* Place the toolbox files in `corpora/<corpus_name>/toolbox/`
and the IMDI files in `corpora/<corpus_name>/imdi/`.

###Create the database

Get the configuration file `src/config.ini` and specify the
paths for the corpora directory (`corpora_dir`) and 
the directory where the database should be written to (`db_dir`):
```ini
[.global]
# directory containing corpora
corpora_dir = corpora
# directory where the database is written to
db_dir = database
...
```

Run the pipeline specifying the path to the configuration file:  
`acqdiv load -c path/to/config.ini`

Run the unittests:  
`$ pytest tests/unittests`  

Run the integrity tests on the database:  
`$ pytest tests/systemtests`

For more options:  
`acqdiv load -h`
