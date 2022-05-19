#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 09:19:17 2022

@author: lzhou
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import os

folder = '/home/lzhou/tcrm/output/guangdong_v2/process'

df_loc = pd.read_csv(os.path.join(folder,'origin_lon_lat'),skiprows=1,names=['lon','lat','LSflag'])
df_year = pd.read_csv(os.path.join(folder,'origin_year'),skiprows=1,names=['year'])
df = pd.concat([df_loc,df_year],axis=1)
#%%
wp= df[(df.lon>=102) & (df.lon<=184) & (df.lat>=2) &(df.lat<=30)]
#%%

fq = wp.value_counts('year').to_frame(name='frequency').reset_index().sort_values(by='year')
#%%
fig,ax = plt.subplots()
ax=sns.barplot(x='year',y='frequency',data=fq)
ax.set_xticks(np.arange(6,138,10))
#%%
df_loc = gpd.GeoDataFrame(df_loc, geometry=gpd.points_from_xy(df_loc.Lon, df_loc.Lat), \
                          crs="epsg:4326")

    
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
    