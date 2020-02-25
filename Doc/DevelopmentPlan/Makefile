DevelopmentPlan.pdf: DevelopmentPlan.bbl DevelopmentPlan.aux
	pdflatex DevelopmentPlan.tex
	pdflatex DevelopmentPlan.tex

DevelopmentPlan.bbl: DevelopmentPlan.aux bibfile.bib DevelopmentPlan-blx.bib
	bibtex DevelopmentPlan.aux

DevelopmentPlan.aux: DevelopmentPlan.tex
	pdflatex DevelopmentPlan.tex

clean:
	rm *.aux *.bbl *.blg *-blx.bib *.log *.out *.run.xml *.toc
