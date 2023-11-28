# Pathes
PRINT := content/print
PAGES := content/pages
GABARIT := gabarit
GABARIT_SRC := $(GABARIT)/src
GABARIT_CHAPTERS := $(GABARIT_SRC)/chapitres
GABARIT_PAGES := $(GABARIT_SRC)/pages
BIB_FILE := content/bib/bibtex.bib
BIB_FORMAT := content/bib/lettres-et-sciences-humaines-fr.csl

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


content/print/references.html : $(PAGES)/references.md
	pandoc \
  	--citeproc \
	$(CITEPROC_OPTIONS) \
    $(PAGES)/references.md \
	-o $@

$(GABARIT_PAGES)/references.md : $(PRINT)/references.html
	@cat $< > $@
	@echo References are transmuted from html to markdown


references: $(GABARIT_PAGES)/references.md 

all: gabarit replace_md references  

# content/print/%.tex: $(PRINT)/%.md
# 	pandoc $< $(TEX_OPTIONS) -o $@

# tex_chapters_standalone_%: content/print/%.tex 

# tex_chapters_standalone: $(TEX_CHAPTERS_STANDALONE_OUT)  

# %.tex: content/print/%.tex
# 	@ ./python/tex_extract.py $<


# tex_chapters_%: %.tex
	
# tex_chapters: $(TEX_CHAPTERS_OUT)

# these.pdf: tex_chapters
# 	xelatex these.tex $(TEX_CHAPTERS_OUT)

# prepare_gabarit: set_gabarit copy_shit_in_gabarit

pdf: these.pdf

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