All code to 
(1) postprocess simulations (/Postprocess_runs) and 
(2) analyse and plot postprocessed simulations (/Analysis)

for Duffey et al., 2024 (?): Low-altitude high-latitude stratospheric aerosol injection is feasible with existing aircraft

NBs:

* the simulations themselves are not in this directory (they are in /gws/nopw/j04/moghli). Postprocessing needs to run somewhere with access to this data, and filepaths will need updating.
* To recreate my analysis, there is no need to re-run postprocessing (which requires the original raw model outputs). Instead point the Analysis .ipynb scripts to a copied version of my postprocessed data (created by the scripts in "/Postprocess_runs"). This postprocessed data is available on Zenodo at: TBC
* I use two seperate environments, one for the GP_emulation and one for everything else. This is because Tensorflow seems to play badly with other packages.
* Supplementary figure 1 requires AOD data for two additional 35-year simulations, which is in the data archive, and will need copying to /Analysis/supp_data/ before "07_AOD_evolution.ipynb" can be run.
