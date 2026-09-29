NOTEBOOKS := $(wildcard *.ipynb)
OUTPUTS := $(NOTEBOOKS:.ipynb=.pdf)

all: $(OUTPUTS)

%.pdf: %.ipynb
	#jupyter nbconvert --execute $<
	#jupyter nbconvert --ExecutePreprocessor.enabled=False --to notebook --execute $< --output /tmp/$<
	papermill $< $*.IPYNB

barb_0MMPG_GF.IPYNB: barb_0MMPG.IPYNB

info:
	@echo "Notebooks:" $(NOTEBOOKS)
	@echo "Outputs:" $(OUTPUTS)

# Clean output markers
clean:
	rm -f *.pdf
