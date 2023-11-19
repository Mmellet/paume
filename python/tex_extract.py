#!/usr/bin/env python3
import re
import fileinput
import argparse
import pathlib

import logging


HERE = pathlib.Path(__file__).parent.parent
STATIC_DIR = HERE / "static"
PRINT_DIR = HERE / "content" / "print"

def get_args():
    parser = argparse.ArgumentParser(description="Shitty way of making ")
    parser.add_argument(
        "pathes",
        type=argparse.FileType("r"),
        nargs="+",
        help="Tex file pathes to extract document content from.",
    )
    args = parser.parse_args()
    return args


def extract_document_content(text, filename):
    pattern = re.compile(r'\\begin\{document\}(.*?)\\end\{document\}', re.DOTALL)
    match = pattern.search(text)
    extracted_content = f"\n\nNO EXTRACTED DOCUMENT FOR {filename}\n\n"
    if match:
        extracted_content = match.group(1)
    return extracted_content

def replace_images_pathes(text):
    return text.replace("\includegraphics{/images/", f"\includegraphics{{{PRINT_DIR/'images'}/")


def save_root_tex(text, path):
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(text)


def get_text(text_io_wrapper):
    return text_io_wrapper.read()


def main(args):
    for text_io_wrapper in args.pathes:
        dest = HERE / text_io_wrapper.name.split("/")[-1] 
        text = get_text(text_io_wrapper)
        text = extract_document_content(text, dest.name)
        text = replace_images_pathes(text)
        save_root_tex(text, dest)


if __name__ == "__main__":
    args = get_args()
    main(args)
