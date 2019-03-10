# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 16:07:26 2019

@author: rocco
"""

#script to compute min and max of MIPAS BTDs (a posteriori apprach)
import h5py
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.feature_selection import VarianceThreshold

def get_minmax(df):
    max_array = np.empty([0])
    min_array = np.empty([0])
    for i in range(0, 10011):
        v_max = df[i].max()
        v_min = df[i].min()
        max_array = np.append(max_array, v_max)
        min_array = np.append(min_array, v_min)
    return max_array, min_array

files = [i for i in os.listdir("../data/mipas_pd")]
files = files[19:24]
for file in files:
    #SVM classifier only PC
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')

new_file = h5py.File("../data/csdb_new/csdb_complete.h5", "r")
btd_csdb = new_file["btd_complete"][:]
labels = new_file["labels"][:]
new_file.close()

selector = VarianceThreshold(threshold=100)
mipas_var_sel = selector.fit_transform(df_data.iloc[:, 0:10011])
ind = selector.get_support()

df_mipas_var_sel = pd.DataFrame(mipas_var_sel)
csdb_var_sel = btd_csdb[:, ind]
df_csdb_var_sel = pd.DataFrame(csdb_var_sel)
var_mipas = df_mipas_var_sel.var()
var_csdb = df_csdb_var_sel.var()
mean_mipas = df_mipas_var_sel.mean()
mean_csdb = df_csdb_var_sel.mean()

#instantiate an SVM (with htang)
clf = svm.SVC()
clf.fit(csdb_var_sel, labels.ravel())

files = [i for i in os.listdir("../data/mipas_pd")]
files = files[19:24]
for file in files:
    #SVM classifier only PC
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    mipas_var_sel = selector.fit_transform(df_data.iloc[:, 0:10011])
    labels_svm = clf.predict(mipas_var_sel)
    df_reduced = df_reduced.assign(labels_svm_var=labels_svm)
    df_reduced.to_hdf(os.path.join('../data/mipas_pd', file), key='df_reduced',
          format='table')