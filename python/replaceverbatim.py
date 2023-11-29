#!/usr/bin/env python3
import re
import fileinput
import argparse
import pathlib
import json

from pprint import pprint
import logging


WORKSPACE_DIR = pathlib.Path(__file__).parent.parent
STATIC_DIR = WORKSPACE_DIR / "static"
PRINT_DIR = WORKSPACE_DIR / "content" / "print"
SCR_DIR = WORKSPACE_DIR / "gabarit" / "src"
G_CHAPTERS_DIR = SCR_DIR / "chapitres"
G_PAGES_DIR = SCR_DIR / "pages"
PAGES_DIR = WORKSPACE_DIR / "content" / "pages"
MAP = PAGES_DIR / "iframe_map.json"

with MAP.open() as stream:
    MAP = json.load(stream)

# pprint(MAP)


def get_args():
    parser = argparse.ArgumentParser(description="Description of the program")
    parser.add_argument(
        "pathes",
        type=argparse.FileType("r"),
        nargs="+",
        help="Mardown file pathes to replace tags, figure and iframe.",
    )
    args = parser.parse_args()
    return args


def replace_spacing_verbatim(text):
    def repl(match):
        verbatim = match.groups()
        print(verbatim)
        verbatim = "".join(verbatim)
        balise = "<!-- LATEX |\\vspace{{0.4cm}}| -->"
        return f"\n{balise}{verbatim}{balise}\n\n"

    pattern = re.compile(r"(^ {4,}.*\n)+", re.MULTILINE)
    return re.sub(pattern, repl, text)


def replace_all(text):
    text = replace_spacing_verbatim(text)
    return text


def save_replaced_markdown(text, path):
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_text(text)
    print(f"Creation: {path}")


def get_text(text_io_wrapper):
    return text_io_wrapper.read()


def main(args):
    for text_io_wrapper in args.pathes:
        dest = PAGES_DIR / text_io_wrapper.name.split("/")[-1]
        if dest.name != "references.md":
            text = get_text(text_io_wrapper)
            text = replace_all(text)
            save_replaced_markdown(text, dest)
        else:
            print(
                "We are sorry your references are too long to be proccessed,"
                " but don't worry pandoc will take care of it"
            )


if __name__ == "__main__":
    args = get_args()
    main(args)
