# md2canvas

## Introduction

This application is designed to seamlessly convert Markdown documents into styled HTML files optimized for Canvas LMS.

### IMPORTANT

As the application is still actively being developed, the `main` branch might not contain some features. If you want to use/test the newest updates, checkout the `dev` branch and run the application manually.

## Features

- Automatically inlines all CSS styles to ensure the output looks exactly as intended within the Canvas LMS environment. However, keep in mind that your organization may enforce some styling rules.
- Custom Markdown syntax extensions:
  - Expandable blocks (`details/summary`) using `^^^^ header`. E.g.:

    ```markdown
    ^^^^ More info
    This application is designed to seamlessly convert Markdown documents into styled HTML files optimized for Canvas LMS.
    ^^^^
    ```

  - Side Blocks: create styled info, warning, or message blocks using `!!!! type`. You can also use color codes (hex) or color name instead of predefined types (which are `warning`, `info`, `message` and `success`) E.g.:
  
    ```markdown
    !!!! warning
    As the application is still actively being developed, the `main` branch might not contain some features. If you want to use/test the newest updates, checkout the `dev` branch and run the application manually.
    !!!!
    ```

  - Inline Colors: color specific words directly in text using `::color | text::`. It supports both color names and hex codes.

- Full support for tables, footnotes and nested lists without breaking numbering (`sane_lists`).

- Integrated with Pygments for syntax highlight in code blocks.

## Requirements

* Python 3.10 or higher

## ToDo

[ ] Add support for different colors/sized for expandable block (may require some changes in syntax)

[ ] Add support for custom classes