# ACQDIV
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3558643.svg)](https://doi.org/10.5281/zenodo.3558643)
![PyPI](https://img.shields.io/pypi/v/acqdiv)

[![CircleCI](https://circleci.com/gh/acqdiv/acqdiv.svg?style=svg)](https://circleci.com/gh/acqdiv/acqdiv)

This repository contains the code and configuration files for transforming 
the child language acquisition corpora into the ACQDIV database.

## Resources

Download the ACQDIV database (only public corpora):

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3558641.svg)](https://doi.org/10.5281/zenodo.3558641)

To request access to the full database including the private corpora (for
research purposes only!), 
please refer to 
[Sabine Stoll](https://www.psycholinguistics.uzh.ch/en/stoll.html).
In case of technical questions, please open an issue on this repository.

--------------

## Corpora

Our full database consists of the following corpora:

| Corpus                                                                                                                    | ISO | Public | # Words   | 
|---------------------------------------------------------------------------------------------------------------------------|:---:|:------:|---------:| 
| Chintang Language Corpus                                                                                                  | ctn | no     | 987'673   | 
| [Cree Child Language Acquisition Study (CCLAS) Corpus](https://phonbank.talkbank.org/access/Other/Cree/CCLAS.html)        | cre | yes    | 44'751    | 
| [English Manchester Corpus](https://childes.talkbank.org/access/Eng-UK/Manchester.html)                                   | eng | yes    | 2'016'043  | 
| [MPI-EVA Jakarta Child Language Database](https://archive.mpi.nl/islandora/object/lat%253A1839_00_0000_0000_0022_6164_B)  | ind | yes    | 2'489'329  | 
| Allen Inuktitut Child Language Corpus                                                                                     | ike | no     | 71'191    | 
| [MiiPro Japanese Corpus](https://childes.talkbank.org/access/Japanese/MiiPro.html)                                        | jpn | yes    | 1'011'670  | 
| [Miyata Japanese Corpus](https://childes.talkbank.org/access/Japanese/Miyata.html)                                        | jpn | yes    | 373'021   | 
| Ku Waru Child Language Socialization Study                                                                                | mux | yes    | 65'723    | 
| [Sarvasy Nungon Corpus](https://childes.talkbank.org/access/Other/Nungon/Sarvasy.html)                                    | yuw | yes    | 19'659    | 
| Qaqet Child Language Documentation                                                                                        | byx | no     | 56'239    | 
| Stoll Russian Corpus                                                                                                      | rus | no     | 2'029'704  | 
| [Demuth Sesotho Corpus](https://childes.talkbank.org/access/Other/Sesotho/Demuth.html)                                    | sot | yes    | 177'963   | 
| Tuatschin Corpus                                                                                                          | roh | no     | 118'310   | 
| Koç University Longitudinal Language Development Database                                                                 | tur | no     | 1'120'077  | 
| Pfeiler Yucatec Child Language Corpus                                                                                     | yua | no     | 262'382   | 
| **Total**                                                                                                                 |     |        | **10'843'735** |

--------------

## Running the pipeline

To run the pipeline yourself:

### Install the package

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
git clone git@github.com:acqdiv/acqdiv.git
cd acqdiv

# Install package (for users!)
pip install .

# Developer mode (for developers!)
pip install -r requirements.txt
```

### Download the corpora

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

### Create the database

Get the configuration file `src/acqdiv/config.ini` and specify the absolute
paths (without trailing slashes) for the corpora directory (`corpora_dir`) and 
the directory where the database should be written to (`db_dir`):
```ini
[.global]
# directory containing corpora
corpora_dir = /absolute/path/to/corpora/dir
# directory where the database is written to
db_dir = /absolute/path/to/database/dir
...
```

Run the pipeline specifying the absolute path to the configuration file:  
`acqdiv load -c /absolute/path/to/config.ini`

Run the unittests:  
`pytest tests/unittests`  

Run the integrity tests on the database:  
`pytest tests/systemtests`
