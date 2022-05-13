#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 15:04:51 2022

@author: lzhou
"""

#import numpy as np
import pandas as pd
from TrackGenerator import TrackGenerator,trackSize
#from TrackGenerator import TrackGenerator
#from Utilities import metutils
#%%
# Read in best track data
infile = r'/home/lzhou/tcrm/input/ibtracs.ALL.list.v04r00.csv'
data = pd.read_csv(infile,usecols=[0,1,2,3,5,6,8,9,10,11,12,15,16,19,20,23,24,40])

# Only use tracks in West Pacific
data = data[data.BASIN=='WP']

# Read in RMW
data['RMW_string_length'] = data['USA_RMW'].apply(lambda x: len(x))
data=data[data.RMW_string_length>1]
data['USA_RMW'] = data['USA_RMW'].astype("float") # unit:nmile
data['USA_RMW'] = data['USA_RMW'] * 1.852 # convert from nmile to km

#%% Lat/Lon
data['USA_LAT'] = data['USA_LAT'].astype("float")
data['USA_LON'] = data['USA_LON'].astype("float")
#%% Pressure data
data['PRES_string_length'] = data['USA_PRES'].apply(lambda x: len(x))
data=data[data.PRES_string_length>1]
data['USA_PRES'] = data['USA_PRES'].astype("float") # unit:mb

# Convert time column to datetime type
data['Time'] = pd.to_datetime(data['ISO_TIME'])

# only keep the first character in IFLAG as only USA_RMW is used for RMW 
data['USA_IFLAG'] = data['IFLAG'].apply(lambda x: x[0])

# only keep the original records, discard interpolated records
data = data[data['USA_IFLAG'].str.contains('O')]
#%% Read in mslp file for extracting Penv, unit: hPa
mslpFile = r'/home/lzhou/tcrm/MSLP/slp.day.ltm.nc'
mslpVar = 'slp'
mslp = TrackGenerator.SamplePressure(mslpFile,var=mslpVar)

for index, row in data.iterrows():
    #period = pd.Period(print_track['Time'].iloc[ii],freq='H')
    period = pd.Period(row['Time'],freq='D')
    data.loc[index,'DoY'] = period.dayofyear
    coords = data[['DoY','USA_LAT','USA_LON']].loc[index].to_numpy().reshape(3,1)
    data.loc[index,'Penv'] = mslp.get_pressure(coords)
#%% find duplicated rows
#duplicate_time = data[data.duplicated(['ISO_TIME'],keep=False)]
#%%
data['dp'] = data['Penv'] - data['USA_PRES']
#test = data['IFLAG'].apply(lambda x: x[0])
#%% find coefficient to fit
#penv = mslp.get_pressure(np.array([[123],[20],[130]]))

