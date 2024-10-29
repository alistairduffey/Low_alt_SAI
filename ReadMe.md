All code to 
(1) postprocess simulations (/Postprocess_runs) and 
(2) analyse and plot postprocessed simulations (/Analysis)

for Duffey et al., 2024 (?): Low-altitude high-latitude stratospheric aerosol injection is feasible with existing aircraft 

NBs:

* The simulations themselves are not in this directory (they are in /gws/nopw/j04/moghli). Postprocessing needs to run on jasmin, with access to this group workspace. 
* I use two seperate environments, one for the GP_emulation and one for everything else. This is because Tensorflow seems to play badly with other packages.
* supp_data not uploaded to GH - this is the AODs for the two 30-year UKESM simulations with injection at 21km 30N/S, which make supp fig S1. This data is available on the zenodo archive under runs u-cd297 (30N) and u-cd354 (30S).
* Postprocess_runs writes postprocessed data to an archive. I have copied all of this except the 3d aerosol burdens files to the shared version of this archive, which is uploaded to zenodo. These 3d burdens are too large for zenodo, so i have added a zonal and annual mean version of these files (which is all that is needed to reproduce the supplementary figures) to the zenodo for these variables instead. The code to produce these means is at the end of Analysis/06_Reff_and_spatial_burdens.ipynb

  

