#!/usr/bin/env python3
import argparse
from bs4 import BeautifulSoup


def prettify_svg(input_file, output_file):
    try:
        if not output_file:
            output_file = input_file.name

        svg_data = input_file.read()

        soup = BeautifulSoup(svg_data, "xml")
        pretty_svg = soup.prettify()

        with open(output_file, "w") as f:
            f.write(pretty_svg)

        print(
            f"SVG file '{input_file.name}' has been prettified and saved to '{output_file}'."
        )
    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Prettify an SVG file using lxml.")
    parser.add_argument(
        "input_filename",
        help="Input SVG file to prettify",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "-o",
        "--output_filename",
        help="Output prettified SVG file",
        default=None,
        type=str,
    )

    args = parser.parse_args()
    prettify_svg(args.input_filename, args.output_filename)


if __name__ == "__main__":
    main()
