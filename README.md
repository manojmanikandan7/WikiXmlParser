# Wikipedia XML Parser

A parser that parses the XML exported using the [Wikipedia Export feature](https://en.wikipedia.org/wiki/Special:Export), and breaks down the corpus into smaller XML documents (according to [wikixml.dtd](resources/wikixml.dtd)). 

## Steps taken to build the parser

- Dependencies/Libraries used:
  - Python's builtin `html` library
  - Python's builtin `xml` library
  - Python's builtin `re` library
  - `Beautiful Soup`, via [pip](https://pypi.org/project/beautifulsoup4/)
  - `lxml`, via [pip](https://pypi.org/project/lxml/)

- The module `xml.etree.ElementTree` was primarily used for processing the original XML file and to design the new XML file.
- `html` module, specifically `html.unescape`, was used for unescaping XML tags in the text content.
- `Beautiful Soup` and `lxml` were used for removing the XML tags extracted in the previous step.
- `xml.dom.minidom` was used for including the DOCTYPE and &lt;?xml?&gt; declarations.
- The `re` library was used for regex-based removal of formatting of texts (e.g. {{...}}, [[..]], ''...'').

## Requirements

- Python >= 3.9

## Installation

Currently, this tool can be installed from the source. 

### Using `pip3 install`
First, make sure you have `pip3` installed.

Open a terminal and run the following commands.
```bash
$ python3 -m pip install --upgrade pip
```

Then, run the following command to install the package.
```bash
$ pip3 install "https://github.com/manojmanikandan7/WikiXmlParser/releases/latest/download/wiki_xml_parser-0.0.2-py3-none-any.whl"
```

## Usage

### As a module
```python
from wiki_xml_parser.parser import XmlParser

# Create a parser object
x_parser = XmlParser()

# Parse the corpus at `input_file` file path 
# and store the results at folder 'output_dir'
x_parser.parse_corpus(input_file, output_dir)
```


### As a Command Line Interface (CLI) tool
The CLI can be accessed through the command `wiki_parse`. 

Run the following for more information on the command
```bash
$ wiki_parse --help
```
```
 Usage: wiki_parse [OPTIONS] INPUT_FILE_NAME OUTPUT_DIR CORPUS_NAME                                                                                                                                                              
                                                                                                                                                                                                                                 
 The command-line tool for parsing a Wikipedia-exported XML file to simplified XML files                                                                                                                                         
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                 
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    input_file_name      TEXT  The input file path for the XML file [default: None] [required]                                                                                                                               │
│ *    output_dir           TEXT  The output file directory for the transformed XML files [default: None] [required]                                                                                                            │
│ *    corpus_name          TEXT  The name of this corpus [default: None] [required]                                                                                                                                            │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                                                       │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                                                │
│ --help                        Show this message and exit.                                                                                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
