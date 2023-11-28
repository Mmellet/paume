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


def replace_title(text):
    def repl(match):
        title = match.group(1)
        return f"# {title}"

    pattern = re.compile(r'---\n.*title:\s+"(.*?)".*\n---', re.DOTALL)
    return re.sub(pattern, repl, text)


def replace_themes(text):
    def repl(match):
        theme = match.group(1)
        return ""

    pattern = re.compile(r'\{\{<\s*themes\s+theme="([^"]+)"\s*>\}\}', re.DOTALL)
    return re.sub(pattern, repl, text)


def replace_citation(text):
    def repl(match):
        citation_keys = match.group(2)
        citation_key = ";".join(
            [
                f"-@{citation_key[1:]}"
                if citation_key.startswith("-")
                else f"@{citation_key}"
                for citation_key in citation_keys.split(";")
            ]
        )
        page_numbers = match.group(4)
        if page_numbers:
            return (
                f"[{citation_key}, p. {page_numbers}]"
                if "-" not in page_numbers
                else f"[{citation_key}, pp. {page_numbers}]"
            )
        return f"[{citation_key}]"

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

        is_web_url = True
        if not src.startswith("https"):
            src = STATIC_DIR / src.lstrip("/")
            is_web_url = False
        images_urls = MAP["iframe"].get(str(src), {}).get("image_urls", [])

        if not is_web_url and not src.is_file():
            return f'![The img "{src}" doesn\'t exist](static/images/imagenotfound.jpg)'

        # input(f"{src} ---- {title}  ---- ")  # DEBUG
        url_to_join = []
        for url in images_urls:
            img_src = pathlib.Path(url)
            dest = "static/images/imagenotfound.jpg"
            if img_src.is_file():
                dest = PRINT_DIR / "images" / img_src.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(img_src.read_bytes())
            url_to_join.append(f"![{title}]({dest})")
        return "\n".join(url_to_join)

    pattern = re.compile(
        r'<iframe\s+src=["\'](.*?)["\']\s+(title=["\'](.*?)["\'])?.*/?>.*</iframe>'
    )
    return re.sub(pattern, repl, text)


def replace_copy_div_object(text):
    def repl(match):
        _id = match.group(1)
        images_urls = MAP["div_object"].get(_id, {}).get("image_urls", [])
        url_to_join = []
        for url in images_urls:
            img_src = pathlib.Path(url)
            dest = "static/images/imagenotfound.jpg"
            if img_src.is_file():
                dest = PRINT_DIR / "images" / img_src.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(img_src.read_bytes())
            url_to_join.append(f"![{dest.stem.title()}]({dest})")
        return "\n".join(url_to_join)

    pattern = re.compile(
        r'<div\s+id=["\'](.*?)["\']\s*.*?>.*</div>\s*<!--\s*\1\s*-->', re.DOTALL
    )
    return re.sub(pattern, repl, text)


def replace_img_path(text):
    def repl(match):
        alt = match.group(1)
        path = match.group(2).lstrip("/")
        img_src = PAGES_DIR / path
        img_dest = PRINT_DIR / path

        if img_src.is_file():
            img_dest.parent.mkdir(parents=True, exist_ok=True)
            img_dest.write_bytes(img_src.read_bytes())
        return f"![{alt}]({img_dest})"

    pattern = re.compile(r"!\[(.*?)\]\((\/.*?)\)", re.DOTALL)
    return re.sub(pattern, repl, text)


def replace_greek_chars(text):
    def repl(match):
        group1 = match.group(1)
        if group1 in ["τίς", "δ"]:
            return group1
        return f"\\textgreek{{{match.group(1)}}}"

    pattern = re.compile("([\u0370-\u03FF\u1F00-\u1FFF]+)", re.UNICODE)
    return re.sub(pattern, repl, text)


def remove_references(text):
    def repl(match):
        return ""

    pattern = re.compile(
        r"#+\s+Références\n+\{\{<\s*bibliography\s*cited\s*>\}\}", re.DOTALL
    )
    return re.sub(pattern, repl, text)


def replace_latex_comment(text):
    def repl(match):
        return match.group(1)

    pattern = re.compile(r"<!--\s*LATEX\s*\|(.*)\|\s*-->", re.DOTALL)
    return re.sub(pattern, repl, text)


def replace_all(text):
    text = replace_title(text)
    # text = replace_themes(text)
    text = replace_citation(text)
    text = replace_exposant(text)
    text = replace_strike(text)
    text = replace_copy_image(text)
    text = replace_copy_iframe(text)
    text = replace_copy_div_object(text)
    text = replace_img_path(text)
    text = remove_references(text)
    text = replace_greek_chars(text)
    text = replace_latex_comment(text)
    return text


def save_replaced_markdown(text, path):
    if not path.stem.isdigit():
        path = G_PAGES_DIR / path.name
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_text(text)
    print(f"Creation: {path}")


def get_text(text_io_wrapper):
    return text_io_wrapper.read()


def main(args):
    for text_io_wrapper in args.pathes:
        dest = G_CHAPTERS_DIR / text_io_wrapper.name.split("/")[-1]
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

    # DEBUG
    # text="entre la cueillette et l'arrangement qui ne fixe pas mais remet en mouvement constamment les témoins fragmentaires d'une culture. La métaphore étymologique de la fleur (ἀνθολογία ou florilège en latin) est ainsi aisée à filer : en tant que fleuristes numériques, nous souhaitions éditer le rassemblement des fragments épigrammatiqu"
    # print(replace_all(text))
