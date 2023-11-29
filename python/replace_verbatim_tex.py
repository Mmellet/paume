#!/usr/bin/env python3
import re
import fileinput
import argparse
import pathlib
import json
from pprint import pprint
import logging


WORKSPACE_DIR = pathlib.Path(__file__).parent.parent
SCR_DIR = WORKSPACE_DIR / "gabarit" / "src"
G_CHAPTERS_DIR = SCR_DIR / "chapitres"
G_PAGES_DIR = SCR_DIR / "pages"



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

BALISE = "\\vspace{0.4cm}"

def replace_verbatim_ending(text):
    return text.replace("\\end{verbatim}",f"\\end{{verbatim}}\n{BALISE}\n")

def replace_verbatim_opening(text):
    return text.replace("\\begin{verbatim}",f"\n{BALISE}\n\\begin{{verbatim}}")

def replace_verbatim(text):
    return replace_verbatim_opening(replace_verbatim_ending(text))

def replace_all(text):
    text = replace_verbatim(text)
    return text


def save_replaced_markdown(text, path):
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_text(text)
    print(f"Replace verbatim: {path}")


def get_text(text_io_wrapper):
    return text_io_wrapper.read()


def main(args):
    for text_io_wrapper in args.pathes:
        dest = pathlib.Path(text_io_wrapper.name)
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