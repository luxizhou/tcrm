#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:02:06 2022

@author: lzhou
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime as dt

track_file = r'/home/lzhou/Precipitation/Precipitation_Scripts/Output/CMA_Best_Tracks.csv'
tracks = pd.read_csv(track_file)
#%%
track = tracks[tracks.CMAID==201325].copy()
print(track.Name.iloc[1])
#track.plot(x='LON',y='LAT')

print_track = track[['Time', 'LAT', 'LON', 'PRES']].copy().reset_index(drop=True)
print_track['Time'] = pd.to_datetime(print_track['Time'])
print_track['Time'] = print_track['Time'].dt.strftime("%Y%m%d%H")
print_track['Index'] = 0
print_track.Index.iloc[0] = 1


