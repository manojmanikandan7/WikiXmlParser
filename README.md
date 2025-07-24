# Wikipedia XML Parser

A parser that parses the XML exported using the [Wikipedia Export feature](https://en.wikipedia.org/wiki/Special:Export), and breaks down the corpus into smaller XML documents (according to [wikixml.dtd](resources/wikixml.dtd)). 

## Steps taken to build the parser

- Dependencies/Libraries used:
  - Python's builtin `html` library
  - Python's builtin `xml` library
  - Python's builtin `re` library
  - `Beautiful Soup`, via [pypi](https://pypi.org/project/beautifulsoup4/)
  - `lxml`, via [pypi](https://pypi.org/project/lxml/)
  - `typer`, via [pypi](https://pypi.org/project/typer/)
  - `typing_extensions`, via [pypi](https://pypi.org/project/typing-extensions/)
  - `rich`, via [pypi](https://pypi.org/project/rich/)

- The module `xml.etree.ElementTree` was primarily used for processing the original XML file and to design the new XML file.
- `html` module, specifically `html.unescape`, was used for unescaping XML tags in the text content.
- `Beautiful Soup` and `lxml` were used for removing the XML tags extracted in the previous step.
- `xml.dom.minidom` was used for including the DOCTYPE and &lt;?xml?&gt; declarations.
- The `re` library was used for regex-based removal of formatting of texts (e.g. {{...}}, [[..]], ''...'').
- The `typer` library was used for creating the `wiki-parse` Command-line Interface (CLI).
- The `typing_extensions` module was a dependency for `typer`, to provide descriptions.
- The `rich` library was used for formatting outputs in the terminal.

## Requirements

- Python >= 3.9

## Installation

This tool can be installed from the [testpypi](https://test.pypi.org) repository, the test version of the [Python Package Index (PyPi)](https://pypi.org).

### Using `pip`
First, make sure you have `pip` installed.

Open a terminal window and run the following commands.

#### On Linux/Unix based systems
```bash
python3 -m pip install --upgrade pip
```

#### On Windows
```bash
python -m pip install --upgrade pip
```
> [!TIP]
> If you are comfortable creating virtual environments, please do so before installing the tool.
> (Refer to: https://docs.python.org/3/library/venv.html#how-venvs-work)
> 
> **Creating a virtual environment**
> ```bash
> python3 -m venv path/to/venv/environment
> ```
> or 
> ```
> python -m venv path/to/venv/environment
> ```
>
> **Activating the virtual environment**
> 
> On Linux/Unix based systems:
> ```bash
> source path/to/venv/environment/bin/activate
> ```
> 
> On Windows:
> ```
> # In cmd.exe
> path\to\venv\environment\Scripts\activate.bat
> # In PowerShell
> path\to\venv\environment\Scripts\Activate.ps1
> ```
  
Then, run the following command to install the package.

#### On Linux/Unix based systems
```bash
python3 -m pip install -i https://test.pypi.org/simple/ wikipedia-xml-parser
```

#### On Windows 
```
python -m pip install -i https://test.pypi.org/simple/ wikipedia-xml-parser
```
## Usage

### As a module
```python
from wikipedia_xml_parser.parser import XmlParser

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
wiki_parse --help
```
Which should print the usage instructions
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
