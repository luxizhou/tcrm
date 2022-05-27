#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 24 17:04:38 2022

@author: lzhou
"""

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
from TrackGenerator import trackSize, TrackGenerator
from Utilities.loadData import getPoci
from numpy.random import default_rng


mslp_file = r'/home/lzhou/tcrm/MSLP/slp.day.ltm.nc'
mslpVar = 'slp'
mslp = TrackGenerator.SamplePressure(mslp_file, var =mslpVar )

#%%
track_file = r'/home/lzhou/Precipitation/Precipitation_Scripts/Output/CMA_Best_Tracks.csv'
tracks = pd.read_csv(track_file)

#%%
track = tracks[tracks.CMAID>=200000].copy()
track = track.reset_index(drop=True)
print(track.Name.iloc[1])
filename = 'CMA_tracks_since_2000.csv'
#%%
track['Index']=0
cmaid = track.CMAID.iloc[0]
track['Index'].iloc[0]=1
for ii in np.arange(1,len(track)):
    if track['CMAID'].iloc[ii] != cmaid:
        cmaid = track['CMAID'].iloc[ii]
        track['Index'].iloc[ii]=1

#%%
#track.plot(x='LON',y='LAT')
print_track = track[['Index','Time', 'LAT', 'LON', 'PRES','WND']].copy().reset_index(drop=True)
print_track['Time'] = pd.to_datetime(print_track['Time'])


#%% assing random error to generate poci and rmw
rng=default_rng(seed=43)
print_track['poci_eps'] = rng.normal(loc=0,scale=2.5717,size=len(print_track))
print_track['RMW_eps'] = rng.normal(loc=0,scale=0.335,size=len(print_track))

#%% generate RMW
for index, row in print_track.iterrows():
    #period = pd.Period(print_track['Time'].iloc[ii],freq='H')
    period = pd.Period(row['Time'],freq='D')
    print_track.loc[index,'DoY'] = period.dayofyear
    aa = np.array([[print_track.loc[index,'DoY']],[print_track.loc[index,'LAT']],[print_track.loc[index,'LON']]])
    print_track.loc[index,'Penv'] = mslp.get_pressure(aa)
    print_track.loc[index,'Poci'] = getPoci(print_track.loc[index,'Penv'],print_track.loc[index,'PRES'],print_track.loc[index,'LAT'],print_track.loc[index,'DoY'],print_track.loc[index,'poci_eps'])
    dp = print_track.loc[index,'Poci']-print_track.loc[index,'PRES']
    print_track.loc[index,'RMW'] = trackSize.rmax(dp,print_track.loc[index,'LAT'],print_track.loc[index,'RMW_eps'])

#%% change the time format 
print_track['Time'] = print_track['Time'].dt.strftime("%Y%m%d%H")
outfile = os.path.join('/home/lzhou/tcrm/input',filename)
print_track.to_csv(outfile,float_format="%.3f",index=False)

