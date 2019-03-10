# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 15:59:24 2019

@author: rocco
"""
#import libraries
import os
import h5py
import numpy as np
#instantiate arrays
rad_app = np.empty([0,142])
labels_app = np.empty([0,1])
htang_app = np.empty([0,1])
radius_app = np.empty([0,1])
features_app = np.empty([0,7])
features_scaled_app = np.empty([0,7])
btd_app_difference = np.empty([0,10011])
#btd_app_difference_scaled = np.empty([0,10011])#check files in directory
files = [i for i in os.listdir("../data/csdb_blabeled_reinhold_features/") if i.endswith(".h5")]
#load one by one
for file in files:
    old_file = h5py.File( os.path.join('../data/csdb_blabeled_reinhold_features/',  file), "r")
    labels_app = np.append(labels_app, old_file["labels"][:], 0)
    btd_app_difference = np.append(btd_app_difference, old_file["btd_complete"][:], 0)
#    btd_app_difference_scaled = np.append(btd_app_difference_scaled, old_file["btd_complete_scaled"][:], 0)
    features_app = np.append(features_app, old_file["features"][:], 0)
    features_scaled_app = np.append(features_scaled_app, old_file["features_scaled"][:], 0)
    htang_app = np.append(htang_app, old_file["htang"][:], 0)
    rad_app = np.append(rad_app, old_file["radiance"][:], 0)
    radius_app = np.append(radius_app, old_file["radius"][:], 0)

    old_file.close()
#new file 
new_file = h5py.File( "../data/csdb_new/csdb_complete.h5", "w")
new_file.create_dataset('labels', data=labels_app)
new_file.create_dataset('radiance', data=rad_app)
new_file.create_dataset('radius', data=radius_app)
new_file.create_dataset('htang', data=htang_app)
new_file.create_dataset('features', data=features_app)
new_file.create_dataset('features_scaled', data=features_scaled_app)
new_file.create_dataset('btd_complete', data=btd_app_difference)
#new_file.create_dataset('btd_complete_scaled', data=btd_app_difference_scaled)
new_file.close()



    