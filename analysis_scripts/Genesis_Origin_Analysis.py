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
df = pd.read_csv(infile)
#%%
infile = r'/home/lzhou/tcrm/output/guangdong/tracks/tracks.00000.nc'
tracks = track.ncReadTrackData(infile)
lat = np.array([])
lon = np.array([])
ll = len(tracks)

for ii in np.arange(0,ll):
    lat = lat.append(tracks[ii].Latitude[0])
    lon = lon.append(tracks[ii].Longitude[0])
    
    