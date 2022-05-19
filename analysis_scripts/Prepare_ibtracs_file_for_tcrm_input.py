#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 14:56:46 2022

@author: lzhou
"""

import pandas as pd
infile = r'/home/lzhou/tcrm/input/ibtracs.ALL.list.v04r00.csv'

df = pd.read_csv(infile,skiprows=2,usecols=[0,1,2,3,6,8,9,10,11,40], \
                 names=['tcserialno','season','num','basin','date','lat','lon','vmax','pressure','rmax'], \
                 dtype={'tcserialno':'str','season':'int','num':'int','lat':'float','lon':'float'})
#%%

#df_basin_nan = df[df.basin.isna()]
#df_wp = df[df.basin=='WP']
                  
#%%
df.to_csv('ibtracs_v40r00.csv',index=False)
