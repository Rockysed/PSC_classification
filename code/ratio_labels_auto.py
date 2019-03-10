# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 08:58:44 2019

@author: rocco
"""
# libraries 
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import model_from_json
from sklearn import svm
import os
#import eli5
#from eli5.sklearn import PermutationImportance
import h5py
import pandas as pd

# load data
new_file = h5py.File("../data/csdb_new/csdb_complete.h5", "r")

btd_csdb = new_file["btd_complete"][:]

labels = new_file["labels"][:]

htang = new_file["htang"][:]

new_file.close()

#transform CSDB data
f_csdb = MinMaxScaler().fit_transform(btd_csdb)

# load json and create model
json_file = open('Neural_net_weights/new/encoder.json', 'r')

loaded_model_json = json_file.read()

json_file.close()

loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("Neural_net_weights/new/model_encoder.h5")

print("Loaded model from disk")

#predict

encoded_c = loaded_model.predict(f_csdb)

#train svm 

clf = svm.SVC(kernel = "linear", probability = True)

clf.fit(encoded_c, labels.ravel())

#classify MIPAS data
files = [i for i in os.listdir("../data/mipas_pd")]

files = files[21:22]
for file in files:
    #SVM classifier autoencoder
    df_data = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')
    df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
    f_mipas = MinMaxScaler().fit_transform(df_data.iloc[:,0:10011])
    encoded_m = loaded_model.predict(f_mipas)
    #labels_svm_pc = clf.predict(pc_t)
    labels_svm = clf.predict(encoded_m)
    prob_svm = clf.predict_proba(encoded_m)
    
index_name = ["ice", "nat", "sts mix 1", "sts mix 2", "sts mix 3"]
cl = "labels_svm_autoenc"
df_prob = pd.DataFrame()
l = []

for i in range(0, 5):
    c = np.count_nonzero(prob_svm[:, i] > 0.9)/np.count_nonzero(labels_svm == i+1)
    l.append(c)
    

my_path = "../progetti/probabilities/"
df_prob = pd.read_hdf(os.path.join(my_path, "table_prob" + '.h5'),'df_table')
df_prob[cl] = l
l.clear()
df_prob["psc_type"] = index_name
df_prob = df_prob.set_index("psc_type")
if not os.path.exists(my_path):
    os.makedirs(my_path)
df_prob.to_hdf(os.path.join(my_path, "table_prob" + '.h5'), key='df_table',
          format='table')