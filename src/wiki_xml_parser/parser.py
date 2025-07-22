"""
The module for parser functions for Wikipedia-exported xml files
"""

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString, getDOMImplementation
from bs4 import BeautifulSoup
import html
from os import PathLike
import re

class XmlParser:
    """
    A class for parsing the XML files
    """
    def __init__(self):
        self.ns = {"default": "http://www.mediawiki.org/xml/export-0.11/"}

    @staticmethod
    def parse_xml(file: PathLike[str]) -> ET.ElementTree:
        """
        Parse the input XML file and return an `xml.etree.ElementTree.ElementTree` representation of it.
        :param file:
        :return:
        """
        return ET.parse(file)

    def get_attrs(self, page: ET.Element, corpus_name: str):
        """

        :param corpus_name:
        :param page:
        :return:
        """
        timestamp = page.find("default:revision", self.ns).find("default:timestamp", self.ns).text
        filename = page.find("default:id", self.ns).text

        title = page.find("default:title", self.ns).text
        _, title = title.split(":")
        title_splits = re.sub(r"\s", "_", title).split("/")

        # In this case, the page is not an archive
        if len(title_splits) < 2:
            xml_title = title_splits[0]
            url = "https://en.wikipedia.org/wiki/Wikipedia_Talk:" + title_splits[0]
        else:
            title_name, archive = title_splits
            xml_title = f"{title_name}_Talk_{archive}"
            url = "https://en.wikipedia.org/wiki/Wikipedia_Talk:" + title_name + '/' + archive



        return {"type": "Talk", "date": timestamp, "sourceCorpus": corpus_name, "filename": filename, "title": xml_title, "url": url}

    def clean_text(self, txt: str):
        """

        :param txt:
        :return:
        """
        # Removing title formatting
        # This should be done before removing tags, since Beautiful Soup looks for curly braces ('{', '}') for namespaces
        no_titles = re.sub("{{.*}}", "", txt)
        no_titles = re.sub(r"[\[.*\]]", "", no_titles)
        no_titles = re.sub("==+", "", no_titles)

        # First, unescape the html special characters (i.e., &..; -> unicode forms)
        txt = html.unescape(no_titles)
        # Then, remove them using beautiful soup
        no_tags = BeautifulSoup(txt, "lxml").text

        # Remove formatting with double-single quotes (''...'')
        no_format = re.sub("''+", "", no_tags)

        # Remove indent guides
        no_indent = re.sub(r"\n:*", "\n", no_format)
        return no_indent



    def build_tree(self, page: ET.Element, corpus_name: str):
        """

        :param page:
        :param corpus_name:
        :return:
        """
        attrs = self.get_attrs(page, corpus_name)
        file = ET.Element("file", attrs)
        text = ET.SubElement(file, "text")
        segment = ET.SubElement(text, "segment", { "id" : f"id{attrs["filename"]}"})
        segment.text = self.clean_text(page.find("default:revision", self.ns).find("default:text", self.ns).text)
        return attrs["title"], file

    def parse_corpus(self, input_file: PathLike[str], output_dir: PathLike[str], corpus_name: str):
        """

        :param input_file:
        :param output_dir:
        :param corpus_name:
        """
        tree = self.parse_xml(input_file)

        pages = tree.findall("default:page", self.ns)

        for page in pages:

            title, file = self.build_tree(page, corpus_name)

            et_string = ET.tostring(file, encoding="utf-8")

            e_tree = parseString(et_string)

            impl = getDOMImplementation()
            doctype = impl.createDocumentType("file", "", "wikixml.dtd")
            dom_doc = impl.createDocument(None, "xml", doctype)

            dom_doc.replaceChild(e_tree.documentElement, dom_doc.documentElement)

            xml_text = dom_doc.toprettyxml(encoding="utf-8", standalone=False)

            with open(output_dir/(title+".xml"), 'wb') as f:
                f.write(xml_text)
