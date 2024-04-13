# RST to HTML Converter

This script converts reStructuredText (RST) files to HTML, handling custom RST directives and applying optional text replacements. It supports inclusion of a CSS stylesheet in the output HTML files, making it suitable for generating styled documentation or other HTML from RST sources.

## Why?

Because the Bitcoin Developer RPC Reference is bullshit.

## Features

- **Custom Directive Handling**: Ignores or processes custom directives such as `highlight` and `toctree`.
- **Text Replacements**: Applies user-specified text replacements throughout the documents.
- **CSS Styling**: Allows linking a CSS stylesheet to the output HTML documents.
- **Flexible Output**: Outputs HTML files either in the same directory as the source or in a user-specified directory.

## Requirements

- Python 3
- Docutils library

To install dependenies, run:

```bash
pip install -r requirements.txt
```

## Usage

## Basic Command

```bash
./rts-to-html <source_folder> [options]
```

## Options
* --output_folder PATH: Specifies the directory where the converted HTML files will be placed. If not specified, files are generated in the same directory as the source files.
* --replace OLD NEW: Specifies a pair of strings to find and replace in the documents. This option can be repeated to specify multiple replacements.
* --css PATH: Specifies the path to the CSS stylesheet that should be linked in the HTML documents. Defaults to 'style.css'.


## Examples

### Convert Files with Default Settings:

```bash
./rts-to-html path_to_rst_files
```

### Convert Files with Output in a Different Folder:

```bash
./script_name.py path_to_rst_files --output_folder path_to_output_folder
```

### Convert Files with Text Replacements:

```bash
./script_name.py path_to_rst_files --replace "Lorem ipsum" "Example text"
```

### Convert Files with a Custom CSS File:

```bash
./script_name.py path_to_rst_files --css path_to_custom_style.css
```

## How It Works

The script processes each .rst file in the specified directory, applying any specified text replacements. It handles custom directives like toctree by converting them into navigable lists of links, and ignores others like highlight. Finally, it wraps the HTML output with basic HTML tags, including a head tag linking to the specified CSS file, and writes the results to the output directory.

## Contributing

Contributions to this script are welcome. Please ensure to test your changes thoroughly before making a pull request.