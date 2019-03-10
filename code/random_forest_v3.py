# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 13:20:09 2019

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
from sklearn.preprocessing import MinMaxScaler
import pickle
#load csdb dataset

new_file = h5py.File("../data/csdb_new/csdb_complete.h5", "r")

btd_csdb = new_file["btd_complete"][:]

labels = new_file["labels"][:]

new_file.close()
#load htang
new_file = h5py.File("../data/csdb_new/csdb_complete.h5", "r")
htang = new_file["htang"][:]
new_file.close()
#load scaler
filename = "minmax_scaler_mipas"
scaler = pickle.load(open(filename, 'rb'))
#scale data
btd_csdb = scale.transform(btd_csdb)
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
pca = PCA(n_components=10)

pc = pca.fit_transform(btd_sel)
"""
#pc_h = np.hstack([pc, htang])

#scaler_1 = MinMaxScaler()
#scaler_2 = MinMaxScaler()

#pc = scaler_1.fit_transform(pc)
#pc_h = scaler_2.fit_transform(pc_h)

#pca.explained_variance_ratio_
#instantiate an SVM (with htang)
print("RF complete")
#clf = svm.SVC(kernel = "rbf", gamma = "auto")
clf = svm.SVC(kernel = "rbf", gamma = "scale", C=1000)
clf.fit(pc, labels.ravel())
print("SVM1 fit complete")

#instantiate an SVM (with htang)
clf_2 = svm.SVC(kernel = "rbf", gamma = "scale", C=1000)
clf_2.fit(pc_h, labels.ravel())
print("SVM2 fit complete")

files = [i for i in os.listdir("../data/mipas_pd")]
files = files[19:24]
for file in files:
    #SVM classifier only PC
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    pc_t = pca.transform(df_data[indices])
    #pc_t = scaler_1.transform(pc_t)
    labels_svm_rk_pc = clf.predict(pc_t)
    df_reduced = df_reduced.assign(labels_svm_rk_pc_rf_noscale=labels_svm_rk_pc)
    df_reduced.to_hdf(os.path.join('../data/mipas_pd', file), key='df_reduced',
          format='table')
    
    #SVM classifier PC and htang
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    #pc_t = pca.transform(df_data[indices])
    pc_t_h = np.hstack([pc_t, np.asarray(df_data.htang).reshape(-1,1)])
    pc_t_h = scaler_2.fit_transform(pc_t_h)
    labels_svm_rk_pc_h = clf_2.predict(pc_t_h)
    df_reduced = df_reduced.assign(labels_svm_rk_pc_h_rf_3=labels_svm_rk_pc_h)
    df_reduced.to_hdf(os.path.join('../data/mipas_pd', file), key='df_reduced',
          format='table')
    """