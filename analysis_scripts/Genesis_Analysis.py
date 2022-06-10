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

from Utilities.track import ncReadTrackData
from mpl_toolkits.axes_grid1 import make_axes_locatable

from statsmodels.nonparametric.kernel_density import KDEMultivariate
#from StatInterface import KDEOrigin

case_name = 'china_since1979'

simu_folder = os.path.join('/home/lzhou/tcrm/output',case_name,'process','simulated_origins')
hist_folder = os.path.join('/home/lzhou/tcrm/output',case_name,'process')
plot_folder = os.path.join('/home/lzhou/tcrm/analysis_scripts/figures',case_name)
#%% extract genesis points and save to file
'''
folder = r'/home/lzhou/tcrm/output/china_since1979/tracks'
output_dir = r'/home/lzhou/tcrm/output/china_since1979/process/simulated_origins'

if os.path.isdir(output_dir) == False:
    os.mkdir(output_dir)
    
#files = os.listdir(folder)
#files.sort()

trackFiles = os.listdir(folder)
files = [f for f in trackFiles if 'nc' in f]
files.sort()

#fq_simu = pd.DataFrame(columns=['Freq'])
for ii in np.arange(0,len(files)):
    if np.mod(ii,10)==0:
        print('Process trackfile: ', files[ii])
    df_simu = pd.DataFrame(columns=['lon','lat','year'])

    infile = os.path.join(folder,files[ii])
    tracks = ncReadTrackData(infile)    
    for track in tracks:
        df_simu.loc[len(df_simu)]=[track.Longitude[0],track.Latitude[0],ii]

    df_simu['year'] = df_simu['year'].astype(int)
    fname = files[ii][:-3] + '.csv'
    outfile = os.path.join(output_dir,fname)
    df_simu.to_csv(outfile,index=False,float_format="%.2f")
'''
#%% Historical data
df_loc = pd.read_csv(os.path.join(hist_folder,'origin_lon_lat'),skiprows=1,names=['lon','lat','LSflag'])
df_year = pd.read_csv(os.path.join(hist_folder,'origin_year'),skiprows=1,names=['year'])
df = pd.concat([df_loc,df_year],axis=1)
fq = df.value_counts('year').to_frame(name='frequency').reset_index().sort_values(by='year')
#%% plot frequency
fig1,axes = plt.subplots(2,1,sharex=True)
sns.histplot(fq.frequency,binwidth=1,kde=True,ax=axes[0])

#%% calculate pdf of the origin location
# initiate kernel
data = df[['lon','lat']].values
#bw = KDEOrigin.getOriginBandwidth(data)
kde = KDEMultivariate(data,bw='cv_ml',var_type='cc')
bw = kde.bw
# prepare grids
xmin = np.floor(df.lon.min()); xmax = np.ceil(df.lon.max()); 
ymin = np.floor(df.lat.min()); ymax = np.ceil(df.lat.max());
#X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
X, Y = np.mgrid[xmin:xmax+1, ymin:ymax+1]
positions = np.vstack([X.ravel(),Y.ravel()])
#%% evaluate pdf
pdf = kde.pdf(data_predict=positions)
#%% plot
Z = np.reshape(pdf.T, X.shape)
fig,ax = plt.subplots(2,1,sharex=True)

divider = make_axes_locatable(ax[0])
cax = divider.append_axes('right', size='5%', pad=0.05)
im = ax[0].imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[xmin, xmax, ymin, ymax])
#ax[0].text(150,28,"Gaussian PDF Bandwidth [lat,lon]:")
#ax[0].text(150,24," {:.2f}, {:.2f}".format(bw[0],bw[1]))
#ax.text(200,24, 'covariance factor / '+str(scaler))
fig.colorbar(im,cax=cax, orientation='vertical')
#fig.set_size_inches(8,6)


#%% simulated data
files = os.listdir(simu_folder)
files.sort()

simu_fq = pd.DataFrame(columns=['Year','Count'])
sdata = pd.read_csv(os.path.join(simu_folder,files[0]))
sarray = sdata[['lon','lat']].values
simu_fq.loc[len(simu_fq),:]=[0,len(sdata)]

idx = 1
for fn in files[1:]: 
    if (np.mod(idx,100) == 0):
        print('processing file: ',fn)
    sdata = pd.read_csv(os.path.join(simu_folder,fn))
    sarray1 = sdata[['lon','lat']].values
    sarray = np.vstack([sarray, sarray1])
    simu_fq.loc[len(simu_fq),:]=[0,len(sdata)]
    idx +=1    
#%%
simu_fq['Count'] = simu_fq.Count.astype('int')
sns.histplot(simu_fq.Count,binwidth=1,kde=True,ax=axes[1])
figname = 'Compare_Genesis_Frequency.png'
ofile = os.path.join(plot_folder,figname)
plt.savefig(ofile)
#%% initiate kernel
simu_kde2 = KDEMultivariate(sarray,bw=bw,var_type='cc')
#%% evaluate pdf
simu_pdf2 = simu_kde2.pdf(data_predict=positions)
#%% plot
Z = np.reshape(simu_pdf2.T, X.shape)
divider = make_axes_locatable(ax[1])
cax = divider.append_axes('right', size='5%', pad=0.05)
im2 = ax[1].imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[xmin, xmax, ymin, ymax])
fig.colorbar(im,cax=cax, orientation='vertical')
#fig.set_size_inches(8,6)

figname = 'Compare_Genesis_Location.png'
ofile = os.path.join(plot_folder,figname)
plt.savefig(ofile)

