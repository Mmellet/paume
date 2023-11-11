#!/usr/bin/env python3
import pathlib
import os
import frontmatter
import re
from collections import Counter

HERE = pathlib.Path(__file__).parent


PAGES_DIR = HERE / "content" / "pages"
themes_counter = Counter()

shortcode_pattern = r'\{\{< themes theme="([^"]+)" >\}\}'

for root, dirs, files in os.walk(PAGES_DIR):
    for file in files:
        if file.endswith(".md"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
                content = post.content
                shortcodes = re.findall(shortcode_pattern, content)
                for theme in shortcodes:
                    themes_counter[theme] += 1
                    if theme not in themes_mapping:
                        themes_mapping[theme] = []
                    themes_mapping[theme].append(os.path.join(root, file))


# Conversion du compteur en DataFrame pour la création du graphique
themes_df = pd.DataFrame.from_dict(
    themes_counter, orient="index", columns=["Occurrence"]
)
themes_df = themes_df.sort_values(by="Occurrence", ascending=False)

# Création d'un diagramme à barres
plt.bar(themes_df.index, themes_df["Occurrence"])
plt.xlabel("Thématique")
plt.ylabel("Occurrences")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Affichage ou sauvegarde du graphique
plt.show()
