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

# Historical data
folder = '/home/lzhou/tcrm/output/guangdong_v2/process'
df_loc = pd.read_csv(os.path.join(folder,'origin_lon_lat'),skiprows=1,names=['lon','lat','LSflag'])
df_year = pd.read_csv(os.path.join(folder,'origin_year'),skiprows=1,names=['year'])
df = pd.concat([df_loc,df_year],axis=1)
wp= df[(df.lon>=102) & (df.lon<=184) & (df.lat>=2) &(df.lat<=30)]
fq = wp.value_counts('year').to_frame(name='frequency').reset_index().sort_values(by='year')
#%%
#fq_cn_1979= fq.copy()
fq_gd = fq.copy()

#%% plot frequency
fig,ax = plt.subplots()
ax=sns.barplot(x='year',y='frequency',data=fq)
ax.set_xticks(np.arange(1,43,10))
#%% plot genesis origin PDF map 
