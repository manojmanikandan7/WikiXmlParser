from pathlib import Path
import typer
from .parser import XmlParser
from typing_extensions import Annotated


def run(
    input_file_name: Annotated[str, typer.Argument(help="The input file path for the XML file")],
    output_dir: Annotated[str, typer.Argument(help="The output file directory for the transformed XML files")],
    corpus_name: Annotated[str, typer.Argument(help="The name of this corpus")],
):
     x_parser = XmlParser()
     x_parser.parse_corpus(Path(input_file_name), Path(output_dir), corpus_name)

app = typer.Typer()
app.command()(run)
if __name__ == "__main__":
    app()