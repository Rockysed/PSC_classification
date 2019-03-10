# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 10:27:51 2018

@author: 754672
"""
#import libraries

import h5py
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.decomposition import PCA
from sklearn import svm
import os
import pandas as pd
#import csdb data

#new_file = h5py.File("../data/csdb_blabeled_reinhold_features/csdb_reinhold_features_correct_btd_complete.h5", "r")
new_file = h5py.File("../data/csdb_blabeled_reinhold_features/csdb_radius_gaussnoise_complete.h5", "r")

#load features

btd_complete_scaled = new_file["btd_complete_scaled"][:]

#load labels

labels = new_file['labels'][:]

#close file

new_file.close()

#random forest classifier

#init rfc

forest = RFC(n_jobs=-1, n_estimators=100)

#fit data

forest.fit(btd_complete_scaled, labels)

#retrieve feature importance

importances = forest.feature_importances_

indices_rf = importances.argsort()[-50:]

#extract selected btds

btd_selected_rf = btd_complete_scaled[:, indices_rf]

#instantiate and fit pca

pca = PCA(n_components=10)

pc = pca.fit_transform(btd_selected_rf)

pca.explained_variance_ratio_

#instantiate an SVM (with htang)
clf = svm.SVC()

clf.fit(pc, labels.ravel())

files = [i for i in os.listdir("../data/mipas_pd")]

for file in files:
    #SVM classifier only PC
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd_scaled')
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    pc_t = pca.transform(df_data[indices_rf])
    labels_svm_pc = clf.predict(pc_t)
    df_reduced = df_reduced.assign(labels_svm_pc=labels_svm_pc)
    df_reduced.to_hdf(os.path.join('../data/mipas_pd', file), key='df_reduced',
          format='table')
    #Other classifiers...
 
#instantiate an SVM (with htang)
clf_h = svm.SVC()



clf_h.fit(pc, labels.ravel())

files = [i for i in os.listdir("../data/mipas_pd")]

for file in files:
    #SVM classifier only PC
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd_scaled')
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    pc_t = pca.transform(df_data[indices_rf])
    labels_svm_pc = clf.predict(pc_t)
    df_reduced = df_reduced.assign(labels_svm_pc=labels_svm_pc)
    df_reduced.to_hdf(os.path.join('../data/mipas_pd', file), key='df_reduced',
          format='table')
    #Other classifiers...
