# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:45:09 2019

@author: rocco
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 12:24:57 2019

@author: rocco
"""
import h5py
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.decomposition import KernelPCA
from sklearn import svm
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle

#load csdb dataset
new_file = h5py.File("../data/csdb_new/csdb_complete.h5", "r")
btd_csdb = new_file["btd_complete"][:]
labels = new_file["labels"][:]
htang = new_file["htang"][:]
new_file.close()
#load kpca
filename = "model_kpca_btd_scaled"
loaded_model = pickle.load(open(filename, 'rb'))
#load minmax sclaer
filename = "minmax_scaler_mipas"
scaler = pickle.load(open(filename, 'rb'))
#scale CSDB
btd_csdb_scaled = scaler.transform(btd_csdb)
#transform using kpca
"""
def compute_kpca(btd, model):
    kpc_stack = np.empty([0, 7])
    dim_data = btd.shape[0]
    #loop and if
    for i in range (0, int(dim_data/5000)):
        kpc = model.transform(btd[(i*5000):((i*5000)+5000), :])
        kpc_stack = np.vstack([kpc_stack, kpc])
        print("chunking: ", i , " of: ", int(dim_data/5000))
    if dim_data%5000 != 0:
        i = i + 1
        kpc = model.transform(btd[(i*5000):((i*5000)+dim_data%5000), :])
        kpc_stack = np.vstack([kpc_stack, kpc])
    return kpc_stack
"""
def compute_kpca(btd, model):
    if isinstance(btd, pd.DataFrame):
        kpc_stack = np.empty([0, 7])
        dim_data = btd.shape[0]
        i = 0
        #loop and if
        for i in range (0, int(dim_data/5000)):
            kpc = model.transform(btd.iloc[(i*5000):((i*5000)+5000), range(0,10011)])
            kpc_stack = np.vstack([kpc_stack, kpc])
            print("chunking: ", i , " of: ", int(dim_data/5000))
        if dim_data%5000 != 0:
            if i != 0: 
                i = i + 1
            kpc = model.transform(btd.iloc[(i*5000):((i*5000)+5000), range(0,10011)])
            kpc_stack = np.vstack([kpc_stack, kpc])
            print("chunking: ", i , " of: ", int(dim_data/5000))
        return kpc_stack
#load btd
df_csdb = pd.DataFrame(btd_csdb_scaled)
#transform btd
kpc_stack = compute_kpca(df_csdb, loaded_model)
kpc_stack_h = np.hstack([kpc_stack, htang])
"""
#svm classifier kpc
clf = svm.SVC(kernel = "linear")
clf.fit(kpc_stack, labels.ravel())
"""

#svm classifier kpc + htang
clf_h = svm.SVC(kernel = "linear")
clf_h.fit(kpc_stack_h, labels.ravel())
#classify MIPAS data
files = [i for i in os.listdir("../data/mipas_pd")]
files = files[19:24]
for file in files:
    """
    #SVM classifier KPCA
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')
    df_data = df_data.iloc[:, range(0, 10011)]
    df_data[df_data.columns] = scaler.transform(df_data[df_data.columns])
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    kpc = compute_kpca(df_data, loaded_model)
    labels_svm_kpca = clf.predict(kpc)
    df_reduced = df_reduced.assign(labels_svm_kpca=labels_svm_kpca)
    df_reduced.to_hdf(os.path.join('../data/mipas_pd', file), key='df_reduced',
          format='table')
    """
    #SVM classifier KPCA + htang
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')
    htang = np.asarray(df_data.htang).reshape(-1,1)
    df_data = df_data.iloc[:, range(0, 10011)]
    df_data[df_data.columns] = scaler.transform(df_data[df_data.columns])
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    kpc = compute_kpca(df_data, loaded_model)
    kpch = np.hstack([kpc, htang])    #labels_svm_pc = clf.predict(pc_t)
    labels_svm_kpca_h = clf_h.predict(kpch)
    df_reduced = df_reduced.assign(labels_svm_kpca_h=labels_svm_kpca_h)
    df_reduced.to_hdf(os.path.join('../data/mipas_pd', file), key='df_reduced',
          format='table')