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

## Usage

```python
from wiki_xml_parser.parser import XmlParser

# Create a parser object
x_parser = XmlParser()

# Parse the corpus at `input_file` file path 
# and store the results at folder 'output_dir'
x_parser.parse_corpus(input_file, output_dir)
```