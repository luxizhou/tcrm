#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:38:50 2022

@author: lzhou
"""

import itertools
import pandas as pd
import numpy as np


#%%
def find_kdeStep(arr):
  
#arr = [1,2,3,4]
    #arr = speed.copy()
    diff_list = []
  
    # Get the combinations of numbers
    for n1, n2 in list(itertools.combinations(arr, 2)):
 
        # Find the absolute difference
        diff_list.append(abs(n1-n2))

    diff_list = np.array(diff_list)
    diff_list = diff_list[diff_list>0]
    print("option 1: %.1f"%min(diff_list))   
    option2 = (speed.max()-speed.min())/len(speed)
    print("option 2: %.1f"%option2)
  
    return

#%% example:

infile = r'/home/lzhou/tcrm/output/china_since1979/process/init_speed'
df = pd.read_csv(infile)
speed = df.values
print('Speed ')
find_kdeStep(speed)

infile = r'/home/lzhou/tcrm/output/china_since1979/process/init_pressure'
df = pd.read_csv(infile)
pressure = df.values
print('Pressure ')
find_kdeStep(pressure)

infile = r'/home/lzhou/tcrm/output/china_since1979/process/init_lon_lat'
df = pd.read_csv(infile)
lat = df.iloc[:,1].values
lon = df.iloc[:,0].values
print('lat ')
find_kdeStep(lat)
print('lon ')
find_kdeStep(lon)
