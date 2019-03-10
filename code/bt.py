# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 08:41:42 2019

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
files = [i for i in os.listdir("../data/mipas_blabeled_2009")]
    #initialize empty arrays
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
r,c = np.triu_indices(142,1)

for file in files:

  ct = 0
  mipas_file = h5py.File(os.path.join('../data/mipas_blabeled_2009', file), "r")
  radiance_l = mipas_file["radiance"][:]
  htang_l = mipas_file["htang"][:]
  time_l = mipas_file["time"][:]
  lon_l = mipas_file["longitude"][:]
  lat_l = mipas_file["latitude"][:]
  wave_min = mipas_file["wave_min"][:]
  confidence_bc = mipas_file["confidence_bc"][:]
  labels_bc = mipas_file["labels_bc"][:]
  date = file.split("_")[2]+"_"+file.split("_")[3]
  for i in range(0, radiance_l[:, 0].size-1):
    ci_idx = calculate_ci(radiance_l[i])
    # print(ci_idx)
    if htang_l[i] >=15 and htang_l[i] <=30:
      if ci_idx >= 0.5 and ci_idx <= 4.5:
        rad = radiance_l[i, :].reshape(1, 142)
        lat_r = lat_l[i].reshape(1,1)
        lon_r = lon_l[i].reshape(1,1)
        time_r = time_l[i].reshape(1,1)
        htang_r = htang_l[i].reshape(1,1)
        rad_app = np.append(rad_app, rad, 0)
        lat_app = np.append(lat_app, lat_r, 0)
        lon_app = np.append(lon_app, lon_r, 0)
        time_app = np.append(time_app, time_r, 0 )
        htang_app = np.append(htang_app, htang_r, 0 )
        #append CI
        ci_idx_a = np.atleast_1d(ci_idx)
        ci_idx_a_r = ci_idx_a.reshape(1, 1)
        ci_idx_app = np.append(ci_idx_app, ci_idx_a_r, 0)
        #append BTDs windows
        bt = BT((abs(rad_app[ct, :]) * (1e-9)), wave_min[:])
        bt_a_r = bt.reshape(1, 142)
        bt_app = np.append(bt_app, bt_a_r, 0)
        ct += 1
  mipas_file.close()
#save to file 
  directory = '../data/mipas_blabeled_2009/2009_bt'
  if not os.path.exists(directory):
    os.makedirs(directory)
  new_file = h5py.File(os.path.join(directory, date + '_bt.h5'), "w")
  new_file.create_dataset('bt', data=bt_app)
  new_file.close()
  ci_idx_app = np.empty([0,1])
  rad_app = np.empty([0,142])
  lat_app = np.empty([0,1])
  lon_app = np.empty([0,1])
  time_app = np.empty([0,1])
  htang_app = np.empty([0,1])
  bt_app = np.empty([0,142])
  
