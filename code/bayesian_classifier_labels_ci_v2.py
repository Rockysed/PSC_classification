# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 13:49:48 2018

@author: 754672
"""

import numpy as np
import h5py
import os
from sklearn.preprocessing import StandardScaler

#load MIPAS files


def calculate_ci(x):
    return x[137]/x[138]
# function to calculate the NI


def calculate_ni(x):
    return x[139]/x[137]
#function to calculate the btd


def BT(rad, wave):
    return 1.438786 * wave / np.log((1.19106e-12 * wave * wave * wave + rad) / rad)

#cycle over arrays
files = [i for i in os.listdir("../data/mipas_blabeled")]
    #initialize empty arrays
rad_app = np.empty([0,142])
lat_app = np.empty([0,1])
lon_app = np.empty([0,1])
time_app = np.empty([0,1])
htang_app = np.empty([0,1])
btd_app = np.empty([0,1])
btd_app_1 = np.empty([0,1])
btd_app_2 = np.empty([0,1])
btd_app_3 = np.empty([0,1])
btd_app_4 = np.empty([0,1])
btd_app_difference = np.empty([0,10011])
ci_idx_app = np.empty([0,1])
ni_app = np.empty([0,1])
labels_bc_app = np.empty([0,1])
confidence_bc_app = np.empty([0,3])
data_list = []
k = 0
ct = 0
  #range of dates
  #mid May
  #upper right matrix indexes
r,c = np.triu_indices(142,1)

for file in files:

  mipas_file = h5py.File(os.path.join('../data/mipas_blabeled', file), "r")
  radiance_l = mipas_file["radiance"][:]
  htang_l = mipas_file["htang"][:]
  time_l = mipas_file["time"][:]
  lon_l = mipas_file["longitude"][:]
  lat_l = mipas_file["latitude"][:]
  wave_min = mipas_file["wave_min"][:]
  confidence_bc = mipas_file["confidence_bc"][:]
  labels_bc = mipas_file["labels_bc"][:]
  date = file.split("_")[2]+"_"+file.split("_")[3]
  
  #for i in range(0, radiance_l[:, 0].size-1):
  ci_idx_list = list(map(calculate_ci, radiance_l))
  htang_list  = list(filter(lambda x: x >=15 and x <=30, htang_l))
  #ci_idx_filtered = list(filter(lambda x: x >= 0.5 and x <= 4.5, ci_idx_list))
  # ci_idx_filtered = list(filter(lambda x: x >=15 and x <=30, ci_idx_list))

  
""" ci_idx = calculate_ci(radiance_l[i])
    # print(ci_idx)
    if htang_l[i] >=15 and htang_l[i] <=30:
      if ci_idx >= 0.5 and ci_idx <= 4.5:
          print(ci_idx) """
