all: denoised.pdf

even_registered.mrc: project_odd_even_and_viceversa.ipynb
	conda run -n opencv papermill project_odd_even_and_viceversa.ipynb project_odd_even_and_viceversa.IPYNB

denoised/epfl1_subset1_float.mrc: even_registered.mrc denoise.ipynb
	conda run -n cryocare_11b papermill denoise.ipynb denoise.IPYNB
	rm even_registered.mrc odd_registered.mrc

denoised.pdf:	denoised/epfl1_subset1_float.mrc results.ipynb
	conda run -n results papermill results.ipynb results.IPYNB
	rm -rf denoised/ data/ model/
	rm model.tar.gz *.json

