# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 10:01:55 2019

@author: rocco
"""

import numpy as np
import pandas as pd
import h5py
import os
from sklearn.preprocessing import StandardScaler
import datetime
from dateutil.relativedelta import relativedelta
from pysolar.solar import *

#load MIPAS files
def date2string(t): 
    delta = relativedelta(years=30)
    return (datetime.datetime.fromtimestamp(t)+delta).strftime("%Y-%m-%d")

def calculate_ci(x):
    return x[137]/x[138]
# function to calculate the NI


def calculate_ni(x):
    return x[139]/x[137]
#function to calculate the btd


def BT(rad, wave):
    return 1.438786 * wave / np.log((1.19106e-12 * wave * wave * wave + rad) / rad)

#cycle over arrays
h5f = h5py.File("../data/csdb/csdb_stacked_radius.h5", "r")

labels_csdb = h5f["labels"][:]
#radiance = h5f["radiance"][:]
wave_min = h5f["wave_min"][:]
wave_max = h5f["wave_max"][:]
htang = h5f["htang"][:]
radius = h5f["radius"][:]

h5f.close()

h5f = h5py.File("../data/csdb/csdb_gaussnoise.h5", "r")

radiance = h5f["csdb_gaussnoise"][:]

h5f.close()

labels = labels_csdb
#index_0 = np.random.choice(labels.shape[0], 70000, replace=False)
#index_0 = np.random.choice(labels.shape[0], 10000, replace=False)
#radiance_l = radiance[index_0,:]
radiance_l = radiance    #initialize empty arrays

rad_app = np.empty([0,142])
lat_app = np.empty([0,1])
lon_app = np.empty([0,1])
time_app = np.empty([0,1])
htang_app = np.empty([0,1])
bt_app = np.empty([0,142])
ci_idx_app = np.empty([0,1])
k = 0
#ct = 0
tzinfo=datetime.timezone.utc
delta = relativedelta(years=30)
  #range of dates
  #mid May
  #upper right matrix indexes


ct = 0
for i in range(0, radiance_l[:, 0].size-1):
    ci_idx = calculate_ci(radiance_l[i])
# print(ci_idx)
    if htang[i] >=15 and htang[i] <=30:
      if ci_idx >= 0.5 and ci_idx <= 4.5:
        rad = radiance_l[i, :].reshape(1, 142)
        htang_r = htang[i].reshape(1,1)
        rad_app = np.append(rad_app, rad, 0)
        htang_app = np.append(htang_app, htang_r, 0 )
        #append CI
        ci_idx_a = np.atleast_1d(ci_idx)
        ci_idx_a_r = ci_idx_a.reshape(1, 1)
        ci_idx_app = np.append(ci_idx_app, ci_idx_a_r, 0)
        #append BTDs windows
        bt = BT((abs(rad_app[ct].reshape(1, 142)) * (1e-9)), wave_min.reshape(1, 142))     
        bt_a_r = bt.reshape(1, 142)
        bt_app = np.append(bt_app, bt_a_r, 0)
        ct += 1
#save to file 
  
directory = '../data/csdb_bt'
if not os.path.exists(directory):
    os.makedirs(directory)
new_file = h5py.File(os.path.join(directory  + '/csdb_bt.h5'), "w")
new_file.create_dataset('bt', data=bt_app)
new_file.close()
ci_idx_app = np.empty([0,1])
rad_app = np.empty([0,142])
lat_app = np.empty([0,1])
lon_app = np.empty([0,1])
time_app = np.empty([0,1])
htang_app = np.empty([0,1])
bt_app = np.empty([0,142])
  