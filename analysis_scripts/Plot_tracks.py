#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 13:28:31 2022

@author: lzhou
"""

import os
import geopandas as gpd
from Utilities.track import ncReadTrackData
import matplotlib.pyplot as plt
import numpy as np
#%%
caseName ='china_since1979_coarse_grid'
trackPath =  os.path.join('/home/lzhou/tcrm/output',caseName,'tracks')
plotPath = os.path.join('/home/lzhou/tcrm/analysis_scripts/figures/',caseName)

if os.path.isdir(plotPath) == False:
    os.mkdir(plotPath)

trackFiles = os.listdir(trackPath)
files = [f for f in trackFiles if 'nc' in f]
files.sort()
#%%
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
cn_shape = world[world.name=='China'].copy()
cn_shape.reset_index(drop=True,inplace=True)
#%%
''' 
# plot one track file
fig,ax = plt.subplots(figsize=(6,6))
cn_shape.boundary.plot(ax=ax)
infile = os.path.join(trackPath, trackFiles[10])
tracks = ncReadTrackData(infile)
for track in tracks:
    plt.plot(track.Longitude,track.Latitude)

figname = trackFiles[0][:-3] + '.png'
ofile = os.path.join(plotPath,figname)
fig.savefig(ofile)
'''
#%%
ii = 0
for trackFile in files:
    if np.mod(ii,10)==0:
        print(trackFile)
        
    fig,ax = plt.subplots(figsize=(6,6))
    cn_shape.boundary.plot(ax=ax)
    infile = os.path.join(trackPath, trackFile)
    tracks = ncReadTrackData(infile)
    for track in tracks:
        plt.plot(track.Longitude,track.Latitude)

    figname = trackFile[:-3] + '.png'
    ofile = os.path.join(plotPath,figname)
    fig.savefig(ofile)
    plt.close(fig)
    
    ii +=1
    
