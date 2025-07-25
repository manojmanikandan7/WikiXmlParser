"""
The module for parser functions for Wikipedia-exported xml files
"""
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom.minidom import parseString, getDOMImplementation
from bs4 import BeautifulSoup
import html
import re
from rich.progress import track


class XmlParser:
    """
    A class for parsing the XML files
    """
    def __init__(self):
        self.ns = {"default": "http://www.mediawiki.org/xml/export-0.11/"}

    @staticmethod
    def parse_xml(file: Path) -> ET.ElementTree:
        """
        Parse the input XML file and return an `xml.etree.ElementTree.ElementTree` representation of it.
        :param file: The path to the file to parse
        :return: An `xml.etree.ElementTree.ElementTree` object, representing the file contents.
        """
        return ET.parse(file)

    def get_attrs(self, page: ET.Element, corpus_name: str, base_name: str):
        """

        :param base_name: The base_name of the url. (eg. https://en.wikipedia.org/)
        :param corpus_name: The name of the corpus to include in the output file(s)
        :param page: The page element to parse
        :return:
        """
        # Extracting the timestamp
        timestamp = page.find("default:revision", self.ns).find("default:timestamp", self.ns).text

        # The 'filename' is the id of the page.
        filename = page.find("default:id", self.ns).text

        title = page.find("default:title", self.ns).text

        # Identifying if the page is a Talk page
        title_parts = title.split(":")

        title = title_parts[-1]

        # Substituting space characters with underscores, then splitting archive number (if present)
        title_splits = re.sub(r"\s", "_", title).split("/")

        # If colon is present, the page is inferred to be a talk page
        if len(title_parts) > 1:
            corpus_type = "Talk"
            sub = "_Talk"
            pre = title_parts[0] + ":"
        else:
            corpus_type = "Article"
            sub = ""
            pre = ""


        # If forward-slash is not present in the title, it is not an archive (Talk pages only, does not affect Articles).
        if len(title_splits) < 2:
            xml_title = title_splits[0] + sub
            url = f"{base_name}/{pre}{title_splits[0]}"
        else:
            title_name, archive = title_splits
            xml_title = f"{title_name}{sub}_{archive}"
            url = f"{base_name}/{pre}{title_name}/{archive}"


        return {"type": corpus_type, "date": timestamp, "sourceCorpus": corpus_name, "filename": filename, "title": xml_title, "url": url}

    def clean_text(self, txt: str, cards_filter: list[str] = ["infobox","wikiproject", "user", "press", "graph", "image", "reflist", "multiple", "ordered", "list"]):
        """
        Function to clean and extract text from the page content.
        XML/HTML tags, Wikipedia formatting, tables, infoboxes, internal links and media links are all removed.
        If alternative titles are provided for links, they are preserved.
        Note: External/markdown-style links are not removed.

        :param cards_filter:
        :param txt: The input text to clean
        :return: Cleaned text
        """
        ## Text cleaning pipeline ##
        # TODO: Elaborated steps

        # Removing all cards/modals/infoboxes
        info_text = '|'.join(cards_filter)
        no_cards = re.sub(r"(?si){{(#invoke|" + info_text + ")[^}]*?\n.*?\n}}", "", txt)

        # Removing all tables
        no_tables = re.sub(r"(?s){\|.*?\n.*?\n\|}", "", no_cards)

        # Removing Wikipedia formatting patterns

        # no_format_patterns = re.sub("{{[^}]*?data/.*?}}", ";DYN;", no_tables)
        # Note: This should be done before removing tags, since Beautiful Soup looks for curly braces ('{', '}') for namespaces
        no_format_patterns = re.sub("{{.*?}}", "", no_tables)
        no_format_patterns = re.sub("{{", "", no_format_patterns)
        no_format_patterns = re.sub("}}", "", no_format_patterns)

        # Removing internal links formatting

        # Preserving internal links with references in the same article
        no_internal_links = re.sub(r"\[\[([^]:|]*?)]]", r"\1", no_format_patterns)

        # Preserving internal link text with references to other articles
        no_internal_links = re.sub(r"\[\[[^]:]*?\|([^]]*?)]]", r"\1", no_internal_links)

        # Removing special internal links, referring to media or metadata
        no_internal_links = re.sub(r"\[\[User[^]]*:[^]]*?\|([^]]*?)]]", r"\1", no_internal_links)

        # Removing special internal links, referring to media or metadata
        no_internal_links = re.sub(r"\[\[[^]]*?:[^]]*?]]", "", no_internal_links)

        # Removing titles
        no_titles = re.sub(r"\s?==+\s?", "\n", no_internal_links)

        # First, unescape the html special characters (i.e., &..; -> unicode forms)
        unesc_xml = html.unescape(no_titles)

        # Removing the self-closing tags
        unesc_xml = re.sub("<ref [^>]*?/>", "", unesc_xml)

        # Then, remove ref tags using beautiful soup
        # Note: The html parser of lxml is used since xml parsers are strict;
        # They might not allow empty content tags (<...></...>) and prefer self-closing tags(<... />)
        soup = BeautifulSoup(unesc_xml, "lxml")
        refs = soup.find_all("ref")
        galleries = soup.find_all("gallery")
        for ref in refs:
            ref.decompose()  # Remove tag and content
        for gallery in galleries:
            gallery.decompose()  # Remove tag and content
        no_tags = soup.text

        # Removing nbsp
        no_tags = no_tags.replace("\xa0", " ")

        # Remove formatting with double-single quotes (''...'')
        no_format = re.sub("''+", "", no_tags)

        # Remove indent guides
        no_indent = re.sub(r"\n:+", "\n", no_format)

        # Remove leftout infobox/media propertiesk
        no_props = re.sub(r"(^|\n)\s?\|.*", "\n", no_indent)

        return no_props



    def build_tree(self, page: ET.Element, corpus_name: str, base_name: str):
        """

        :param base_name:
        :param page:
        :param corpus_name:
        :return:
        """
        attrs = self.get_attrs(page, corpus_name, base_name)
        file = ET.Element("file", attrs)
        text = ET.SubElement(file, "text")
        segment = ET.SubElement(text, "segment", { "id" : f"id{attrs['filename']}"})
        segment.text = self.clean_text(page.find("default:revision", self.ns).find("default:text", self.ns).text)
        return attrs["title"], file

    def parse_corpus(self, input_file: Path, output_dir: Path, corpus_name: str):
        """

        :param input_file:
        :param output_dir:
        :param corpus_name:
        """
        tree = self.parse_xml(input_file)

        base_name = tree.find("default:siteinfo", self.ns).find("default:base", self.ns).text

        base_name = base_name.rsplit("/", 1)[0]

        pages = tree.findall("default:page", self.ns)

        for page in track(pages, "Processing..."):

            title, file = self.build_tree(page, corpus_name, base_name)

            et_string = ET.tostring(file, encoding="utf-8")

            e_tree = parseString(et_string)

            impl = getDOMImplementation()
            doctype = impl.createDocumentType("file", "", "wikixml.dtd")
            dom_doc = impl.createDocument(None, "xml", doctype)

            dom_doc.replaceChild(e_tree.documentElement, dom_doc.documentElement)

            xml_text = dom_doc.toprettyxml(encoding="utf-8", standalone=False)

            output_dir.mkdir(parents=True, exist_ok=True)

            file_name = output_dir/(title+".xml")
            with open(file_name, 'wb') as f:
                f.write(xml_text)
            print(f"Processed {title}: Saved as {file_name}")
            time.sleep(0.01)