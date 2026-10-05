all: denoised.pdf

even.mrc: split_even_odd.ipynb
	conda run -n cryocare_11b papermill split_even_odd.ipynb split_even_odd.IPYNB

denoised/Corbel2301_block2_June2019_crop_ali_crop.mrc: even.mrc denoise.ipynb
	conda run -n cryocare_11b papermill denoise.ipynb denoise.IPYNB
	#rm even.mrc odd.mrc

denoised.pdf:	denoised/Corbel2301_block2_June2019_crop_ali_crop.mrc results.ipynb
	conda run -n results papermill results.ipynb results.IPYNB
	rm -rf denoised/ data/ model
	rm model.tar.gz
	rm *.json

