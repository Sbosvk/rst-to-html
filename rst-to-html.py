#!/usr/bin/env python3
import os
import argparse
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.core import publish_parts
import re

class IgnoreDirective(Directive):
    has_content = True
    def run(self):
        return []  # Ignore the content

class ToctreeDirective(Directive):
    has_content = True
    option_spec = {
        'maxdepth': int,
        'caption': str,
    }

    def run(self):
        container = nodes.container(classes=['rpc_nav'])
        for entry in self.content:
            item_node = nodes.list_item(classes=['rpc_item'])
            link_node = nodes.reference(refuri=f"/rpc/{entry}.html", text=entry)
            item_node += nodes.paragraph('', '', link_node)
            container += item_node
        return [container]

def setup_directives():
    directives.register_directive('highlight', IgnoreDirective)
    directives.register_directive('toctree', ToctreeDirective)

def apply_replacements(content, replacements, case_insensitive=False):
    for old, new in replacements:
        if case_insensitive:
            content = re.sub(old, new, content, flags=re.IGNORECASE)
        else:
            content = re.sub(old, new, content)
    return content

def add_html_boilerplate(html_content, css_path="style.css", js_path=None, footer_text=""):
    js_link = f'<script src="{js_path}"></script>' if js_path else ""
    footer = f"<footer class='fixed-bottom'><p class='copyright'>{footer_text}</p></footer>"
    return f"""
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="{css_path}">
</head>
<body>
{html_content}
{js_link}
{footer}
</body>
</html>
"""

def rst_to_html(rst_content, replacements, case_insensitive=False):
    setup_directives()
    rst_content = apply_replacements(rst_content, replacements, case_insensitive)
    html_content = publish_parts(source=rst_content, writer_name='html')['html_body']
    return html_content

def convert_folder(source_folder, output_folder=None, replacements=[], css_path="style.css", js_path=None, case_insensitive=False, footer_text=""):
    if output_folder is None:
        output_folder = source_folder

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".rst"):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, source_folder)
                destination_dir = os.path.join(output_folder, relative_path)
                os.makedirs(destination_dir, exist_ok=True)
                destination_path = os.path.join(destination_dir, file[:-4] + ".html")

                with open(source_path, 'r', encoding='utf-8') as file:
                    rst_content = file.read()

                html_content = rst_to_html(rst_content, replacements, case_insensitive)
                full_html = add_html_boilerplate(html_content, css_path, js_path, footer_text)

                with open(destination_path, 'w', encoding='utf-8') as file:
                    file.write(full_html)

                print(f"Converted {source_path} to {destination_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert .rst files to HTML files in a specified directory.")
    parser.add_argument("source_folder", type=str, help="The path to the directory containing .rst files.")
    parser.add_argument("--output_folder", type=str, help="The path to the directory where the converted files should be placed.")
    parser.add_argument("--replace", action='append', nargs=2, metavar=('OLD', 'NEW'), help="Pairs of strings to find and replace in the documents, interpreted as regex.")
    parser.add_argument("--css", type=str, default="style.css", help="Path to the CSS stylesheet.")
    parser.add_argument("--js", type=str, help="Path to the JavaScript file to include.")
    parser.add_argument("--ie", action="store_true", help="Make replacements case insensitive.")
    parser.add_argument("--footer", type=str, default="© Copyright DigiByte Project 2024", help="Custom footer text for the HTML documents.")

    args = parser.parse_args()
    replacements = args.replace if args.replace else []
    convert_folder(args.source_folder, args.output_folder, replacements, args.css, args.js, args.ie, args.footer)

if __name__ == "__main__":
    main()
    