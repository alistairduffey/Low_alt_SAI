## 29th May 2024 AD
## branched from postprocess_sAOD.. 
## this version calculates both stratospheric and whole column AOD

## update Wednesday 31st July - need to add mineral dust to overall AOD calc, since this will be included
## in the background (od550aer) total which we compare against, and is significant (mostly over desserts) 

import os
import glob
import iris
import pandas as pd
import numpy as np
import logging
#import esmvalcore.preprocessor
import xarray as xr
#from xmip.preprocessing import rename_cmip6
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys

path_to_archive = '/gws/nopw/j04/moghli/archive/'

run_dict = {'u-df777':[30.625, 12.9],
            'u-de348':[30.625, 14.1],
            'u-de517':[30.625, 15.4],
            'u-de349':[30.625, 16.0],
            'u-de350':[30.625, 18.0],
            'u-de365':[30.625, 20.2],
            'u-de110':[40.625, 12.3],
            'u-de636':[40.625, 12.9],
            'u-de111':[40.625, 14.1],
            'u-de505':[40.625, 15.4],
            'u-de145':[40.625, 16.0],
            'u-de187':[40.625, 18.0],
            'u-de369':[40.625, 20.2],
            'u-dd987':[50.625, 12.3],
            'u-de593':[50.625, 12.9],
            'u-dd989':[50.625, 14.1],
            'u-de506':[50.625, 15.4],
            'u-de012':[50.625, 16.0],
            'u-de013':[50.625, 18.0],
            'u-de399':[50.625, 20.2],
            'u-de018':[60.625, 12.3],
            'u-de567':[60.625, 12.9],
            'u-de026':[60.625, 14.1],
            'u-de633':[60.625, 15.4],
            'u-de050':[60.625, 16.0],
            'u-de052':[60.625, 18.0],
            'u-de457':[60.625, 20.2],
            'u-dg027':[70.625, 12.3],
            'u-df710':[70.625, 12.9],
            'u-dg309':[70.625, 14.1],
            'u-dg028':[70.625, 15.4],
            'u-dg549':[70.625, 16.0],
            'u-dg552':[70.625, 18.0],
            'u-dg655':[70.625, 20.2],
            'u-df848':[60.625, 12.9, 'Spring'],
            'u-df859':[60.625, 12.9, 'Summer'],
            'u-df931':[60.625, 12.9, 'Autumn'],
            'u-df932':[60.625, 12.9, 'Winter'],
            'u-dg051':[60.625, 12.9, 'Jan-Jun/Jul-Dec'],
            'u-dg331':[60.625, 12.9, 'Mar-Aug/Sep-Feb'],
            'u-dg381':[30.625, 15.4, 'Mar-Aug/Sep-Feb']
            }

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
    print(run)
    
    stream = 'a.pm'
    runpath = path_to_archive + run + '/'
    cycles = os.listdir(runpath)
    
    paths = []
    for cycle in ['20360101T0000Z']:
        cyclepath = runpath + cycle + '/'
        files = [x for x in os.listdir(cyclepath) if stream in x]
        for f in files:
            paths.append(cyclepath+f)
    
    paths = [x for x in paths if 'pm203' in x]
    
    
    stash_dict = {'m01s02i240':'Aitken_mode_soluble_absOD',
                  'm01s02i241':'Accumulation_mode_soluble_absOD',
                  'm01s02i242':'Course_mode_soluble_absOD',
                  'm01s02i243':'Aitken_mode_insoluble_absOD',
                  'm01s02i251':'Aitken_mode_soluble_strato_AOD',
                  'm01s02i252':'Accumulation_mode_soluble_strato_AOD',
                  'm01s02i253':'Course_mode_soluble_strato_AOD',
                  'm01s02i254':'Aitken_mode_insoluble_strato_AOD',
                  'm01s02i300':'Aitken_mode_soluble_AOD',
                  'm01s02i301':'Accumulation_mode_soluble_AOD',
                  'm01s02i302':'Course_mode_soluble_AOD',
                  'm01s02i303':'Aitken_mode_insoluble_AOD',
                  'm01s02i285':'Dust_ambient_aerosol_AOD'
                  }
    
    for path in tqdm(paths):
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
        ds = xr.merge(ds_list).sel(pseudo_level=3) # merge and select 550nm
        
        ds['Total_sAOD'] = ds['Aitken_mode_soluble_strato_AOD'] + ds['Accumulation_mode_soluble_strato_AOD'] + ds['Course_mode_soluble_strato_AOD'] + ds['Aitken_mode_insoluble_strato_AOD']
        
        ds['Total_sulf_AOD'] = ds['Aitken_mode_soluble_AOD'] + ds['Accumulation_mode_soluble_AOD'] + ds['Course_mode_soluble_AOD'] + ds['Aitken_mode_insoluble_AOD']

        ds['Total_AOD'] = ds['Aitken_mode_soluble_AOD'] + ds['Accumulation_mode_soluble_AOD'] + ds['Course_mode_soluble_AOD'] + ds['Aitken_mode_insoluble_AOD'] + ds['Dust_ambient_aerosol_AOD']
        
        ds['Total_absOD'] = ds['Aitken_mode_soluble_absOD'] + ds['Accumulation_mode_soluble_absOD'] + ds['Course_mode_soluble_absOD'] + ds['Aitken_mode_insoluble_absOD']
        
        month = ds.time.dt.month.item()
        year = ds.time.dt.year.item()
        
        outpath_root = '/gws/nopw/j04/moghli/postprocessed_ncs/'
        outpath = outpath_root+run+'/AOD' 
        # NB - this AOD includes mineral dust, becuase we are comparing against the variable 'od550aer'
        # i used to put this output into the dir 'AOD_incl_dust', but have now renamed this to 'AOD' for simplicity
        attrs_dict = {'Author': 'Alistair Duffey, University College London, alistair.duffey.21@ucl.ac.uk',
                      'Date':'October 2024',
                      'Model':'UKESM1.0',
                      'Simulation design':'Branched from SSP2-4.5 in 2035, with injection of 12Tg SO2 total across two injection locations per year',
              }
        ds = ds.assign_attrs(attrs_dict)
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        print('saving:')
        print(outpath)
        ds.to_netcdf(outpath+'/AOD_{y}_{m}_{r}.nc'.format(y=year, m=month, r=run))

