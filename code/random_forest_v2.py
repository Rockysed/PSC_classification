# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:49:22 2019

@author: rocco
"""

import h5py
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.decomposition import PCA
from sklearn import svm
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
#import csdb data

#new_file = h5py.File("../data/csdb_blabeled_reinhold_features/csdb_reinhold_features_correct_btd_complete.h5", "r")
new_file = h5py.File( '../data/csdb_new/csdb_complete.h5', "r")
#load features

btd_complete = new_file["btd_complete"][:]

#load labels

labels = new_file['labels'][:]

#close file

new_file.close()

#random forest classifier

#init rfc

forest = RFC(n_jobs=-1, n_estimators=100)

#fit data

forest.fit(btd_complete, labels.ravel())

#retrieve feature importance

importances = forest.feature_importances_

f_n = normalize(importances.reshape(1,-1), norm='max')
#indices_rf = importances.argsort()[-50:]

#extract selected btds

#btd_selected_rf = btd_complete[:, indices_rf]

#select features with importance above 10% of the maximum

btd_sel = btd_complete[:, np.where(f_n>0.1)[1]]

del btd_complete