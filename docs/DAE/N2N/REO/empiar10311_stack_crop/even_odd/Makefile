all: denoised.pdf

even.mrc: split_even_odd.ipynb
	conda run -n cryocare_11b papermill split_even_odd.ipynb split_even_odd.IPYNB

denoised/empiar10311_stack_crop.mrc: even.mrc denoise.ipynb
	conda run -n cryocare_11b papermill denoise.ipynb denoise.IPYNB
	#rm even.mrc odd.mrc

denoised.pdf:	denoised/empiar10311_stack_crop.mrc results.ipynb
	conda run -n results papermill results.ipynb results.IPYNB
	rm -rf denoised/ data/ model
	rm model.tar.gz
	rm *.json

