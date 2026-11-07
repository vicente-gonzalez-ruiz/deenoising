all: denoised.pdf

even_registered.mrc: project_odd_even_and_viceversa.ipynb
	conda run -n opencv papermill project_odd_even_and_viceversa.ipynb project_odd_even_and_viceversa.IPYNB

denoised/empiar10311_stack_crop.mrc: even_registered.mrc denoise.ipynb
	conda run -n cryocare_11b papermill denoise.ipynb denoise.IPYNB
	rm even_registered.mrc odd_registered.mrc

denoised.pdf:	denoised/empiar10311_stack_crop.mrc results.ipynb
	conda run -n results papermill results.ipynb results.IPYNB
	rm -rf denoised/ data/ model/
	rm model.tar.gz *.json

