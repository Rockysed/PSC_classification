# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 12:03:31 2019

@author: rocco
"""
#open coincidence file and load variables
import os
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import datetime
files = [i for i in os.listdir("../data/mipas_pd")]
#files = files[19:24]
files = files[21:22]
ind_arr = np.empty([0,1])
ind = np.empty([0,1])
ind_cal = np.empty([0,1])
lab_cl = np.empty([0,1])
lab_cl_2 = np.empty([0,1])
lab_cl_3 = np.empty([0,1])


for file in files:
    #load mipas df
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    s0 = df_reduced.shape[0]
    cl_max_class = np.ones(s0)*(-1)
    cl_dense = np.ones(s0)*(-1)
    df_reduced = df_reduced.assign(cal_max_cl=cl_max_class)
    df_reduced = df_reduced.assign(caliop_class=cl_max_class)
    df_reduced = df_reduced.assign(caliop_class_dense=cl_dense)
    #load coinc data
    file_coinc = "coinc_MipCalV2_" +file.split("_")[0] +file.split("_")[1] + "_main.nc"
    dataset = Dataset("../data/classification/coinc/" + file_coinc)
    cal_max_cl = dataset["caliop_max_class"][:]
    caliop_class = dataset["caliop_class"][:]
    nclass_cal4mip = dataset["nclass_cal4mip"][:]
    htang_caliop = dataset["htang"][:]
    time_caliop = dataset.variables["time"][:]
    lat_caliop = dataset["latitude"][:]
    lon_caliop = dataset["longitude"][:]
    dataset.close()
    ind_arr = np.empty([0,1])
    ind_cal = np.empty([0,1])
    for i in range(0, len(caliop_class)):
        if (nclass_cal4mip[i, :].max() )/ nclass_cal4mip[i, :].sum() > 0.7:
                cl_dense[i] = np.argmax(nclass_cal4mip[i, :], axis=0)
    for i in range(0, len(caliop_class)):
        if time_caliop[i]>0:
            ind = np.where((df_reduced.time >= (datetime.datetime.fromtimestamp(time_caliop[i]) - datetime.timedelta(milliseconds = 500)).timestamp()) & (df_reduced.time <= (datetime.datetime.fromtimestamp(time_caliop[i]) + datetime.timedelta(milliseconds = 500)).timestamp()))[0]
            if len(ind) == 1:
                ind_arr = np.vstack([ind_arr, ind])
                ind_cal = np.vstack([ind_cal, i])
    for j in range(0, len(ind_arr)):
        q_r = np.arange(ind_arr[j]- 5, ind_arr[j]+ 5)
        if np.count_nonzero((abs(df_reduced.iloc[q_r, :].htang - htang_caliop[int(ind_cal[j])])< 0.5) & (abs(df_reduced.iloc[q_r, :].lat - lat_caliop[int(ind_cal[j])])< 2) \
         & (abs(df_reduced.iloc[q_r, :].lon - lon_caliop[int(ind_cal[j])])< 2) == True) != 0:
            id_l = int(np.where((abs(df_reduced.iloc[q_r, :].htang - htang_caliop[int(ind_cal[j])])< 0.5) & (abs(df_reduced.iloc[q_r, :].lat - lat_caliop[int(ind_cal[j])])< 2) \
             & (abs(df_reduced.iloc[q_r, :].lon - lon_caliop[int(ind_cal[j])])< 2) == True)[0][0] + q_r.min())
            print(id_l)
            lab_cl = np.vstack([lab_cl, caliop_class[j]])
            df_reduced.iloc[id_l, :].caliop_class = caliop_class[j]
            lab_cl_2 = np.vstack([lab_cl_2, cal_max_cl[j]])
            df_reduced.iloc[id_l, :].cal_max_cl = cal_max_cl[j]
            lab_cl_3 = np.vstack([lab_cl_3, cl_dense[j]])
            df_reduced.iloc[id_l, :].caliop_class_dense = cl_dense[j]           
    df_reduced.to_hdf(os.path.join('../data/mipas_pd', file), key='df_reduced',
          format='table')