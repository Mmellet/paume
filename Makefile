# Pathes
PRINT := content/print
PAGES := content/pages
GABARIT := gabarit
GABARIT_SRC := $(GABARIT)/src
GABARIT_CHAPTERS := $(GABARIT_SRC)/chapitres
GABARIT_PAGES := $(GABARIT_SRC)/pages
GABARIT_TMP := $(GABARIT)/tmp
BIB_FILE := content/bib/bibtex.bib
BIB_FORMAT := content/bib/etudes-francaises.csl

CSL_FILE := gabarit/etudes-francaises.csl

STATIC := static

G_CHAPTERS := $(sort $(shell find $(PAGES) -name '[[:digit:]].md'))
G_PAGES := $(sort $(shell find $(PAGES) ! -name '[[:digit:]].md'| grep '.md'))
GABARIT_CHAPTERS_OUTPUT := $(patsubst %.md, $(GABARIT_CHAPTERS)/%.md, $(notdir $(G_CHAPTERS)))
GABARIT_PAGES_OUTPUT := $(patsubst %.md, $(GABARIT_PAGES)/%.md, $(notdir $(G_PAGES)))

CITEPROC_OPTIONS=--bibliography=$(BIB_FILE) --csl=$(CSL_FILE)

lol:
	@echo $(GABARIT_PAGES) |cat -e
	@echo $(GABARIT_CHAPTERS) | cat -e
	@echo $(GABARIT_PAGES_OUTPUT) | cat -e
	@echo $(GABARIT_CHAPTERS_OUTPUT) | cat -e

copy_images: 
	@mkdir -vp $(GABARIT)/$(PRINT)/images
	@mkdir -vp $(GABARIT)/$(PRINT)/creation
	@cp -vr $(STATIC)/images  $(GABARIT)/$(PRINT)
	@cp -vr $(STATIC)/creation  $(GABARIT)/$(PRINT)

clean_gabarit:
	@rm -rfv $(GABARIT_CHAPTERS_OUTPUT) $(GABARIT_PAGES_OUTPUT) 2>/dev/null || true

clean_print:
	@rm -rfv $(PRINT)/* 

clean_pdf: 
	@ rm -v $(LATEX_SHIT) these.pdf  2>/dev/null || true

clean: clean_print clean_gabarit # clean_pdf #reset_gabarit

pages: # why ? I don't know ! ok ! it's required !
	@ echo WTF 

gabarit/src/pages/%.md: content/pages/%.md
	@ ./python/replace.py $<

gabarit/src/chapitres/%.md: content/pages/%.md
	@ ./python/replace.py $<

replace_md: $(GABARIT_PAGES_OUTPUT) $(GABARIT_CHAPTERS_OUTPUT)

gabarit/src/bibliographie.json: path/to/bib.json
	cp -v path/to/bib.json gabarit/src/bibliographie.json

cp_bib: gabarit/src/bibliographie.json

gabarit/src/reglages.md: static/src/reglages.md
	cp -v static/src/reglages.md gabarit/src/reglages.md

cp_reglages: gabarit/src/reglages.md

gabarit: copy_images cp_bib cp_reglages

$(PAGES)/references.tex:
	echo boom a wild appear $(PAGES)/references.tex


$(GABARIT_TMP)/references.md.tex : $(PAGES)/references.tex
	@cp -v $< $@


references: $(GABARIT_TMP)/references.md.tex

distant_clean:
	make -C gabarit clean

all: distant_clean gabarit replace_md references
	make -C gabarit memoire.pdf

set_gabarit:
	git submodule update --init --recursive

# reset_gabarit:
# 	@ cd gabarit && git checkout . 2>/dev/null 
# # @ cd gabarit && git clean -fd . 2>/dev/null 



.PHONY: all html pdf clean gabarit


install_pandoc:
	sudo wget https://github.com/jgm/pandoc/releases/download/1.15.1/pandoc--amd64.deb
	sudo dpkg -i pandoc-1.15.1-1-amd64.deb

love:
	@ echo "I love U"