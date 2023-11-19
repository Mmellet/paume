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
    parser = argparse.ArgumentParser(description="Description of the program")
    parser.add_argument(
        "pathes",
        type=argparse.FileType("r"),
        nargs="+",
        help="Mardown file pathes to replace tags, figure and iframe.",
    )
    args = parser.parse_args(args=["content/pages/replace_dummy.md"])
    return args


def repl(match):
    citation_key = match.group(2)
    page_numbers = match.group(4)
    input(page_numbers)
    if page_numbers:
        return (
            f"[@{citation_key}, p. {page_numbers}]"
            if "-" not in page_numbers
            else f"[@{citation_key}, pp. {page_numbers}]"
        )
    else:
        return f"[@{citation_key}]"


def replace_citation(text):
    def repl(match):
        citation_key = match.group(2)
        page_numbers = match.group(4)
        if page_numbers:
            return (
                f"[@{citation_key}, p. {page_numbers}]"
                if "-" not in page_numbers
                else f"[@{citation_key}, pp. {page_numbers}]"
            )
        return f"[@{citation_key}]"

    pattern = r'{{<\s*cite\s*("|\s*-)([^"\s]+)"?(\s+(\d+-*\d*)?)?\s*>}}'
    return re.sub(pattern, repl, text)


def replace_exposant(text):
    def repl(match):
        return f"^{match.group(1)}^"

    pattern = re.compile(r"<sup>(.*?)</sup>")
    return re.sub(pattern, repl, text)


def replace_exposant(text):
    def repl(match):
        return f"^{match.group(1)}^"

    pattern = re.compile(r"<sup>(.*?)</sup>")
    return re.sub(pattern, repl, text)


def replace_strike(text):
    def repl(match):
        return f"~~{match.group(1)}~~"

    pattern = re.compile(r"<strike[^>]*>(.*?)</strike>")
    return re.sub(pattern, repl, text)


def replace_copy_image(text):
    def repl(match):
        src = match.group(1)
        alt = match.group(3) if match.group(3) else ""

        src = STATIC_DIR / src.lstrip("/")
        dest = PRINT_DIR / "images" / src.name

        # input(f"{src} ---- {alt}  ---- {dest}")  # DEBUG

        if src.is_file():
            # logging.log(logging.INFO, f"copy {src} to {dest}")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(src.read_bytes())
            return f"![{alt if alt else 'EMPTY ALT DESCRITPTION'}]({dest})"
        # logging.log(logging.CRITICAL, f"The file {src} isn't existing")
        return f'![The img "{src}" doesn\'t exist]({dest})'

    pattern = re.compile(r'<img\s+src=["\'](.*?)["\']\s+(alt=["\'](.*?)["\'])?.*/?>')
    return re.sub(pattern, repl, text)

def replace_copy_iframe(text):
    def repl(match):
        src = match.group(1)
        title = match.group(3) if match.group(3) else ""

        src = STATIC_DIR / src.lstrip("/")
        src = src.parent / (src.stem + ".png")
        dest = PRINT_DIR / "images" / src.name

        # input(f"{src} ---- {title}  ---- {dest}")  # DEBUG

        # TODO use content/pages/iframe_map.json

        if src.is_file():
            # logging.log(logging.INFO, f"copy {src} to {dest}")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(src.read_bytes())
            return f"![{title if title else 'EMPTY TILTE DESCRITPTION'}]({dest})"
        # logging.log(logging.CRITICAL, f"The file {src} isn't existing")
        return f'![The img "{src}" doesn\'t exist]({dest})'

    pattern = re.compile(r'<iframe\s+src=["\'](.*?)["\']\s+(title=["\'](.*?)["\'])?.*/?>.*</iframe>')
    return re.sub(pattern, repl, text)


def replace_all(text):
    text = replace_citation(text)
    text = replace_exposant(text)
    text = replace_strike(text)
    text = replace_copy_image(text)
    text = replace_copy_iframe(text)
    return text


def save_replaced_markdown(text, path):
    pass


def get_text(text_io_wrapper):
    return text_io_wrapper.read()


def main(args):
    for text_io_wrapper in args.pathes:
        text = get_text(text_io_wrapper)
        text = replace_all(text)

    print(text)


if __name__ == "__main__":
    args = get_args()
    main(args)
