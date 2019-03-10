# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 12:09:25 2019

@author: rocco
"""
#import libraries
import numpy as np
import pandas as pd
import h5py
import datetime
from dateutil.relativedelta import relativedelta
#import data
new_file = h5py.File('C:/Users/rocco/Documents/dati_tesi/mipas/mipas_2006/2006_07_prova.h5', "r")
lon = new_file["lon"][:]
lat = new_file["lat"][:]
htang = new_file["htang"][:]
labels_bc = new_file["labels_bc"][:]
time = new_file["time"][:]
new_file.close()
#define time shift
#define function that converts timestamp to string
def date2string(t): 
    delta = relativedelta(years=30)
    return (datetime.datetime.fromtimestamp(t)+delta).strftime("%Y-%m-%d")
#map to list
list_date = list(map(date2string, time.ravel()))
#string date
#str_date = "2006-07-24"
#list_index = list(filter(lambda x: list_date[x]== str_date, range(len(list_date))))
#create a data matrix: longitude, latitude, labels_bc, altitude
#data_matrix = np.hstack([lon[list_index], lat[list_index], labels_bc[list_index], htang[list_index]])
#select data with altitude condition
data_matrix = np.hstack([lon, lat, labels_bc, htang])
date = pd.to_datetime(list_date)
df = pd.DataFrame(data_matrix)
df['date'] = date
df = df.set_index(['date'])
#select date range
df_sel = df.loc['2006-7-4':'2006-7-6']
#select min and max altitude
h_min = 20
h_max = 25
df_sel_h = df_sel[(df_sel[3] > h_min) & (df_sel[3] < h_max)]
#data_matrix_selected = data_matrix[(data_matrix[:,3]>h_min) & (data_matrix[:,3]<h_max), :]
"""
#definition function to plot psc, df is a pandas dataframe, i = 0 if Northern Emisphere, i = 1 if Southern Emisphere
def plot_psc(df, i):
    if i == 1:
        ax = plt.axes(projection=ccrs.Orthographic(0, -90))
    else:
        ax = plt.axes(projection=ccrs.Orthographic(0, 90))
    ax.coastlines(resolution='10m')
    ax.gridlines()   
    plt.scatter(df["lon"] , df["lat"], c = df["labels_bc"], s=20,\
                 cmap=plt.cm.Spectral, transform=ccrs.Geodetic())
    if i == 1:
        ax.set_extent([-180, 180, -60, -90], crs=ccrs.PlateCarree())
    else:
        ax.set_extent([-180, 180, 60, 90], crs=ccrs.PlateCarree())        
#plot (Southern Emisphere)

ax = plt.axes(projection=ccrs.Orthographic(0, -90))
ax.coastlines(resolution='10m')
ax.gridlines()
#plt.scatter(data_matrix_selected[:, 0], data_matrix_selected[:, 1], c = data_matrix_selected[:, 2], s=10, cmap=plt.cm.Spectral, transform=ccrs.Geodetic())
plt.scatter(df_sel_h[0], df_sel_h[1], c = df_sel_h[2],\
            s=10, cmap=plt.cm.Spectral, transform=ccrs.Geodetic())
ax.set_extent([-180, 180, -60, -90], crs=ccrs.PlateCarree())
"""
