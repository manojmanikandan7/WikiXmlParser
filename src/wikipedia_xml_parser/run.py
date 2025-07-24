from parser import XmlParser
from pathlib import Path

x_parser = XmlParser()
x_parser.parse_corpus(Path("../../corpus/Covid-19.xml"), Path("../../outputs/COVID-19"), "COVID-19")