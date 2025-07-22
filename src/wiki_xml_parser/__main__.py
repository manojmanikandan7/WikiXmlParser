"""

"""
from .parser import XmlParser
from pathlib import Path
import argparse


# TODO: Build a CLI
# parser = argparse.ArgumentParser()

parser = XmlParser()
parser.parse_corpus(Path("resources/Talk MEDRS All archives.xml"), Path("outputs/MEDRS"), "MEDRS")
parser.parse_corpus(Path("resources/Talk Wikiproject Medicine All Archives.xml"), Path("outputs/Wikiproject Medicine"), "WikiProject_Medicine")
