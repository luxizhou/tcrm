#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:47:16 2022

@author: lzhou
"""

import os
import numpy as np
#import pandas as pd
#import geopandas as gpd
import netCDF4 as nc
import matplotlib.pyplot as plt
import seaborn as sns
import cartopy.crs as ccrs
import pickle

import scipy.stats as stats
from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns

'''
## example script to go through hierachies in nc file:
def walktree(top):
    values = top.groups.values() 
    yield values
    for value in top.groups.values():
        for children in walktree(value):
            yield children
            
for children in walktree(rootgrp):
    for child in children:
            print(child)
            
## example script to load data from groups 
trackfile = os.path.join(trackdir,files[0])
rootgrp = nc.Dataset(trackfile,'r')
dt = rootgrp.groups['tracks'].groups['tracks-0032'].variables['time']
data = rootgrp.groups['tracks'].groups['tracks-0032'].variables['track']            
        
'''
            
outdir = r'/home/lzhou/tcrm/output'

figdir = r'/home/lzhou/tcrm/analysis_scripts/figures'
casename = 'guangdong'
figname = 'Genesis_Map_' + casename
trackdir = os.path.join(outdir, casename,'tracks')
genesisFile = os.path.join(trackdir,'origins.pkl')

'''
#%% extrac genesis location and save to pickle file

files = os.listdir(trackdir)

orig_lat = []
orig_lon = []

idx = 0
tot_files = len(files)
for file in files:
    #print(file)
    trackfile = os.path.join(trackdir,file)
    rootgrp = nc.Dataset(trackfile,'r')
    for tt in rootgrp.groups['tracks'].groups.keys():
        #print(tt)
        data = rootgrp.groups['tracks'].groups[tt].variables['track']
        #lat = data[:]['Latitude']
        #lon = data[:]['Longitude']
        orig_lat.append(data[0]['Latitude'])
        orig_lon.append(data[0]['Longitude'])
    idx+=1
    if np.mod(idx,100) == 0:
        perc = idx/tot_files*100
        print('progress: %0.0f%%' %perc)

# save genesis location to .pkl file
origins = np.array([orig_lon,orig_lat])
#filename = os.path.join(trackdir,'origins.pkl')
f = open(genesisFile,'wb') 
pickle.dump(origins,f)
pickle.dump(orig_lon,f)
f.close()

'''

#%% test load
s = open(genesisFile,'rb') 
values = pickle.load(s)
xmin = values[0,:].min(); ymin = values[1,:].min(); 
xmax = values[0,:].max(); ymax = values[1,:].max()
X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([X.ravel(),Y.ravel()])
kernel = stats.gaussian_kde(values)

# Very tricky step: tune the pdf for 'closer' simulation to historical genesis points
# if no tuning, skip the line below or just pass kernel.covariance_factor(). 
# if tuning, pass a bandwidth, recommend do it by scale the kernel.covariance_factor() by half, one-third, etc.
# currently use a bandwith that is equal to half of the kernel. covariance_factor. ## 2022.1.21 
scaler = 2.
kernel.set_bandwidth(kernel.covariance_factor()/scaler)
#%%

Z = np.reshape(kernel(positions).T, X.shape)
#%%
#central_longitude=(xmin+xmax)/2.

fig,ax = plt.subplots()
#ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
#fig.set_size_inches(20,10)
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.05)
#ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r)
im=ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[xmin, xmax, ymin,ymax])
#ax.coastlines()
#ax.set_xticks([ymin,ymax], crs=ccrs.PlateCarree())
ax.text(160,28,'Gaussian PDF Bandwidth:')
ax.text(160,24, 'covariance factor / '+str(scaler))
fig.colorbar(im,cax=cax, orientation='vertical')
fig.set_size_inches(8,6)
ofile = os.path.join(figdir,figname)
fig.savefig(ofile)


