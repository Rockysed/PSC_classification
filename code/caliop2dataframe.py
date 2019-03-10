# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 08:42:38 2019

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
"""

#open coincidence file and load variables
dataset = Dataset("../data/classification/coinc/coinc_MipCalV2_200909_main.nc")
cal_max_cl = dataset["caliop_max_class"][:]
htang_cal = dataset["htang"][:]
time_caliop = dataset.variables["time"][:]
dataset.close()
"""
#
#files = [i for i in os.listdir("../data/mipas_pd")]
#files = files[19:24]
files = [i for i in os.listdir("../data/mipas_blabeled_2009")]
    #initialize empty arrays
rad_app = np.empty([0,142])
lat_app = np.empty([0,1])
lon_app = np.empty([0,1])
time_app = np.empty([0,1])
htang_app = np.empty([0,1])
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
        ci_idx_a = np.atleast_1d(ci_idx)
        ci_idx_a_r = ci_idx_a.reshape(1, 1)
        ci_idx_app = np.append(ci_idx_app, ci_idx_a_r, 0)
        ct += 1
  mipas_file.close()
  """
#save to file 
# new_file = h5py.File(os.path.join('../data/mipas_blabeled_reinhold_features/2006_v2', date + '_prova.h5'), "w")
  new_file = h5py.File(os.path.join('C:/Users/rocco/Documents/dati_tesi/mipas/mipas_2006/', date + '_prova.h5'), "w")
  new_file.create_dataset('ci', data=ci_idx_app)
  new_file.create_dataset('ni', data=ni_app)  
  new_file.create_dataset('time', data=time_app)  
  new_file.create_dataset('sun_elev', data=sun_elev_app)
  new_file.create_dataset('btd_complete', data=btd_app_difference)
  new_file.create_dataset('btd_complete_scaled', data=btd_complete_scaled)
  new_file.create_dataset('labels_bc', data=labels_bc_app)
  new_file.create_dataset('lat', data=lat_app)
  new_file.create_dataset('lon', data=lon_app) 
  new_file.create_dataset('htang', data=htang_app)
  new_file.create_dataset('features', data=myarray_t)
  new_file.create_dataset('features_scaled', data=myarray_scaled)
  """
 #save btds to pandas dataframe
  if ci_idx_app.shape[0] > 0:
    file_df = file.split("_")[2] + "_" + file.split("_")[3] + "_prova.h5"
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file_df),'df_reduced')
    df_reduced = df_reduced.assign(time=time_app)
    df_reduced.to_hdf(os.path.join('../data/mipas_pd', file_df), key='df_reduced',
          format='table')


  #new_file.create_dataset('datetime', data=dt_app)
  """
  asciiList = [n.encode("ascii", "ignore") for n in data_list]
  new_file.create_dataset('date', (len(asciiList),1),'S10', asciiList)

  asciiList = [n.encode("ascii", "ignore") for n in dt_list]
  new_file.create_dataset('date', (len(asciiList),1),'S10', asciiList)
  """
  #new_file.close()
  ci_idx_app = np.empty([0,1])
  rad_app = np.empty([0,142])
  lat_app = np.empty([0,1])
  lon_app = np.empty([0,1])
  time_app = np.empty([0,1])
  htang_app = np.empty([0,1])
  #dt_app = np.empty([0,1])
  """time
  btd_app = np.empty([0,1])
  btd_app_1 = np.empty([0,1])
  btd_app_2 = np.empty([0,1])
  btd_app_3 = np.empty([0,1])
  btd_app_4 = np.empty([0,1])
  """
  ci_idx_app = np.empty([0,1])
