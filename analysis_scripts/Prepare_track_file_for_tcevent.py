#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:02:06 2022

@author: lzhou

Script to prepare input file for tcevent.py. The major task here is to produce radius of max. wind (RMW) as the data is not available for tracks. 

To-Do:
    1. parameterization for poci needs update based on west pacific data
    2. parameterization for RMW needs update based on west pacific data

"""

import os
import numpy as np
import pandas as pd
from datetime import datetime as dt
#from Utilities import stats
from TrackGenerator import trackSize, TrackGenerator
from Utilities.loadData import getPoci
from numpy.random import default_rng


#mslp_file = r'/home/lzhou/tcrm/input/slp.day.1981-2010.ltm.nc'
#mslpVar = 'slp'
#mslp = TrackGenerator.SamplePressure(mslp_file, var =mslpVar )
#penv = mslp.get_pressure(DoY,lat,lon)
penv = 1008.

track_file = r'/home/lzhou/Precipitation/Precipitation_Scripts/Output/CMA_Best_Tracks.csv'
tracks = pd.read_csv(track_file)
#%%
track = tracks[tracks.CMAID==201325].copy()
print(track.Name.iloc[1])
filename = str(track.Year.iloc[1])+'_'+track.Name.iloc[1]+'.csv'

#track.plot(x='LON',y='LAT')
print_track = track[['Time', 'LAT', 'LON', 'PRES','WND']].copy().reset_index()
print_track['Time'] = pd.to_datetime(print_track['Time'])
print_track['index'] = 0
print_track['index'].iloc[0] = 1

#%% assing random error to generate poci and rmw
rng=default_rng(seed=43)
print_track['poci_eps'] = rng.normal(loc=0,scale=2.5717,size=len(print_track))
print_track['RMW_eps'] = rng.normal(loc=0,scale=0.335,size=len(print_track))

#%% generate RMW
for index, row in print_track.iterrows():
    #period = pd.Period(print_track['Time'].iloc[ii],freq='H')
    period = pd.Period(row['Time'],freq='D')
    print_track.loc[index,'DoY'] = period.dayofyear
    print_track.loc[index,'Poci'] = getPoci(penv,print_track.loc[index,'PRES'],print_track.loc[index,'LAT'],print_track.loc[index,'DoY'],print_track.loc[index,'poci_eps'])
    dp = print_track.loc[index,'Poci']-print_track.loc[index,'PRES']
    print_track.loc[index,'RMW'] = trackSize.rmax(dp,print_track.loc[index,'LAT'],print_track.loc[index,'RMW_eps'])

#%% change the time format 
print_track['Time'] = print_track['Time'].dt.strftime("%Y%m%d%H")
outfile = os.path.join('/home/lzhou/tcrm/input',filename)
print_track.to_csv(outfile,float_format="%.3f",index=False)

