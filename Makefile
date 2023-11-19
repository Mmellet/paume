# Pathes
PRINT := content/print
PAGES := content/pages # Source of truth
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

# all: html pdf



CHAPTERS := $(sort $(shell find $(PAGES) -type f -iname '*.md'))
TEX_CHAPTERS_OUT := $(patsubst %.md, $(PRINT)/%.tex, $(notdir $(CHAPTERS)))
PDF_CHAPTERS_OUT := $(patsubst %.md, $(PRINT)/%.pdf, $(notdir $(CHAPTERS)))
REPLACED_CHAPTERS_OUT := $(patsubst %.md, $(PRINT)/%.md, $(notdir $(CHAPTERS)))

LATEX_SHIT := these.aux these.lof these.lot these.toc
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

clean_print:
	@rm -rfv $(PRINT)/*

clean_pdf: 
	@ rm -v $(LATEX_SHIT) these.pdf  2>/dev/null || true

content/print/%.md: content/pages/%.md
	@ ./python/replace.py $<

replace_md: $(REPLACED_CHAPTERS_OUT)

content/print/%.tex: $(PRINT)/%.md
	pandoc $< $(TEX_OPTIONS) -o $@


tex_chapters_%: content/print/%.tex 

these.pdf: 
	xelatex these.tex

pdf: these.pdf


.PHONY: all html pdf clean


love:
	@ echo "I love U"