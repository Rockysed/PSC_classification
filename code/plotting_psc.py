# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:48:58 2019

@author: rocco
"""
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pandas as pd
import os

"""
Definition function to plot psc, df is a pandas dataframe, i = 0 if Northern Emisphere, i = 1 if Southern Emisphere
title, classifier_type = [labels_bc, labels_svm_pc]
"""
def plot_psc(df, i, title, classifier_type):
    if i == 1:
        ax = plt.axes(projection=ccrs.Orthographic(0, -90))
    else:
        ax = plt.axes(projection=ccrs.Orthographic(0, 90))
    ax.coastlines(resolution='10m')
    ax.gridlines()   
    if classifier_type == "labels_bc":
        markers = ['s', 's', '^', 'o', 'D', 'v', '>']
        colors = ['w', 'b', 'r', 'chartreuse', 'cyan', 'goldenrod', 'steelblue']
        edges = ['k', 'b', 'r', 'chartreuse', 'cyan', 'goldenrod', 'steelblue']
        labels = ['unspec.', 'ICE', 'NAT', 'STSmix', 'ICE_NAT', "NAT_STS", "ICE_STS"]
        for j in range (7):
            plt.scatter(df[df["labels_bc"]==j]["lon"] , df[df["labels_bc"]==j]["lat"], c = colors[j], s=40 \
                        , marker=markers[j], transform=ccrs.Geodetic(), label=labels[j], edgecolors=edges[j])
    else:
        markers = ['s', '^', 'o', 'D', 'v']
        colors = ['b', 'r', 'chartreuse', 'chartreuse', 'chartreuse']
        labels = ['ICE', 'NAT', 'STS_1', 'STS_2', 'STS_3']
        for j in range (0, 5):
            plt.scatter(df[df[classifier_type]==j+1]["lon"] , df[df[classifier_type]==j+1]["lat"], c = colors[j], s=40 \
                        , marker=markers[j], transform=ccrs.Geodetic(), label=labels[j])
    

    if i == 1:
        ax.set_extent([-180, 180, -60, -90], crs=ccrs.PlateCarree())
    else:
        ax.set_extent([-180, 180, 60, 90], crs=ccrs.PlateCarree())  
    plt.plot()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title(title)
    
#dates to be considered  
"""
dates = ["2003-05-23", "2003-06-05", "2003-06-09", "2003-06-11", "2003-06-12", "2003-06-15", "2008-05-28" \
          , "2008-05-29",  "2008-05-30",  "2008-05-31",  "2008-06-01",  "2008-06-02", "2007-01-25", "2011-01-07" \
          , "2007-07-08", "2008-07-25", "2008-08-29"]
"""
"""
dates = ["2003-05-23", "2003-06-05", "2003-06-09", "2003-06-11", "2003-06-12", "2003-06-15", "2008-05-28" \
          , "2008-05-29",  "2008-05-30",  "2008-05-31",  "2008-06-01",  "2008-06-02", "2007-01-25", "2011-01-07" \
          , "2007-07-08", "2008-07-25", "2008-08-29"]
"""
dates = ["2009-05-23", "2009-06-14", "2009-06-24", "2009-07-24", "2009-08-26"]
#Minumum and maximum tangent height
#classifier type
#classifier_type = "labels_svm_kpca_red"
#classifier_type = "labels_svm_lk_pc_rf_scale_v1"
classifier_type = "labels_bc"
if classifier_type == "labels_svm_lk_pc_rf_scale_v1":
    cl_type = "SVM (RF + PCA)"
if classifier_type == "labels_svm_kpca":
    cl_type = "SVM (KPCA)"  
if classifier_type == "labels_svm_auto":
    cl_type = "SVM (autoenc)" 
if classifier_type == "labels_bc":
    cl_type = "Bayesian cl."
#cycle on dates

#df = (df_may_2003[(df_may_2003['htang'] > htang_min)  & (df_may_2003['htang'] < htang_max)]).loc[dates[0]]

for date in dates:
    year = date.split("-")[0]
    month = date.split("-")[1]
    day = date.split("-")[2]
    c_date = year + month + day
    df = pd.read_hdf( '../data/mipas_pd/' + year + '_' + month + '_prova.h5','df_reduced', where=['index == c_date'])
    bins = ([(14, 16), (16, 18), (18, 22), (21.2, 26.8)])
    for k in range(0, len(bins)):
        df_binned = df[(df["htang"] > bins[k][0]) & (df["htang"] < bins[k][1])]
        if df_binned.shape[0] > 0:
            if df_binned["lat"].mean() < 0:
                i = 1
            else: i = 0
            title = "PSC plot date: " + date + " Altitude range: " + str(bins[k][0]) + "-" + str(bins[k][1]) + " [km]" + "\n using " + cl_type     
            plot_psc(df_binned, i, title, classifier_type)
            my_path = "../progetti/test_plots_specific_days/new/" + cl_type
            if not os.path.exists(my_path):
                os.makedirs(my_path)
            my_file =  date + "_v2" + str(k) +".png"
            plt.savefig(os.path.join(my_path, my_file))
            plt.close()
    


#plt.scatter(df[df["labels_bc"] == 2]["lat"] , df[df["labels_bc"] == 2]["lon"], marker = markers[2], s=20, color='r', transform=ccrs.Geodetic())