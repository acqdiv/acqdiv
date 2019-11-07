# Inclusion of a Toolbox corpus

## Preparation

### Create ini
* Create an INI file: `src/acqdiv/ini/<corpus_name>.ini`
* Copy the following into the ini file and fill in all `xxx`:

```
[corpus]
iso639-3 == xxx
glottolog_code == xxx
format == toolbox
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
type == xxx
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
    `acqdiv.parsers.toolbox.readers.reader.ToolboxReader`
    * Make sure every method of `ToolboxReader` has a correct implementation, 
    otherwise override the method
* Session parser class:
    * Create a class called `<corpus_name>SessionParser` in a file named
    `session_parser.py` in the package
    * Make it inherit from the class `acqdiv.parsers.toolbox.parser.ToolboxParser`
    * Override the methods `get_record_reader()` and `get_metadata_reader()` to
     return an instance of the newly implemented reader class and an instance
     of some metadata reader (see `acqdiv.parsers.metadata` package)
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