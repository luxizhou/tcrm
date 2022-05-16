#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 10:57:11 2022

@author: lzhou
"""

import os
import numpy as np
import pandas as pd
import netCDF4 as nc
from Utilities import track

#%% readin hstorical data
infile = r'/home/lzhou/tcrm/output/guangdong/process/origin_lon_lat'
hist_orig = pd.read_csv(infile)
#%%

folder = r'/home/lzhou/tcrm/output/guangdong/tracks/'
files = os.listdir(folder)
track_files = [f for f in files if 'tracks' in f]
#%%
#lat = np.array([])
#lon = np.array([])
#lat = np.array(tracks[0].Latitude[0])
#lat = [-9999]
lat = []
lon = []
#lon = tracks[0].Longitude[0]]
for ff in track_files:
    print(ff)
    infile = os.path.join(folder,ff)
    tracks = track.ncReadTrackData(infile)
    for ii in np.arange(0,len(tracks)):
        lat.append(tracks[ii].Latitude[0])
        lon.append(tracks[ii].Longitude[0])
    
    