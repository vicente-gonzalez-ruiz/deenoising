all: denoised.pdf

even_registered.mrc: project_odd_even_and_viceversa.ipynb
	conda run -n opencv papermill project_odd_even_and_viceversa.ipynb project_odd_even_and_viceversa.IPYNB

denoised/Corbel2301_block2_June2019_crop_ali_crop.mrc: even_registered.mrc denoise.ipynb
	conda run -n cryocare_11b papermill denoise.ipynb denoise.IPYNB
	rm even_registered.mrc odd_registered.mrc

denoised.pdf:	denoised/Corbel2301_block2_June2019_crop_ali_crop.mrc results.ipynb
	conda run -n results papermill results.ipynb results.IPYNB
	rm -rf denoised/ data/ model/
	rm model.tar.gz *.json
	rm ../even_odd/*.mrc


