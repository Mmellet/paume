import bibtexparser
import json
import re

# Chemin vers mon fichier BibTeX
bibtex_file = 'content/bib/bibtex_sample.bib'
temp_bib_tex = "content/bib/bibtex_sample.bib.temp"

with open(bibtex_file) as f:
    with open(temp_bib_tex, "w+") as w:
        text=f.read()
        text=re.sub(r"month( *= *)([a-z]{3})", r"month\1{\2}", text)
        w.write(text)

# Charger le fichier BibTeX
with open(temp_bib_tex) as f:
    bib_database = bibtexparser.load(f)

# Convertir en format JSON
references = []
print(len(bib_database.entries))
for entry in bib_database.entries:
    reference = {
        'key': entry['ID'],
        'author': entry.get('author', ''),
        'title': entry.get('title', ''),
        'year': entry.get('year', ''),
        'month': entry.get('month', '')
    }
    references.append(reference)

# Écrire le fichier JSON
json_file = 'static/bib.json'
with open(json_file, 'w') as f:
    json.dump(references, f, indent=4)
