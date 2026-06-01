from pathlib import Path

import markdown
import css_inline
from pygments.formatters import HtmlFormatter
from markdown_extension import ExtensionsRegister


def convert(input_path: str, output_path: str, styles_path: str) -> None:
    """
    A main converter function that converts a given markdown file into html file
    as well as styles the output with a provided stylesheet
    :param input_path: markdown file path
    :param output_path: output directory path
    :param styles_path: stylesheet path
    """
    # TODO: add error handling
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
                    "tables"])

    html = md.convert(markdown_content)

    formatter = HtmlFormatter(style="dark-plus")
    pygments_css = formatter.get_style_defs(".codehilite")

    html = f"<meta charset='UTF-8'><style>{pygments_css} {styles}</style><body>{html}</body>"
    html = css_inline.inline(html)

    with open(Path(output_path) / "output.html", "w", encoding="utf-8") as f:
        f.write(html)
