# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 13:20:09 2019

@author: rocco
"""
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
pca = PCA(n_components=10)

pc = pca.fit_transform(btd_sel)
pc_h = np.hstack([pc, htang])

scaler_1 = MinMaxScaler()
scaler_2 = MinMaxScaler()

pc = scaler_1.fit_transform(pc)
"""
print("RF complete")
#clf = svm.SVC(kernel = "linear", probability = True)
#clf = svm.SVC(kernel = "rbf", gamma = "auto", probability = True)
clf = svm.SVC(kernel = "rbf", gamma = 1, C = 10, probability = True)

clf.fit(pc_scaled, labels.ravel())
print("SVM1 fit complete")

files = [i for i in os.listdir("../data/mipas_pd")]
files = files[21:22]
for file in files:
    """
    #SVM classifier only PC
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    pc_t = pca.transform(df_data[indices])
    pc_t = scaler_1.transform(pc_t)
    labels_svm  = clf.predict(pc_t)
    """
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')
    df_data = scaler.transform(df_data[range(0,10011)])
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    pc_t = pca.transform(df_data[:, indices])
    pc_t = scaler_pc.transform(pc_t)
    prob_svm = clf.predict_proba(pc_t)
index_name = ["ice", "nat", "sts mix 1", "sts mix 2", "sts mix 3"]
cl = "labels_svm_pk_pc_rf"
df_prob = pd.DataFrame()
l = []

for i in range(0, 5):
    c = np.count_nonzero(prob_svm[:, i] > 0.9)/np.count_nonzero(labels_svm == i+1)
    l.append(c)
    

my_path = "../progetti/probabilities/new/"
df_prob = pd.read_hdf(os.path.join(my_path, "table_prob" + '.h5'),'df_table')
df_prob[cl] = l
l.clear()
df_prob["psc_type"] = index_name
df_prob = df_prob.set_index("psc_type")
if not os.path.exists(my_path):
    os.makedirs(my_path)
df_prob.to_hdf(os.path.join(my_path, "table_prob" + '.h5'), key='df_table',
          format='table')