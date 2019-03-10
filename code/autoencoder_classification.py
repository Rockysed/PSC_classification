# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 08:58:44 2019

@author: rocco
"""

# libraries 
from keras.models import model_from_json
from sklearn import svm
import os
import pickle
import h5py
import pandas as pd
from scipy import stats
from sklearn.model_selection import GridSearchCV


# load data
new_file = h5py.File("../data/csdb_new/csdb_complete.h5", "r")

btd_csdb = new_file["btd_complete"][:]

labels = new_file["labels"][:]

htang = new_file["htang"][:]

new_file.close()

#load scaler 
filename = "new_min_max_scaler.pckl"
scaler = pickle.load(open(filename, 'rb'))

#transform CSDB data
f_csdb = scaler.fit_transform(btd_csdb)

del btd_csdb
# load json and create model
json_file = open('Neural_net_weights/new/new_encoder_2.json', 'r')

loaded_model_json = json_file.read()

json_file.close()

loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("Neural_net_weights/new/new_model_encoder_2.h5")

print("Loaded model from disk")

#predict

encoded_c = loaded_model.predict(f_csdb)

del f_csdb

#train svm 

parameters = [{'C': [1, 10, 100, 1000, 1000, 10000], 'kernel': ['linear']}]

svc = svm.SVC()

clf = GridSearchCV(svc, parameters, cv=5)

#clf = RandomizedSearchCV(svc, parameters, cv=5, n_iter=n_iter_search)

clf.fit(encoded_c, labels.ravel())

f = open('grid_svm_autoenc.pckl', 'wb')
pickle.dump(clf, f)
f.close()
"""
clf = svm.SVC(kernel = "linear")

clf.fit(encoded_c, labels.ravel())

#classify MIPAS data
files = [i for i in os.listdir("../data/mipas_pd")]

files = files[19:24]

for file in files:
    #SVM classifier autoencoder
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    f_mipas = scaler.fit_transform(df_data.iloc[:,0:10011])
    encoded_m = loaded_model.predict(f_mipas)
    #labels_svm_pc = clf.predict(pc_t)
    labels_svm_auto = clf.predict(encoded_m)
    df_reduced = df_reduced.assign(labels_svm_auto_new_2 = labels_svm_auto)
    df_reduced.to_hdf(os.path.join('../data/mipas_pd', file), key='df_reduced',
          format='table')
"""
