# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 14:08:03 2019

@author: rocco
"""

import h5py
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.decomposition import PCA
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.preprocessing import MinMaxScaler
import pickle
"""
#load csdb dataset

new_file = h5py.File("../data/csdb_new/csdb_complete.h5", "r")

btd_csdb = new_file["btd_complete"][:]

labels = new_file["labels"][:]

new_file.close()
#load htang
new_file = h5py.File("../data/csdb_new/csdb_complete.h5", "r")
htang = new_file["htang"][:]
new_file.close()
#option: merge all STS mixes in one label
#labels[((labels == 4) | (labels == 5))] = 3
#instantiate RF classifier
forest = RFC(n_jobs=-1, n_estimators=100)

#fit data

forest.fit(btd_csdb, labels.ravel())

#retrieve feature importance

importances = forest.feature_importances_

f_n = normalize(importances.reshape(1,-1), norm='max')
#indices_rf = importances.argsort()[-50:]

#extract selected btds

#btd_selected_rf = btd_complete[:, indices_rf]

#select features with importance above 10% of the maximum
indices = np.where(f_n>0.1)[1]

#btd_sel = btd_csdb_scaled[:, indices]
btd_sel = btd_csdb[:, indices]

#clear not used var

del btd_csdb

#fit PCA 

pca = PCA(n_components=10)

pc = pca.fit_transform(btd_sel)

#clear not used var

del btd_sel

scaler_1 = MinMaxScaler()

pc = scaler_1.fit_transform(pc)

#save principal components 

f = open('pc_csdb.pckl', 'wb')
pickle.dump(pc, f)
f.close()
"""
#grid search

parameters = [
  #{'C': [1, 10, 100, 1000], 'kernel': ['linear']},
  {'C': [1, 10, 100, 1000, 10000], 'gamma': [0.0001, 0.001, 0.01, 0.1, 1, 10, "auto", "scale"], 'kernel': ['rbf']},
  #{'C': [1, 10, 100, 1000], 'gamma': [0.0001, 0.001, 0.01, 0.1, 1], 'kernel': ['poly']}
]

svc = svm.SVC()

clf = GridSearchCV(svc, parameters, cv=5)

clf.fit(pc, labels.ravel())
"""
f = open('grid_svm_rbf.pckl', 'wb')
pickle.dump(clf, f)
f.close()
"""