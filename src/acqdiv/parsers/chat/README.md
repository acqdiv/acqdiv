# Inclusion of a CHAT corpus

## Preparation

### Create ini
Add a section to `src/acqdiv/config.ini` and fill in all `xxx`:

```ini
[xxx]
iso639-3 = xxx
glottolog_code = xxx
language = xxx
corpus = xxx
owner = xxx
acronym = xxx
name = xxx
sessions = ${.global:corpora_dir}/xxx/cha/*.cha
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
