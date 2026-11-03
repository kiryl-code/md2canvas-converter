#!/usr/bin/env python3

from pathlib import Path
import argparse

import markdown
import css_inline
from pygments.formatters import HtmlFormatter
from markdown_extension import ExtensionsRegister
from utils.stdout_kit import StdoutKit
from utils.darcula_theme import DarculaStyle

DEFAULT_PAGES_STYLE = Path(__file__).parent / "styles" / "pages.css"
DEFAULT_FEEDBACK_STYLE = Path(__file__).parent / "styles" / "feedback.css"


def convert(input_path: Path, output_path: Path, styles_path: Path) -> str:
    """
    A main converter function that converts a given markdown file into html file
    as well as styles the output with a provided stylesheet
    :param input_path: markdown file path
    :param output_path: output directory path
    :param styles_path: stylesheet path

    :return: converted HTML file path
    """
    with open(input_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(styles_path, "r", encoding="utf-8") as f:
        styles = f.read()

    md = markdown.Markdown(
        extensions=[ExtensionsRegister(),
                    "fenced_code",
                    "codehilite",
                    "toc",
                    "nl2br",
                    "sane_lists",
                    "tables",
                    "footnotes"])

    html = md.convert(markdown_content)

    # change code highlight theme here if you want
    formatter = HtmlFormatter(style=DarculaStyle)
    pygments_css = formatter.get_style_defs(".codehilite")

    html = f"<meta charset='UTF-8'><style>{pygments_css} {styles}</style><body>{html}</body>"
    html = css_inline.inline(html)

    output_name = str(input_path).split("/")[-1].split(".")[0].strip()

    with open(output_path / f"{output_name}.html", "w", encoding="utf-8") as f:
        f.write(html)

    return str(output_path / f"{output_name}.html")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert markdown file to an HTML, Canvas-friendly version. May be used for easier styling / "
                    "development of Canvas pages or feedback")
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Path to the markdown file to convert"
    )
    parser.add_argument(
        "-d", "--dir", "--dist",
        help="Path to the output directory"
    )
    style_group = parser.add_mutually_exclusive_group()
    style_group.add_argument(
        "-s", "--styles", "--css",
        help="Path to custom stylesheet"
    )
    style_group.add_argument(
        "-p", "--page",
        action="store_true",
        help="Use default stylesheet for Canvas pages"
    )
    style_group.add_argument(
        "-g", "--grading", "--feedback",
        action="store_true",
        help="Use default stylesheet for feedback (use if you want to attach feedback as an HTML file)"
    )

    args = parser.parse_args()
    markdown_file_path = Path(args.file).expanduser()
    if not Path.exists(markdown_file_path):
        StdoutKit.error(f"File {markdown_file_path} does not exist")
        return

    if not args.dir:
        args.dir = args.dist = markdown_file_path.parent

    if not Path.exists(args.dir):
        StdoutKit.error(f"Directory {args.dir} does not exist. Please create it or specify a valid directory with -d")
        return

    args.dir = Path(args.dir).expanduser()

    if args.page:
        stylesheet_path = DEFAULT_PAGES_STYLE
    elif args.grading:
        stylesheet_path = DEFAULT_FEEDBACK_STYLE
    else:
        stylesheet_path = Path(args.styles).expanduser() if args.styles else None

    if stylesheet_path is None or not Path.exists(stylesheet_path):
        StdoutKit.error(f"File {stylesheet_path} does not exist")
        return

    StdoutKit.cyan(f"Converting {markdown_file_path}")
    result_filepath = convert(markdown_file_path, args.dir, stylesheet_path)
    StdoutKit.cyan(f"Saved to {result_filepath}")


if __name__ == "__main__":
    main()
