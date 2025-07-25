from pathlib import Path
import typer
from .parser import XmlParser
from .clean_text import clean_text
from typing_extensions import Annotated


app = typer.Typer(help="The command-line interface for processing Wikipedia-exported XML files or its contents")

@app.command(help="The command-line tool for parsing a Wikipedia-exported XML file to simplified XML files")
def parse_corpus(
    input_file_name: Annotated[Path, typer.Argument(help="The input file path for the XML file")],
    output_dir: Annotated[Path, typer.Argument(help="The output file directory for the transformed XML files")],
    corpus_name: Annotated[str, typer.Argument(help="The name of this corpus")],
):
    x_parser = XmlParser()
    x_parser.parse_corpus(Path(input_file_name), Path(output_dir), corpus_name)

@app.command(help="The command-line tool for cleaning/processing Wikipedia-formatted text to plain text")
def process_text(
        input_file_name: Annotated[Path, typer.Argument(help="The input file path for the file with page text")],
        output_file_name: Annotated[Path, typer.Argument(help="The output file path for the cleaned text")],
):
    with open(input_file_name, "r") as file:
        print(f"Cleaning the contents of {input_file_name}...")
        clean = clean_text(file.read())

    with open(output_file_name, "w") as file:
        print(f"Saving cleaned text to {output_file_name}...")
        file.write(clean)


if __name__ == "__main__":
    app()