from pygments.style import Style
from pygments.token import (
    Comment,
    Keyword,
    Name,
    String,
    Error,
    Generic,
    Number,
    Text,
    Literal,
)


class Colors:
    # https://github.com/kevinvn1709/vscode-dracula-color-theme/blob/master/themes/dracula-color-theme.json

    foreground = "#d4d4d4"
    background = "#212122"
    highlight = "#2A2A2B26"
    comment = "#808080"
    error = "#f44747"

    syntax_string = "#6A8759"
    syntax_keyword = "#CC7832"
    syntax_tag = "#FFC66D"
    syntax_constant = "#6897BB"
    syntax_regex = "#6A8759"
    syntax_class = "#D7BA7D"
    syntax_func = "#FFC66D"
    syntax_label = "#C8C8C8"
    syntax_attribute = "#BABABA"
    syntax_pseudo = "#d7ba7d"

    diff_inserted = "#b5cea8"
    diff_deleted = "#ce9178"


class DarculaStyle(Style):
    """
    Pygments style based on the JetBrains darcula theme.

    https://github.com/kevinvn1709/vscode-dracula-color-theme/blob/master/themes/dracula-color-theme.json
    """

    name = "darcula"
    aliases = ["Darcula"]

    background_color = Colors.background
    highlight_color = Colors.highlight

    styles = {
        Text: Colors.foreground,
        Error: Colors.error,
        Comment: Colors.comment,
        Comment.Preproc: Colors.syntax_keyword,
        Comment.PreprocFile: Colors.syntax_string,
        Keyword: f"bold {Colors.syntax_keyword}",
        Keyword.Constant: Colors.syntax_string,
        Keyword.Pseudo: Colors.syntax_pseudo,
        Keyword.Type: Colors.syntax_tag,
        Name.Attribute: Colors.syntax_attribute,
        Name.Builtin: Colors.syntax_func,
        Name.Builtin.Pseudo: Colors.syntax_pseudo,
        Name.Class: Colors.syntax_class,
        Name.Constant: Colors.syntax_constant,
        Name.Decorator: Colors.syntax_func,
        Name.Exception: Colors.syntax_class,
        Name.Function: Colors.syntax_func,
        Name.Tag: Colors.syntax_tag,
        Name.Label: Colors.syntax_label,
        Name.Other: Colors.foreground,
        Literal: Colors.syntax_string,
        String: Colors.syntax_string,
        String.Interpol: Colors.syntax_tag,
        String.Regex: Colors.syntax_regex,
        Number: Colors.syntax_constant,
        Generic.Deleted: Colors.diff_deleted,
        Generic.Inserted: Colors.diff_inserted,
        Generic.Error: Colors.error,
        Generic.Emph: "italic",
        Generic.Strong: f"bold {Colors.syntax_tag}",
        Generic.Heading: Colors.syntax_tag,
        Generic.Subheading: Colors.syntax_tag,
        Generic.Output: Colors.syntax_string,
        Generic.Prompt: Colors.syntax_label,
        Generic.Traceback: Colors.error,
    }
