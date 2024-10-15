import os
import glob
import iris
import mo_pack
import pandas as pd
import numpy as np
import logging
import xarray as xr
from xmip.preprocessing import rename_cmip6
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import sys

path_to_archive = '/gws/nopw/j04/moghli/archive/'


all_runs = ['u-de012', 'u-de052', 'u-de348', 'u-de399', 'u-de567', 
            'u-df848', 'u-dg028', 'u-dg549', 'u-de013', 'u-de110', 
            'u-de349', 'u-de457', 'u-de593', 'u-df859', 'u-dg051',
            'u-dg552', 'u-de018', 'u-de111', 'u-de350', 'u-de505',
            'u-de633', 'u-df931', 'u-dg309', 'u-dg655', 'u-dd987', 
            'u-de026', 'u-de145', 'u-de365', 'u-de506', 'u-de636', 
            'u-df710', 'u-df932', 'u-dg331', 'u-dg683', 'u-dd989', 
            'u-de050', 'u-de187', 'u-de369', 'u-de517', 'u-df777', 
            'u-dg027', 'u-dg381']

for run in all_runs:
    outpath_root = '/gws/nopw/j04/moghli/postprocessed_ncs/'
    outpath = outpath_root+run+'/TOAFluxesUpCleanSky'
    
    #if os.path.exists(outpath):
    #    print(run)
    #    print('skipping')
        
    #else:
    #    os.makedirs(outpath)

    if not os.path.exists(outpath):
        os.makedirs(outpath)
        
    print(run)
    stream = 'a.p4'
    runpath = path_to_archive + run + '/'
    cycles = os.listdir(runpath)
    
    paths = []
    for cycle in ['20350101T0000Z']:
        cyclepath = runpath + cycle + '/'
        files = [x for x in os.listdir(cyclepath) if stream in x]
        for f in files:
            paths.append(cyclepath+f)
    
    stash_dict = {'m01s01i517':'clean-air_upward_SW_flux_levels',
                  'm01s02i517':'clean-air_upward_LW_flux_levels',
                  'm01s01i519':'clearclean-air_upward_SW_flux_levels',
                  'm01s02i519':'clearclean-air_upward_LW_flux_levels',
                  }
    
    
    for path in paths:
        cubes = iris.load(path)
            
        sub_list_cubes, stashes = [], []
        
        for stash in stash_dict.keys():    
            for cube in cubes:
                if str(cube.attributes['STASH']) == stash:
                    sub_list_cubes.append(cube)
                    stashes.append(stash)
        out_cubes = dict(zip(stashes, sub_list_cubes))
        
        ds_list = []
        for stash in stash_dict.keys():  
            da = xr.DataArray.from_iris(out_cubes[stash])
            ds = da.to_dataset(name=stash_dict[stash])
            ds_list.append(ds)
        ds = xr.merge(ds_list)
        ds = ds.sel(model_level_number=86) # select TOA
        
        month = ds.time.dt.month.item()
        year = ds.time.dt.year.item()
        
        
        if not os.path.exists(outpath):
            os.makedirs(outpath)
    
        ds.to_netcdf(outpath+'/TOAFluxesUpCleanSky_{y}_{m}_{r}.nc'.format(y=year, m=month, r=run))