#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 11:45:06 2022

@author: lzhou
"""

import os 
#import numpy as np
#import pandas as pd
#import geopandas as gpd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


#%%
outdir = r'/home/lzhou/tcrm/output'
figdir = r'/home/lzhou/tcrm/analysis_scripts/figures'

casename = 'guangdong'
figname = 'Hazard_Map_' + casename

hazfile = os.path.join(outdir,casename,'hazard','hazard.nc')
data = xr.open_dataset(hazfile)

# mask out negative values. The reason for negative values should be found!
data_masked = data.where(data['wspd']>0.)
#%%
rps = [5., 10., 20., 50., 100., 200., 250., 500., 1000.]
#fig = plt.figure()
fig = plt.figure(figsize=(12,12))
idx = 1
for rp in rps:
    ax = fig.add_subplot(3,3,idx,projection=ccrs.PlateCarree())
    ax.coastlines()
    data_masked.wspd.sel(ari=rp).plot(x="lon",y='lat', \
                                      cbar_kwargs={'label':'Average Wind Speed [m/s]'}, \
                                          robust=True,cmap='Oranges',ax=ax)
    ax.set_title('Return Period of %d Years'%rp)
    #ax.set_title('Average Recurrence Interval at %d Years'%rp)
    #fig.tight_layout()
    idx+=1
    
fig.suptitle('Case: '+casename)
fig.tight_layout()
fig.savefig(os.path.join(figdir,figname))