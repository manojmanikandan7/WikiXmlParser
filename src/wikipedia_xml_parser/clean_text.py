"""
Module for tools to clean revision text of Wikipedia pages
"""
from typing import Iterable
from bs4 import BeautifulSoup
import html

def clean_text(txt: str,
               cards_filter: Iterable[str] = ("infobox", "wikiproject", "user", "press", "graph", "image", "reflist",
                                          "multiple", "ordered", "list")) -> str:
    """
    Function to clean and extract text from the page content.
    XML/HTML tags, Wikipedia formatting, tables, infoboxes, internal links and media links are all removed.
    If alternative titles are provided for links, they are preserved.
    Note: External/markdown-style links are not removed.

    :param cards_filter: The wikipedia cards to filter out
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

    no_format_patterns = re.sub("{{[^}]*?data/.*?}}", ";DYN;", no_tables)
    no_format_patterns = re.sub("{{[^}]*?As of\|(.*?)}}", r"As of \1", no_format_patterns)
    # Note: This should be done before removing tags, since Beautiful Soup looks for curly braces ('{', '}') for namespaces
    no_format_patterns = re.sub("{{.*?}}", "", no_format_patterns)
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