# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 14:49:53 2019

@author: rocco
"""
import pandas as pd
import os
import numpy as np
import h5py
from sklearn.preprocessing import MinMaxScaler
import pickle
#define arrays
max_val = np.zeros([1,10011])
min_val = np.zeros([1,10011])
max_arr = np.zeros([1,10011])
min_arr = np.zeros([1,10011])
#compute MIPAS min and max
files = [i for i in os.listdir("../data/mipas_pd")]
files = files[19:24]

for file in files:

    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')
    df_data = df_data[range(0,10011)]
    max_val = np.asarray(df_data.max())
    min_val = np.asarray(df_data.min())
    max_arr = np.maximum(max_arr, max_val)
    min_arr = np.minimum(min_arr, min_val)

del df_data

#compute CSDB min and max
new_file = h5py.File("../data/csdb_new/csdb_complete.h5", "r")
btd_csdb = new_file["btd_complete"][:]
new_file.close()
max_val = np.amax(btd_csdb, axis=0)
min_val = np.amin(btd_csdb, axis=0)
del btd_csdb
#final min and max array
max_arr = np.maximum(max_arr, max_val)
min_arr = np.minimum(min_arr, min_val)
arr_st = np.vstack([max_arr, min_arr])
#fit scaler
scaler = MinMaxScaler()
arr_scaled = scaler.fit_transform(arr_st)
#compute MIPAS 2006 min and max
new_file = h5py.File("../data/mipas_blabeled_reinhold_features/rf_mipas_complete", "r")
btd_csdb = new_file["btd_complete"][:]
new_file.close()
max_val = np.amax(btd_csdb, axis=0)
min_val = np.amin(btd_csdb, axis=0)
del btd_csdb
#final min and max array
max_arr = np.maximum(max_arr, max_val)
min_arr = np.minimum(min_arr, min_val)
arr_st = np.vstack([max_arr, min_arr])
#fit scaler
scaler = MinMaxScaler()
arr_scaled = scaler.fit_transform(arr_st)
#save the scaler
f = open('new_min_max_scaler.pckl', 'wb')
pickle.dump(scaler, f)
f.close()
