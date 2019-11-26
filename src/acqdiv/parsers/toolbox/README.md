# Inclusion of a Toolbox corpus

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
sessions = ${.global:corpora_dir}/xxx/toolbox/*.xxx
metadata_dir = ${.global:corpora_dir}/xxx/imdi/
```

## Coding

### Parser
First, create a new Python package:
`src/acqdiv/parsers/corpora/main/<corpus_name>`. Then, create the following 
classes:

* Reader class:
    * Create a class called `<corpus_name>Reader` in a file named 
    `reader.py` in the package.
    * Make it inherit from the class 
    `acqdiv.parsers.toolbox.readers.reader.ToolboxReader`.
    * Make sure every method of `ToolboxReader` has a correct implementation, 
    otherwise override the method.
* Cleaner class:
    * Create a class called `<corpus_name>Cleaner` in a file named 
    `cleaner.py` in the package.
    * Make it inherit from the class 
    `acqdiv.parsers.toolbox.cleaners.cleaner.ToolboxCleaner`.
    * Make sure every method of `ToolboxCleaner` has a correct implementation, 
    otherwise override the method.
* Session parser class:
    * Create a class called `<corpus_name>SessionParser` in a file named
    `session_parser.py` in the package.
    * Make it inherit from the class `acqdiv.parsers.toolbox.parser.ToolboxParser`.
    * Override the methods `get_record_reader()`, `get_metadata_reader()` and
     `get_cleaner()` to return an instance of the newly implemented reader class, 
     an instance of some metadata reader (see `acqdiv.parsers.metadata` package)
     and an instance of the newly implemented cleaner class, respectively.
* Corpus parser class:
    * Create a class called `<corpus_name>CorpusParser` in a file named
    `corpus_parser.py` in the package.
    * Make it inherit from the class `acqdiv.parsers.corpus_parser.CorpusParser`
    * Implement the method `get_session_parser()` to return an instance of 
    the newly implemented session parser class.

### Mapper
Add a mapping of the corpus name to the newly implemented corpus parser in
the `mappings` dictionary of the class `CorpusParserMapper` of the 
module `acqdiv.parsers.corpus_parser_mapper.CorpusParserMapper`.
