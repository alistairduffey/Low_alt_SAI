All code to 
(1) postprocess simulations (/Postprocess_runs) and 
(2) analyse and plot postprocessed simulations (/Analysis)

for Duffey et al., 2024: Low-altitude high-latitude stratospheric aerosol injection is feasible with existing aircraft
Earth's Future (hopefully..). 

NBs:

* the simulations themselves are not in this directory (they are in /gws/nopw/j04/moghli). Postprocessing needs to run on jasmin, with access to this gws. 
* I use two seperate environments, one for the GP_emulation and one for everything else. This is because Tensorflow seems to play badly with other packages.
* some data has been brought in from elsewhere..
  

