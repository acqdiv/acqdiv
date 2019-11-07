# Inclusion of a CHAT corpus

## Preparation

### Create ini
* Create a an ini file: `src/acqdiv/ini/<corpus_name>.ini`
* Copy the following into the ini file and fill in all `xxx`:

```
[corpus]
iso639-3 == xxx
glottolog_code == xxx
format == cha
language == xxx
corpus == xxx
owner == xxx
acronym == xxx
name == xxx

[paths]
path == corpora
sessions == ${path}/${corpus:corpus}/${corpus:format}/*.xxx
sessions_dir == ${path}/${corpus:corpus}/${corpus:format}/
metadata_dir == ${path}/${corpus:corpus}/${metadata:type}/

[metadata]
type == cha
```

## Coding

### Parser

First, create a new Python package:
`src/acqdiv/parsers/corpora/main/<corpus_name>`. Then, create the following 
classes:

* Reader class:
    * Create a class called `<corpus_name>Reader` in a file named 
    `reader.py` in the package.
    * Make it inherit from the class `acqdiv.parsers.chat.readers.reader.CHATReader`
    * Make sure every method of `CHATReader` has a correct implementation, 
    otherwise override the method
* Cleaner class:
    * Create a class called `<corpus_name>Cleaner` in a file named 
    `cleaner.py` in the package
    * Make it inherit from the class `acqdiv.parsers.chat.cleaners.cleaner.CHATCleaner`
    * Make sure every method of `CHATCleaner` has a correct implementation,
    otherwise override the method.
* Session parser class:
    * Create a class called `<corpus_name>SessionParser` in a file named
    `session_parser.py` in the package
    * Make it inherit from the class `acqdiv.parsers.chat.parser.CHATParser`
    * Override the methods `get_reader()` and `get_cleaner()` to return 
    an instance of the newly implemented reader and cleaner class, respectively
* Corpus parser class:
    * Create a class called `<corpus_name>CorpusParser` in a file named
    `corpus_parser.py` in the package
    * Make it inherit from the class `acqdiv.parsers.corpus_parser.CorpusParser`
    * Implement the method `get_session_parser()` to return an instance of 
    the newly implemented session parser class.
    
### Mapper
Add a mapping of the corpus name to the newly implemented corpus parser in
the `mappings` dictionary of the class `CorpusParserMapper` of the 
module `acqdiv.parsers.corpus_parser_mapper.CorpusParserMapper`.

### Loader

Add the ini file to the `configs` list in the method `load()` of the module
`acqdiv.loader`.
