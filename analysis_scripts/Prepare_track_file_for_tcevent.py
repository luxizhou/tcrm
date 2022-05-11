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
#from Utilities import stats
import TrackGenerator
from TrackGenerator import trackSize
from Utilities.loadData import getPoci

mslp_file = r'/home/lzhou/tcrm/input/slp.day.1981-2010.ltm.nc'

track_file = r'/home/lzhou/Precipitation/Precipitation_Scripts/Output/CMA_Best_Tracks.csv'
tracks = pd.read_csv(track_file)
#%%
track = tracks[tracks.CMAID==201325].copy()
print(track.Name.iloc[1])
#track.plot(x='LON',y='LAT')

print_track = track[['Time', 'LAT', 'LON', 'PRES']].copy().reset_index()
print_track['Time'] = pd.to_datetime(print_track['Time'])
print_track['Time'] = print_track['Time'].dt.strftime("%Y%m%d%H")
print_track['index'] = 0
print_track['index'].iloc[0] = 1

lat = print_track['LAT'].to_array()
central_pressure = print_track['PRES'].to_array()
#%%
mslp = SamplePressure(mslp_file, var =mslpVar )

penv = mslp.get_pressure(jday, lat,lon)

poci_eps = PRNG.normalvariate(0., 2.5717) #generate a random number from normal distribution with mean at 0, std=2.5717
poci = getPoci(penv, pressure, lat, jday, poci_eps)
dp = poci - pressure
rmwEps = np.random.normal(0,scale=0.335)
print_track['RMW'] = trackSize.rmax(dp, lat, rmwEps)
