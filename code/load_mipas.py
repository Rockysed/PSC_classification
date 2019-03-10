# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 14:47:22 2018

@author: 754672
"""

import numpy as np
from netCDF4 import Dataset
import h5py
import os

#PART 1: Loading the data
#iterate over files
files = [i for i in os.listdir("../data/mipas/2010") if i.endswith(".nc")]
#initialize empty arrays
for file in files:
    dataset = Dataset(os.path.join('../data/mipas/2010', file))
    dataset_psc = Dataset(os.path.join('../data/classification/psc_mipas', 'psc_' + file))
    # init at every iteration
    lat_l = np.empty([0,1])
    lon_l = np.empty([0,1])
    time_l = np.empty([0,1])
    radiance_l = np.empty([0,142])
    htang_l = np.empty([0,1])
    wave_min_l = np.empty([0,1])
    wave_max_l = np.empty([0,1])
    cl_l = np.empty([0,1])
    conf_l = np.empty([0,3])      
    #latitude
    lat = dataset.variables['latitude'][:]
    lat_l_r = lat.reshape(-1, 1)
    lat_l = np.append(lat_l, lat_l_r, 0)
    #longitude
    lon = dataset.variables['longitude'][:]
    lon_l_r = lon.reshape(-1, 1)
    lon_l = np.append(lon_l, lon_l_r, 0)
    #time
    time = dataset.variables['time'][:]
    time_l_r = time.reshape(-1, 1)
    time_l = np.append(time_l, time_l_r, 0)
    #radiance
    radiance = dataset.variables['radiance'][:]
    radiance_l_r = radiance.reshape(-1, 142)
    radiance_l = np.append(radiance_l, radiance_l_r, 0)
    #htang
    htang = dataset.variables['htang'][:]
    htang_l_r = htang.reshape(-1, 1)
    htang_l = np.append(htang_l, htang_l_r, 0)
    #wave_min
    wave_min = dataset.variables['wave_min'][:]
    #wave_max
    wave_max = dataset.variables['wave_max'][:]
    #Bayesian Classifier Labels
    cl = dataset_psc.variables['class'][:]
    cl_l_r = cl.reshape(-1, 1)
    cl_l = np.append(cl_l, cl_l_r, 0)
    #Bayesian Classifier Confidence
    conf = dataset_psc.variables['confidence'][:]
    conf = conf[:, 0:3]
    conf_l_r = conf.reshape(-1, 3)
    conf_l = np.append(conf_l, conf_l_r, 0)
    #close dataset
    dataset.close()
    dataset_psc.close()
    #save to a new file 
    file_w_e = os.path.splitext(file)[0]
    new_file = h5py.File(os.path.join('../data/mipas_blabeled_2010', 'new_' + file_w_e), 'w')
    new_file.create_dataset('labels_bc', data=cl_l)
    new_file.create_dataset('confidence_bc', data=conf_l)    
    new_file.create_dataset('latitude', data=lat_l)
    new_file.create_dataset('longitude', data=lon_l)
    new_file.create_dataset('wave_min', data=wave_min)
    new_file.create_dataset('wave_max', data=wave_max)
    new_file.create_dataset('htang', data=htang_l)
    new_file.create_dataset('time', data=time_l)
    new_file.create_dataset('radiance', data=radiance_l)
    
    new_file.close()

    
