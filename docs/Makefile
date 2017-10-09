MAIN_TEX = main.tex
OUTPUT_DIR = _build

build:
	pdflatex -shell-escape $(MAIN_TEX)
	pdflatex -shell-escape $(MAIN_TEX)
	pdflatex -shell-escape $(MAIN_TEX)

clean:
	find . -type f -regex '.*\.\(log\|aux\|dvi\|toc\|out\|xdy\|glo\|glg\|gls\|ist\|lot\|lof\)' -print -delete
	rm -rf _minted-main

.PHONY: build clean
