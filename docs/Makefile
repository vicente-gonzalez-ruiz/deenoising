default:	all

.PHONY: clean all mrproper

all:	main.pdf

BIBINPUTS += ".:~/bibs"

PDFLATEX = pdflatex -synctex=1 -interaction=nonstopmode

main.pdf:	*.tex
		make -C figs
		make -C notebooks
		$(PDFLATEX) main
		(export BIBINPUTS=${BIBINPUTS}:${BIBS}; bibtex main)
		$(PDFLATEX) main
		makeglossaries main
		$(PDFLATEX) main

clean:
		rm -f *.aux *.bbl *.blg *.log *.out *.pdf
