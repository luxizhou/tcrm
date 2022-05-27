#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 13:22:45 2022

@author: lzhou
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

#%% Get list of CMA stations

stations = pd.read_csv('/home/lzhou/Precipitation/Data/CMA_Historical_Data/Wind_Rainfall/China_Sta.csv')
stations['lat'] = stations['lat'].apply(lambda x: float(x[:2])+int(x[3:5])/60.)
stations['long'] = stations['long'].apply(lambda x: float(x[:3])+int(x[4:6])/60.)
stations.rename(columns={"long": "lon"},inplace=True)

#%% Read in CMA wind data

gust_file = '/home/lzhou/Precipitation/Data/CMA_Historical_Data/Wind_Rainfall/1949-2018_Gust.csv'
gale_file = '/home/lzhou/Precipitation/Data/CMA_Historical_Data/Wind_Rainfall/1949-2018_Wind.csv'

def Read_CMA_Wind_Data(filename):
    gust = pd.read_csv(filename,names=['SerialID','TC_Number','StationID','Speed','Direction','Time'])
    # remove rows with no time stamp
    gust['Time_len'] = gust['Time'].apply(lambda x: len(x))      
    gust = gust[gust.Time_len>1]
    # convert time
    gust['Time'] = pd.to_datetime(gust['Time'])
    gust['DayNum'] = gust['Time'].apply(lambda x: x.toordinal())
    
    return gust
  
gust = Read_CMA_Wind_Data(gust_file)
gale = Read_CMA_Wind_Data(gale_file)

#%%

df1=gust.SerialID.value_counts().to_frame(name='Count_by_Gust')
df2=gale.SerialID.value_counts().to_frame(name='Count_by_Gale')
events = pd.merge(df1,df2,left_index=True,right_index=True,how='outer')
events['Total'] = events.sum(axis=1)
events = events.sort_values(by='Total',ascending=False)

df3 = gust.StationID.value_counts().to_frame(name='Count_by_Gust')
df4 = gale.StationID.value_counts().to_frame(name='Count_by_Gale')
events2 = pd.merge(df3,df4,left_index=True,right_index=True,how='outer')
events2['Total'] = events2.sum(axis=1)
events2 = events2.sort_values(by='Total',ascending=False)
plot_stations = pd.merge(stations,events2,left_on='StationID',right_index=True,how='inner')
print(plot_stations.lat.min(),plot_stations.lat.max(),plot_stations.lon.min(),plot_stations.lon.max())

#%%
infile = r'/home/lzhou/Precipitation/Precipitation_Scripts/Output/CMA_Best_Tracks.csv'
tracks = pd.read_csv(infile)
                                       
                                                                           


#%%

run_case = '2013_Fitow_ZJ'

outdir = '/home/lzhou/tcrm/output'

track_files = os.listdir(os.path.join(outdir,run_case,'process','timeseries'))
for track_file in track_files:
    #track_file = track_files[0] 
    df = pd.read_csv(os.path.join(outdir,run_case,'process','timeseries',track_file))
    df['Time'] = pd.to_datetime(df['Time'])
    df['DayNum'] = df['Time'].apply(lambda x: x.toordinal())
    sid = df.Station.iloc[0]
    init_day = df.DayNum.min()
    end_day = df.DayNum.max()
    
    gust_data = gust[(gust.StationID==sid)&(gust.DayNum>=init_day)&(gust.DayNum<=end_day)]
    gale_data = gale[(gale.StationID==sid)&(gale.DayNum>=init_day)&(gale.DayNum<=end_day)]
    
    if gust_data.empty == False or gale_data.empty== False:
        fig,ax = plt.subplots()
        df.plot(x='Time',y='Speed',label='Model',ax=ax)
    
    if gust_data.empty == False:
        print('Gust: ', track_file)
        gust_data.plot(x='Time',y='Speed',linestyle='',marker='o', color='r', markersize=6,label='CMA Gust',ax=ax)
     
    if gale_data.empty == False:
        print('Gale: ', track_file)
        gale_data.plot(x='Time',y='Speed',linestyle='',marker='o', color='b', markersize=6,label='CMA Gale',ax=ax)  
   
    if gust_data.empty == False or gale_data.empty== False:
        plt.legend()