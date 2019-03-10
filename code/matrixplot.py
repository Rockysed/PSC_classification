# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 15:03:20 2019

@author: rocco
"""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib as mpl

def plotmatrix(p, bins_date):
    x_lims = [bins_date[0], bins_date[-1]]
    x_lims = mdates.date2num(x_lims)
    y_lims = [0, 2]
    fig, ax = plt.subplots()
    cax = ax.matshow(p, extent = [x_lims[0], x_lims[1],  y_lims[0], y_lims[1]], 
         aspect='auto',)
    fig.colorbar(cax)
    ax.xaxis_date()
    date_format = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(date_format)
    ax.set_yticklabels(['STS', 'NAT', 'ICE'])
#p is the hist to be plotted, cl is True considering all clouds together
def plotmatrix_psc(p, bins_date, cl):
    cmap = plt.cm.Spectral
    cmap = cmap.reversed()
    cmap.set_under(color="w")
    if cl == True:
        norm = mpl.colors.Normalize(vmin=100000, vmax=20000000)
    else:    
        #norm = mpl.colors.Normalize(vmin=100000, vmax=16000000)  
        bounds = [100000, 200000, 300000, 500000, 700000, 1000000, 2000000, 3000000, 5000000, 7000000, 10000000, 13000000, 16000000]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    x_lims =  [bins_date[0], bins_date[-1]]
    x_lims = mdates.date2num(x_lims)
    y_lims = [0, 5]
    fig, ax = plt.subplots()
    cax = ax.matshow(p, extent = [x_lims[0], x_lims[1],  y_lims[0], y_lims[1]], 
         aspect='auto', origin = 'lower', norm = norm, cmap=cmap)
    cbar = fig.colorbar(cax, format='%.1e')
    #cbar.set_clim(0, 10000000)
    ax.xaxis_date()
    date_format = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(date_format)
    ax.set_yticklabels(['15 [km]', '18 [km]', '21 [km]', '24 [km]', '27 [km]', '30 [km]'])
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    
def plotmatrix_psc_count(p, bins_date):
    x_lims = [bins_date[0], bins_date[-1]]
    x_lims = mdates.date2num(x_lims)
    y_lims = [0, 5]
    fig, ax = plt.subplots()
    norm = mpl.colors.Normalize(vmin=1, vmax=200)
    cmap = plt.cm.Spectral
    cmap = cmap.reversed()
    cmap.set_under(color="w")
    cax = ax.matshow(p, extent = [x_lims[0], x_lims[1],  y_lims[0], y_lims[1]], 
         aspect='auto', origin = 'lower', norm = norm, cmap=cmap)
    #cbar.set_clim(0, 10000000)
    ax.xaxis_date()
    cbar = fig.colorbar(cax)
    date_format = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(date_format)
    ax.set_yticklabels(['15 [km]', '18 [km]', '21 [km]', '24 [km]', '27 [km]', '30 [km]'])
 #   manager = plt.get_current_fig_manager()
 #   manager.window.showMaximized()