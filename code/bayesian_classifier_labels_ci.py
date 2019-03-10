# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 16:11:09 2018

@author: 754672
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
btd_app = np.empty([0,1])
btd_app_1 = np.empty([0,1])
btd_app_2 = np.empty([0,1])
btd_app_3 = np.empty([0,1])
btd_app_4 = np.empty([0,1])
btd_app_difference = np.empty([0,10011])
ci_idx_app = np.empty([0,1])
ni_app = np.empty([0,1])
sun_elev_app = np.empty([0,1])
labels_bc_app = np.empty([0,1])
confidence_bc_app = np.empty([0,3])
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
        dt = datetime.datetime.fromtimestamp(time_r, tzinfo)+delta
        sun_elev = get_altitude(lat_r, lon_r, dt)
        sun_elev_app = np.append(sun_elev_app, sun_elev, 0)
        #append labels
        labels_bc_app = np.append(labels_bc_app, labels_bc[i].reshape(1,1), 0)
        #append confidence
        confidence_bc_app = np.append(confidence_bc_app, confidence_bc[i, :].reshape(1, 3), 0)
        #append CI
        ci_idx_a = np.atleast_1d(ci_idx)
        ci_idx_a_r = ci_idx_a.reshape(1, 1)
        ci_idx_app = np.append(ci_idx_app, ci_idx_a_r, 0)
        #append NI
        ni_r = calculate_ni(radiance_l[i])
        ni_a = np.atleast_1d(ni_r)
        ni_a_r = ni_a.reshape(1, 1)
        ni_app = np.append(ni_app, ni_a_r, 0)
        #append BTDs windows
        btd_r_difference = BT((abs(rad_app[ct, r]) * (1e-9)), wave_min[r]) - BT(abs(rad_app[ct, c] * (1e-9)),  wave_min[c])
        btd_a_r_difference = btd_r_difference.reshape(1, 10011)
        btd_app_difference = np.append(btd_app_difference, btd_a_r_difference, 0)
        #BTDs Reinhold
        btd_r = BT((abs(rad_app[ct,140])*(1e-9)), 833) - BT(abs(rad_app[ct,141]*(1e-9)), 949)
        btd_a = np.atleast_1d(btd_r)
        btd_a_r = btd_a.reshape(1, 1)
        btd_app = np.append(btd_app, btd_a_r, 0)
        #append brightness difference BT 820-831
        btd_r_1 = BT((abs(rad_app[ct,38])*(1e-9)), 820) - BT(abs(rad_app[ct,49]*(1e-9)), 831)
        btd_a_1 = np.atleast_1d(btd_r_1)
        btd_a_r_1 = btd_a_1.reshape(1, 1)
        btd_app_1 = np.append(btd_app_1, btd_a_r_1, 0)
        #append brightness difference BT 1406-960
        btd_r_2 = BT((abs(rad_app[ct,101])*(1e-9)), 1406) - BT(abs(rad_app[ct,79]*(1e-9)), 960)
        btd_a_2 = np.atleast_1d(btd_r_2)
        btd_a_r_2 = btd_a_2.reshape(1, 1)
        btd_app_2 = np.append(btd_app_2, btd_a_r_2, 0)
        #append brightness difference BT 831-1225
        btd_r_3 = BT((abs(rad_app[ct,49])*(1e-9)), 831) - BT(abs(rad_app[ct,85]*(1e-9)), 1225)
        btd_a_3 = np.atleast_1d(btd_r_3)
        btd_a_r_3 = btd_a_3.reshape(1, 1)
        btd_app_3 = np.append(btd_app_3, btd_a_r_3, 0)
        #append brightness difference BT 960-1225
        btd_r_4 = BT((abs(rad_app[ct,79])*(1e-9)), 960) - BT(abs(rad_app[ct,85]*(1e-9)), 1225)
        btd_a_4 = np.atleast_1d(btd_r_4)
        btd_a_r_4 = btd_a_4.reshape(1, 1)
        btd_app_4 = np.append(btd_app_4, btd_a_r_4, 0)
        ct += 1
  mipas_file.close()
  if btd_app_difference.shape[0] > 0:
    btd_complete_scaled = StandardScaler().fit_transform(btd_app_difference)
#save to file  
  features = [ci_idx_app, ni_app, btd_app, btd_app_1, btd_app_2, btd_app_3, btd_app_4]
  myarray = np.asarray(features)
  myarray = myarray.reshape(7, -1)
  myarray_t = myarray.transpose()
  if myarray_t.shape[0] > 0:
   myarray_scaled = StandardScaler().fit_transform(myarray_t)
  list_date = list(map(date2string, time_app.ravel()))
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
   df_btd = pd.DataFrame(btd_app_difference)
   df_btd["ci"]=ci_idx_app
   df_btd["ni"]=ni_app
   df_btd["lon"]=lon_app
   df_btd["lat"]=lat_app
   df_btd["sun_elev"]=sun_elev_app
   df_btd["htang"]=htang_app
   df_btd["labels_bc"]=labels_bc_app
   df_btd['date'] = pd.to_datetime(list_date)
   df_btd = df_btd.set_index(['date'])
   df_btd.to_hdf(os.path.join('../data/mipas_pd', date + '_prova.h5'), key='df_btd', mode='w') 
   #save scaled btds to pandas dataframe
   df_btd_scaled = pd.DataFrame(btd_complete_scaled)
   df_btd_scaled["ci"]=ci_idx_app
   df_btd_scaled["ni"]=ni_app
   df_btd_scaled["lon"]=lon_app
   df_btd_scaled["lat"]=lat_app
   df_btd_scaled["sun_elev"]=sun_elev_app
   df_btd_scaled["htang"]=htang_app
   df_btd_scaled["labels_bc"]=labels_bc_app
   df_btd_scaled['date'] = pd.to_datetime(list_date)
   df_btd_scaled = df_btd_scaled.set_index(['date'])
   df_btd_scaled.to_hdf(os.path.join('../data/mipas_pd', date + '_prova.h5'), key='df_btd_scaled')
   #save features to pandas dataframe
   df_features = pd.DataFrame(myarray_t)
   df_features["ci"]=ci_idx_app
   df_features["ni"]=ni_app
   df_features["lon"]=lon_app
   df_features["lat"]=lat_app
   df_features["sun_elev"]=sun_elev_app
   df_features["htang"]=htang_app
   df_features["labels_bc"]=labels_bc_app
   df_features['date'] = pd.to_datetime(list_date)
   df_features = df_features.set_index(['date'])
   df_features.to_hdf(os.path.join('../data/mipas_pd', date + '_prova.h5'), key='df_features',
          format='table')
   #save scaled features to pandas dataframe
   df_features_scaled = pd.DataFrame(myarray_scaled)
   df_features_scaled["ci"]=ci_idx_app
   df_features_scaled["ni"]=ni_app
   df_features_scaled["lon"]=lon_app
   df_features_scaled["lat"]=lat_app
   df_features_scaled["sun_elev"]=sun_elev_app
   df_features_scaled["htang"]=htang_app
   df_features_scaled["labels_bc"]=labels_bc_app
   df_features_scaled['date'] = pd.to_datetime(list_date)
   df_features_scaled = df_features_scaled.set_index(['date'])
   df_features_scaled.to_hdf(os.path.join('../data/mipas_pd', date + '_prova.h5'), key='df_features_scaled',
          format='table')
   #save lon lat htang sun_elev ci ni date and labels_bc
   df_reduced = pd.DataFrame(ci_idx_app, columns = ["ci"])
   df_reduced["ni"]=ni_app
   df_reduced["lon"]=lon_app
   df_reduced["lat"]=lat_app
   df_reduced["sun_elev"]=sun_elev_app
   df_reduced["htang"]=htang_app
   df_reduced["labels_bc"]=labels_bc_app
   df_reduced['date'] = pd.to_datetime(list_date)
   df_reduced = df_reduced.set_index(['date'])
   df_reduced.to_hdf(os.path.join('../data/mipas_pd', date + '_prova.h5'), key='df_reduced',
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
  """
  btd_app = np.empty([0,1])
  btd_app_1 = np.empty([0,1])
  btd_app_2 = np.empty([0,1])
  btd_app_3 = np.empty([0,1])
  btd_app_4 = np.empty([0,1])
  """
  btd_app_difference = np.empty([0,10011])
  btd_app = np.empty([0,1])
  btd_app_1 = np.empty([0,1])
  btd_app_2 = np.empty([0,1])
  btd_app_3 = np.empty([0,1])
  btd_app_4 = np.empty([0,1])
  ci_idx_app = np.empty([0,1])
  ni_app = np.empty([0,1])
  sun_elev_app = np.empty([0,1])
  labels_bc_app = np.empty([0,1])
  confidence_bc_app = np.empty([0,3])
        #append brightness difference BT
"""
        btd_r = BT((abs(rad_app[ct,140])*(1e-9)), 833) - BT(abs(rad_app[ct,141]*(1e-9)), 949)
        btd_a = np.atleast_1d(btd_r)
        btd_a_r = btd_a.reshape(1, 1)
        btd_app = np.append(btd_app, btd_a_r, 0)
        #append brightness difference BT 820-831
        btd_r_1 = BT((abs(rad_app[ct,38])*(1e-9)), 820) - BT(abs(rad_app[ct,49]*(1e-9)), 831)
        btd_a_1 = np.atleast_1d(btd_r_1)
        btd_a_r_1 = btd_a_1.reshape(1, 1)
        btd_app_1 = np.append(btd_app_1, btd_a_r_1, 0)
        #append brightness difference BT 1406-960
        btd_r_2 = BT((abs(rad_app[ct,101])*(1e-9)), 1406) - BT(abs(rad_app[ct,79]*(1e-9)), 960)
        btd_a_2 = np.atleast_1d(btd_r_2)
        btd_a_r_2 = btd_a_2.reshape(1, 1)
        btd_app_2 = np.append(btd_app_2, btd_a_r_2, 0)
        #append brightness difference BT 831-1225
        btd_r_3 = BT((abs(rad_app[ct,49])*(1e-9)), 831) - BT(abs(rad_app[ct,85]*(1e-9)), 1225)
        btd_a_3 = np.atleast_1d(btd_r_3)
        btd_a_r_3 = btd_a_3.reshape(1, 1)
        btd_app_3 = np.append(btd_app_3, btd_a_r_3, 0)
        #append brightness difference BT 960-1225
        btd_r_4 = BT((abs(rad_app[ct,79])*(1e-9)), 960) - BT(abs(rad_app[ct,85]*(1e-9)), 1225)
        btd_a_4 = np.atleast_1d(btd_r_4)
        btd_a_r_4 = btd_a_4.reshape(1, 1)
        btd_app_4 = np.append(btd_app_4, btd_a_r_4, 0)
        #append BTDs windows
        btd_r_difference = BT((abs(rad_app[ct, r]) * (1e-9)), wave_min[r]) - BT(abs(rad_app[ct, c] * (1e-9)),  wave_min[c])
        btd_a_r_difference = btd_r_difference.reshape(1, 10011)
        btd_app_difference = np.append(btd_app_difference, btd_a_r_difference, 0)
        #data list
        data_list.append(date)
        ct += 1
  mipas_file.close()

features_csdb = [ci_idx_app, ni_app, btd_app, btd_app_1, btd_app_2, btd_app_3, btd_app_4]
myarray = np.asarray(features_csdb)
myarray = myarray.reshape(7, -1)
myarray_t = myarray.transpose()
myarray_scaled = StandardScaler().fit_transform(myarray_t)
btd_complete_scaled = StandardScaler().fit_transform(btd_app_difference)

#save to file
new_file = h5py.File(os.path.join('../data/mipas_blabeled_reinhold_features', 'rf_mipas_radiance'), "w")
new_file.create_dataset('features', data=myarray_t)
new_file.create_dataset('features_scaled', data=myarray_scaled)
new_file.create_dataset('btd_complete', data=btd_app_difference)
new_file.create_dataset('btd_complete_scaled', data=btd_complete_scaled)
new_file.create_dataset('labels_bc', data=labels_bc_app)
new_file.create_dataset('confidence_bc', data=confidence_bc_app)
asciiList = [n.encode("ascii", "ignore") for n in data_list]
new_file.create_dataset('date', (len(asciiList),1),'S10', asciiList)
new_file.close()
"""