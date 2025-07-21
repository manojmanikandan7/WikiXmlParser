"""

"""
from src.wiki_xml_parser.parser import XmlParser
from pathlib import Path
import argparse


# TODO: Build a CLI
# parser = argparse.ArgumentParser()

parser = XmlParser({"default": "http://www.mediawiki.org/xml/export-0.11/"})
parser.parse_corpus(Path("../../resources/Talk MEDRS All archives.xml"), Path("../../outputs/MEDRS"), "MEDRS")
parser.parse_corpus(Path("../../resources/Talk Wikiproject Medicine All Archives.xml"), Path("../../outputs/Wikiproject Medicine"), "WikiProject_Medicine")
