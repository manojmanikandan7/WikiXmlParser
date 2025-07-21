"""
The module for parser functions
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom.minidom import parseString, getDOMImplementation
from os import PathLike
import re

class XmlParser:

    def __init__(self, ns: dict[str:str]):
        self.ns = ns

    @staticmethod
    def parse_xml(file: PathLike) -> ET.ElementTree:
        """
        Parse the input XML file and return an `xml.etree.ElementTree.ElementTree` representation of it.
        :param file:
        :return:
        """
        return ET.parse(file)

    def get_attrs(self, page: ET.Element):
        """

        :param page:
        :return:
        """
        timestamp = page.find("default:revision", self.ns).find("default:timestamp", self.ns).text
        filename = page.find("default:id", self.ns).text

        title = page.find("default:title", self.ns).text
        _, title = title.split(":")
        title_name, archive = re.sub(r"\s", "_", title).split("/")

        url = "https://en.wikipedia.org/wiki/" + title_name + '/' + archive
        return {"type": "Talk", "date": timestamp, "sourceCorpus": "Wikiproject_Medicine", "filename": filename, "title": f"{title_name}_Talk_{archive}", "url": url}

    def clean_text(self, txt: str):
        no_tags = re.sub("&lt;.*&gt;", "", txt)

        no_titles = re.sub("{{.*}}", "", no_tags)
        no_titles = re.sub("==+", "", no_titles)

        no_format = re.sub("''+", "", no_titles)

        no_indent = re.sub(r"\n:*", "\n", no_format)
        return no_indent



    def build_tree(self, page: ET.Element):
        attrs = self.get_attrs(page)
        file = ET.Element("file", attrs)
        text = ET.SubElement(file, "text")
        segment = ET.SubElement(text, "segment", { "id" : f"id{attrs["filename"]}"})
        segment.text = self.clean_text(page.find("default:revision", self.ns).find("default:text", self.ns).text)
        return attrs["title"], file

    def parse(self, input_file: PathLike, output_dir: PathLike):
        tree = self.parse_xml(input_file)

        pages = tree.findall("default:page", self.ns)

        for page in pages:

            title, file = self.build_tree(page)

            et_string = ET.tostring(file, encoding="utf-8")

            e_tree = parseString(et_string)

            impl = getDOMImplementation()
            doctype = impl.createDocumentType("file", "", "wikixml.dtd")
            dom_doc = impl.createDocument(None, "xml", doctype)

            dom_doc.replaceChild(e_tree.documentElement, dom_doc.documentElement)

            xml_text = dom_doc.toprettyxml(encoding="utf-8", standalone=False)

            with open(output_dir/(title+".xml"), 'wb') as f:
                f.write(xml_text)
