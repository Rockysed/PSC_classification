# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 15:13:16 2019

@author: rocco
"""

from sklearn.decomposition import KernelPCA
from sklearn.preprocessing import MinMaxScaler
import h5py
import pickle
import numpy as np

#filter microwindows
r,c = np.triu_indices(142,1)
wk = np.where(((c < 106) | (c > 137)) & ((r < 106) | (r > 137)))[0]

new_file = h5py.File("../data/mipas_blabeled_reinhold_features/rf_mipas_complete", "r")
btd_mipas = new_file["btd_complete"][:, wk]
new_file.close()

scaler = MinMaxScaler()
btd_mipas_scaled = scaler.fit_transform(btd_mipas)


kpca = KernelPCA(kernel = "polynomial", n_components = 7)
kpc = kpca.fit_transform(btd_mipas_scaled)

filename = "model_kpca_btd_scaled_red"
pickle.dump(kpca, open(filename, 'wb'))