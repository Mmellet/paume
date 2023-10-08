#!/usr/bin/env python3

import argparse
from templates import SVG_TEXT, SVG_PATH, SVG_FILE, HTML_FILE, CSS_DELAY

STYLE_TEXT = {
    "font-style": "normal",
    "font-variant": "normal",
    "font-weight": "normal",
    "font-stretch": "normal",
    "font-size": "4pt",
    "font-family": "'GFS Didot'",
    "-inkscape-font-specification": "'GFS Didot'",
    "white-space": "pre",
    "display": "inline",
}
STYLE_PATH = {
    "fill":"transparent",
    "stroke":"#37abc8",
    "stroke-width": "0.5",
    "stroke_linecap": "round",
    "stroke_linejoin": "round",
}


def get_style(**kwargs):
    return ";".join(f"{key}:{value}" for key, value in kwargs.items())


def get_svg_text(**kwargs):
    return SVG_TEXT.format(**kwargs)


def get_css_delay(**kwargs):
    return CSS_DELAY.format(**kwargs)


def get_svg_path(**kwargs):
    return SVG_PATH.format(**kwargs)


def create_svg_and_css(lines, path_color):
    # Force the image to a known size.
    elements = []
    css_animation_delaies = []

    x = 100
    class_text = "text_rendering fade-in-stay-out"
    class_path = "path-fill"
    style_text = get_style(**STYLE_TEXT)
    style_path = get_style(**STYLE_PATH)
    for i, line in enumerate(lines):
        y = (i + 1) * 100
        id_i = i
        text_delay = f" second_delay_{i}"
        path_delay = f" second_delay_{i}_epsilon"
        elements.append(
            get_svg_text(
                id=id_i,
                style=style_text,
                y=y,
                x=x,
                _class=class_text + text_delay,
                text=line,
            )
        )
        css_animation_delaies.append(get_css_delay(delay=i, delay_name=i))
        css_animation_delaies.append(
            get_css_delay(delay=i + 0.25, delay_name=f"{i}_epsilon")
        )
        if i != len(lines) - 1:
            elements.append(
                get_svg_path(
                    id=id_i,
                    style=style_path,
                    y=y + 25,
                    x=x,
                    _class=class_path + path_delay,
                )
            )

    svg_file = SVG_FILE.format(elements="\n".join(elements))
    html_file = HTML_FILE.format(
        svg_content=svg_file[svg_file.find("\n") :],
        css_animation_delaies="\n".join(css_animation_delaies),
    )
    print(html_file)


def get_lines(filename):
    with open(filename.name) as stream:
        text = stream.read()
    return [line.strip() for line in text.split("\n") if line.strip()]


def main(args):
    # text cleaning
    lines = get_lines(args.FILENAME)
    # print(lines)
    # create disposition
    create_svg_and_css(lines, args.path_color)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "FILENAME",
        type=argparse.FileType("r"),
    )
    parser.add_argument("--path_color", default="#37abc8")
    args = parser.parse_args()
    main(args)
