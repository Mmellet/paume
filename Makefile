# Pathes
PRINT := content/print
PAGES := content/pages # Source of truth
GABARIT := gabarit
GABARIT_SRC := $(GABARIT)/src
GABARIT_CHAPTERS := $(GABARIT_SRC)/chapitres
GABARIT_PAGES := $(GABARIT_SRC)/pages
BIB_FILE := content/bib/bibtex.bib
BIB_FORMAT := content/bib/lettres-et-sciences-humaines-fr.csl
TEX_GABARIT := gabarit/gabarit.tex
CLASS_LATEX := gabarit/dms.cls

STATIC := static

# # Copy static files recursively :
# # (Adapted from https://stackoverflow.com/questions/41993726/)
# STATIC := $(shell find static -type f)
# STATIC_OUT := $(patsubst static/%, output/%, $(STATIC))
# $(foreach s,$(STATIC),$(foreach t,$(filter %$(notdir $s),$(STATIC_OUT)),$(eval $t: $s)))
# $(STATIC_OUT):; $(if $(wildcard $(@D)),,mkdir -p $(@D) &&) cp $^ $@




CHAPTERS := $(sort $(shell find $(PAGES) -type f -iname '*.md'))
TEX_CHAPTERS_STANDALONE_OUT := $(patsubst %.md, $(PRINT)/%.tex, $(notdir $(CHAPTERS)))
GABARIT_CHAPTERS_OUTPUT := $(patsubst %.md, $(GABARIT_CHAPTERS)/%.md, $(notdir $(CHAPTERS)))
GABARIT_PAGES_OUTPUT := $(patsubst %.md, $(GABARIT_PAGES)/%.md, $(notdir $(CHAPTERS)))
PDF_CHAPTERS_STANDALONE_OUT := $(patsubst %.md, $(PRINT)/%.pdf, $(notdir $(CHAPTERS)))
TEX_CHAPTERS_OUT := $(patsubst %.md, %.tex, $(notdir $(CHAPTERS)))
AUX_CHAPTERS_OUT := $(patsubst %.md, %.aux, $(notdir $(CHAPTERS)))
REPLACED_CHAPTERS_OUT := $(patsubst %.md, $(PRINT)/%.md, $(notdir $(CHAPTERS)))

LATEX_SHIT := these.aux these.lof these.lot these.toc these.log $(AUX_CHAPTERS_OUT) $(TEX_CHAPTERS_OUT)
TEX_OPTIONS := -f markdown -t latex --standalone  --bibliography=$(BIB_FILE) --no-highlight --csl=$(BIB_FORMAT) --pdf-engine=xelatex  # --citeproc





# # HTML
# html: $(STATIC_OUT) output/index.html output/introduction.html output/conclusion.html $(CHAPTERS_OUT)
# output/index.html: index.md
# 	pandoc $< [options] -o $@
# output/introduction.html: text/introduction.md
# 	pandoc $< [options] -o $@
# output/conclusion.html: text/conclusion.md
# 	pandoc $< [options] -o $@
# print/%.md: $(PAGES)/%.md
# 	replacee $(PAGES)/%.md 
# 	replacee 

copy_images: clean_print_images
	cp -r $(STATIC)/images $(PRINT)/images
	cp -r $(STATIC)/creation $(PRINT)/creation
	mkdir -p $(GABARIT)/$(PRINT)/images
	mkdir -p $(GABARIT)/$(PRINT)/creation
	cp -r $(PRINT)/images  $(GABARIT)/$(PRINT)
	cp -r $(PRINT)/creation  $(GABARIT)/$(PRINT)

clean_print_images:
	@rm -rfv $(PRINT)/images/

clean_print:
	@rm -rfv $(PRINT)/*

clean_pdf: 
	@ rm -v $(LATEX_SHIT) these.pdf  2>/dev/null || true

clean: clean_pdf clean_print #reset_gabarit

content/print/%.md: content/pages/%.md
	@ ./python/replace.py $<

replace_md: $(REPLACED_CHAPTERS_OUT)

copy_chapter_in_gabarit: replace_md
	rm $(GABARIT_CHAPTERS)/*
	cp $(shell find content/print/*.md -type f -name '[[:digit:]].md' | xargs) $(GABARIT_CHAPTERS)

copy_pages_in_gabarit: replace_md
	rm $(GABARIT_PAGES)/*
	cp $(shell find content/print/*.md -type f ! -name '[[:digit:]].md' | xargs) $(GABARIT_PAGES)

copy_shit_in_gabarit: copy_chapter_in_gabarit copy_pages_in_gabarit copy_images
	cp static/gabarit/src/reglages.md gabarit/src/reglages.md
	cp path/to/bib.json gabarit/src/bibliographie.json


content/print/%.tex: $(PRINT)/%.md
	pandoc $< $(TEX_OPTIONS) -o $@


tex_chapters_standalone_%: content/print/%.tex 

tex_chapters_standalone: $(TEX_CHAPTERS_STANDALONE_OUT)  

%.tex: content/print/%.tex
	@ ./python/tex_extract.py $<


tex_chapters_%: %.tex
	
tex_chapters: $(TEX_CHAPTERS_OUT)

these.pdf: tex_chapters
	xelatex these.tex $(TEX_CHAPTERS_OUT)

# prepare_gabarit: set_gabarit copy_shit_in_gabarit

pdf: these.pdf

set_gabarit:
	git submodule update --init --recursive

# reset_gabarit:
# 	@ cd gabarit && git checkout . 2>/dev/null 
# # @ cd gabarit && git clean -fd . 2>/dev/null 


all: replace_md copy_shit_in_gabarit 

.PHONY: all html pdf clean


install_pandoc:
	sudo wget https://github.com/jgm/pandoc/releases/download/1.15.1/pandoc--amd64.deb
	sudo dpkg -i pandoc-1.15.1-1-amd64.deb

love:
	@ echo "I love U"