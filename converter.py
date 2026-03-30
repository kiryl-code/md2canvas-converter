import markdown
import css_inline
from pygments.formatters import HtmlFormatter
from markdown_extensions import ExtensionsRegister
import json

# TODO: rm hardcoded values
def run_test():

    with open("input.md", "r", encoding="utf-8") as f:
        test_md = f.read()

    with open("styles/kiya-feedback-style.css", "r", encoding="utf-8") as f:
        page_style = f.read()

    md = markdown.Markdown(extensions=[ExtensionsRegister(), 'fenced_code', 'codehilite', 'toc', 'nl2br'])
    raw_html = md.convert(test_md)

    formatter = HtmlFormatter(style='github-light-default')
    pygments_css = formatter.get_style_defs('.codehilite')

    full_html = f"<meta charset='UTF-8'><style>{pygments_css} {page_style}</style><body>{raw_html}</body>"
    inlined_html = css_inline.inline(full_html)

    with open("test_output.html", "w", encoding="utf-8") as f:
        f.write(inlined_html)

    print("Klart! Öppna 'test_output.html' i din webbläsare.")


def main():
    with open("user-config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    if config.get("run_gui"):
        from gui import run
        run()

if __name__ == "__main__":
    main()
    # run_test()
