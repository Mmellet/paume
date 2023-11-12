#!/usr/bin/env python3
import pathlib
import re
from collections import Counter
from collections import defaultdict

from markdown import markdown
from bs4 import BeautifulSoup
from bs4.element import Tag

from pprint import pprint
from copy import deepcopy

HERE = pathlib.Path(__file__).parent


PAGES_DIR = HERE / ".." / "content" / "pages"
themes_counter = Counter()

'{{&lt; themes theme="homo faber" &gt;}}'
SHORTCODE_PATTERN = r'\{\{&lt; *themes *theme="([a-z ]+)" *&gt;\}\}'

PATTERN_TITLE = r'title: *"(.*?)"\n'

THEMES = defaultdict(list)

HTML_HEADERS = ["h1", "h2", "h3", "h4", "h5", "h6"]


def init_default_themes_state():
    return {
        "document_title": None,
        "h1": None,
        "h2": None,
        "h3": None,
        "h4": None,
        "h5": None,
        "h6": None,
    }


def update_themes_state(themes_state, tag, text):
    # print(f"{tag} --> {text}")
    headers_to_rinit = HTML_HEADERS[HTML_HEADERS.index(tag) :]
    for h in headers_to_rinit:
        themes_state[h] = None
    themes_state[tag] = text


def get_next_html_element(soup: BeautifulSoup) -> Tag:
    for element in soup.descendants:
        if element.name is not None:
            yield element


def get_markdown_dom(md_filename: pathlib.Path):
    markdown_content = md_filename.open("r").read()
    html_content = markdown(markdown_content)
    soup = BeautifulSoup(html_content, "html.parser")
    return soup


def get_chapter_title(elt: Tag, filename: str) -> str:
    text = elt.get_text()
    match = re.search(PATTERN_TITLE, text)
    if match:
        title = match.group(1)
    else:
        raise Exception(f"Pattern not found for tittle regex in file name {filename} ")
    return title


def match_theme(elt: Tag) -> str:
    match = re.search(SHORTCODE_PATTERN, str(elt))
    return match


def walk_files():
    paragraphs = []
    for x in PAGES_DIR.glob("*.md"):  # /!\ use "*.md"
        soup = get_markdown_dom(x)
        themes_state = init_default_themes_state()
        soup_generator = get_next_html_element(soup)
        if next(soup_generator).name == "hr":
            elt = next(soup_generator)
            themes_state["document_title"] = get_chapter_title(elt, str(x))
        for elt in soup_generator:
            # print(type(elt))
            if elt.name.startswith("h") and elt.name != "hr" and len(elt.name) == 2:
                update_themes_state(themes_state, elt.name, elt.get_text())
                # pprint(themes_state)
            if m := match_theme(elt):
                THEMES[m.group(1)].append(deepcopy(themes_state))


walk_files()

# pprint(THEMES)

import json

with open("themes.json", "w+", encoding="utf-8") as stream:
    json.dump(THEMES, stream, sort_keys=True, indent=4)


# # Conversion du compteur en DataFrame pour la création du graphique
# themes_df = pd.DataFrame.from_dict(
#     themes_counter, orient="index", columns=["Occurrence"]
# )
# themes_df = themes_df.sort_values(by="Occurrence", ascending=False)

# # Création d'un diagramme à barres
# plt.bar(themes_df.index, themes_df["Occurrence"])
# plt.xlabel("Thématique")
# plt.ylabel("Occurrences")
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()

# # Affichage ou sauvegarde du graphique
# plt.show()
