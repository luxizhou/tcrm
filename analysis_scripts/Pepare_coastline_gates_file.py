#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:07:43 2022

@author: lzhou
"""

#import geopandas as gpd
import pandas as pd



infile = r'/home/lzhou/GIS/Coastline_gates.csv'
data = pd.read_csv(infile)
data.drop(columns='distance',inplace=True)
data.reset_index()
#%%
ofile = r'/home/lzhou/tcrm/input/Coastline_gates.csv'
data.to_csv(ofile,float_format='%.2f',header=False)