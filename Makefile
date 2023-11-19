

.PHONY: all html pdf clean

all: html pdf

clean:
	rm -rf output/*

CHAPTERS := $(sort $(shell find text/chapters -type f -iname '*.md'))
CHAPTERS_OUT := $(patsubst %.md, output/%.html, $(notdir $(CHAPTERS)))

# Copy static files recursively :
# (Adapted from https://stackoverflow.com/questions/41993726/)
STATIC := $(shell find static -type f)
STATIC_OUT := $(patsubst static/%, output/%, $(STATIC))
$(foreach s,$(STATIC),$(foreach t,$(filter %$(notdir $s),$(STATIC_OUT)),$(eval $t: $s)))
$(STATIC_OUT):; $(if $(wildcard $(@D)),,mkdir -p $(@D) &&) cp $^ $@

# Pathes



OPTIONS := -f markdown -t latex --standalone --citeproc --bibliography=content/bib/bibtex.bib --no-highlight # --csl=




# pandoc --standalone --bibliography=bibtex.bib --csl=lettres-et-sciences-humaines-fr.csl --no-highlight -f markdown -t latex

# Pandoc conversions

# Use your own [options]
# Example:
# --data-dir html --standalone --to=html5 --template=template.html
# --css=css/styles.css --section-divs --wrap=none
# --citeproc --bibliography=references.bib --csl=thesis-fr.csl
# --toc --toc-depth=3 --number-sections
# etc.

# PDF
# pdf: output/these.pdf
# output/these.pdf: text/introduction.md $(CHAPTERS) text/conclusion.md
# 	pandoc $^  -o output/these.pdf

# # HTML
# html: $(STATIC_OUT) output/index.html output/introduction.html output/conclusion.html $(CHAPTERS_OUT)
# output/index.html: index.md
# 	pandoc $< [options] -o $@
# output/introduction.html: text/introduction.md
# 	pandoc $< [options] -o $@
# output/conclusion.html: text/conclusion.md
# 	pandoc $< [options] -o $@
# print/replaced_%.md: $(PAGES)/%.md
# 	replacee $(PAGES)/%.md 
# 	replacee 

# print/%.tex: print/replaced_%.md
	



love:
	@ echo "I love U"



# install:
# 	hugo install



# pandoc --standalone --bibliography=bibtex.bib --csl=lettres-et-sciences-humaines-fr.csl --no-highlight -f markdown -t latex 1.md -o 1.tex && xelatex 1.tex