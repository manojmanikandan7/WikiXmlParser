"""
The module for parser functions for Wikipedia-exported xml files
"""
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom.minidom import parseString, getDOMImplementation
from rich.progress import track

from .clean_text import clean_text


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

        :param base_name: The base_name of the url. (e.g. https://en.wikipedia.org/)
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
            pre = title_parts[0].replace(" ", "_") + ":"
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

    def build_tree(self, page: ET.Element, corpus_name: str, base_name: str) -> tuple[str, ET.Element]:
        """
        Function to build the new XML tree

        :param base_name: The base name of the url
        :param page: The object representing the current page
        :param corpus_name: Name of the corpus to include in the new XML file
        :return: A tuple, containing the title of page and the root of the new XML tree
        """
        attrs = self.get_attrs(page, corpus_name, base_name)
        file = ET.Element("file", attrs)
        text = ET.SubElement(file, "text")
        segment = ET.SubElement(text, "segment", { "id" : f"id{attrs['filename']}"})
        segment.text = clean_text(page.find("default:revision", self.ns).find("default:text", self.ns).text)
        return attrs["title"], file

    def parse_corpus(self, input_file: Path, output_dir: Path, corpus_name: str):
        """
        Function to parse a Wikipedia-exported XML file, extract information and segregate the pages into separate XML files.

        :param input_file: The path to Wikipedia-exported XML file to process
        :param output_dir: The path to the directory to dump the segregated XML files
        :param corpus_name: The name of the corpus to include in the processed the XML files
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