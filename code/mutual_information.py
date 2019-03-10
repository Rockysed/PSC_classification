# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 10:27:51 2018

@author: 754672
"""
#import libraries

import h5py
import numpy as np
from sklearn.feature_selection import mutual_info_classif

#import csdb data

new_file = h5py.File("../data/csdb_blabeled_reinhold_features/csdb_reinhold_features_correct_btd_complete.h5", "r")

#load features

btd_complete_scaled = new_file["btd_complete_scaled"][:]

#load labels

labels = new_file['labels'][:]

#close file

new_file.close()

#mutual information classifier

#init mi

feature_scores = mutual_info_classif(btd_complete_scaled, labels)

#indeces

features_scores_mi_ind = np.argpartition(feature_scores, -10)[-10:]

#retrieve feature score

feature_scores_important = feature_scores[features_scores_mi_ind]