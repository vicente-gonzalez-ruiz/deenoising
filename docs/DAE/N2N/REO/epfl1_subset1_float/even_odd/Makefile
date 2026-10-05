all: denoised.pdf

even.mrc: split_even_odd.ipynb
	conda run -n cryocare_11b papermill split_even_odd.ipynb split_even_odd.IPYNB

denoised/epfl1_subset1_float.mrc: even.mrc denoise.ipynb
	conda run -n cryocare_11b papermill denoise.ipynb denoise.IPYNB
	#rm even.mrc odd.mrc

denoised.pdf:	denoised/epfl1_subset1_float.mrc results.ipynb
	conda run -n results papermill results.ipynb results.IPYNB
	rm -rf denoised/ data/ model
	rm model.tar.gz
	rm *.json

