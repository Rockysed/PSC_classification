# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:52:43 2019

@author: rocco
"""
import pandas as pd
import h5py
import numpy as np
import os
import matplotlib.pyplot as plt
#load cdsdb
new_file = h5py.File("../data/csdb_bt/csdb_bt.h5", "r")
bt_csdb = new_file["bt"][:]
new_file.close()
#compute mean and var csdb dataset
df_bt_csdb = pd.DataFrame(bt_csdb)
mean_bt_csdb = df_bt_csdb.mean()
var_bt_csdb = df_bt_csdb.var()

directory = "../data/mipas_blabeled_2009/2009_bt"
files = [i for i in os.listdir(directory)]
bt_mipas_tot = np.empty([0, 142])
for file in files:
    #load mipas df
    bt_mipas = np.empty([0, 142])
    new_file = h5py.File(os.path.join(directory, file), "r")
    bt_mipas = new_file["bt"][:]
    new_file.close()
    bt_mipas_tot = np.vstack([bt_mipas_tot, bt_mipas])
df_bt_mipas = pd.DataFrame(bt_mipas_tot)
mean_bt_mipas = df_bt_mipas.mean()
var_bt_mipas = df_bt_mipas.var()
#plotting variance
my_path = "../progetti/bt_mean_var/"
if not os.path.exists(my_path):
    os.makedirs(my_path)
my_file =  "var_bt" + ".png"
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()
ax1.plot(np.arange(0,142), var_bt_mipas, label = "mipas")
ax1.plot(np.arange(0,142), var_bt_csdb, label = "csdb")
loc = [84, 99, 107, 113, 125, 131, 137]
new_tick_locations = np.array(loc)
ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(new_tick_locations)
transition = ["t1", "t2", "t3", "t4", "t5", "t6", "t7"]
ax2.set_xticklabels(transition)
ax2.set_xlabel("transition")
title = ax2.set_title("Variance: BT")
title.set_y(1.1)
fig.subplots_adjust(top=0.85)
ax1.legend()
for tr in loc:
    ax1.axvline(tr, linewidth = 1, color = 'k')
ax1.set_ylabel("var")
ax1.set_xlabel("BT")
fig.savefig(os.path.join(my_path, my_file))
plt.close()
#plotting mean
my_file =  "mean_bt" + ".png"
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()
ax1.plot(np.arange(0,142), mean_bt_mipas, label = "mipas")
ax1.plot(np.arange(0,142), mean_bt_csdb, label = "csdb")
new_tick_locations = np.array(loc)
ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(transition)
ax2.set_xlabel("transition")
title = ax2.set_title("Mean: BT")
title.set_y(1.1)
fig.subplots_adjust(top=0.85)
ax1.legend() 
for tr in loc:
    ax1.axvline(tr, linewidth = 1, color = 'k')
ax1.set_ylabel("mean")
ax1.set_xlabel("BT")
fig.savefig(os.path.join(my_path, my_file))
plt.close()
"""
#btd
new_file = h5py.File("../data/csdb_new/csdb_complete.h5", "r")
btd_csdb = new_file["btd_complete"][:]
new_file.close()
df_btd_csdb = pd.DataFrame(btd_csdb)
mean_btd_csdb = df_btd_csdb.mean()
var_btd_csdb = df_btd_csdb.var()
directory = "../data/mipas_pd"
files = [i for i in os.listdir(directory)]
files = files[19:24]
df_btd_mipas_complete = pd.DataFrame()
for file in files:
    #load mipas df
    df_btd_mipas = pd.read_hdf(os.path.join(directory, file),'df_btd')
    df_btd_mipas_complete = df_btd_mipas_complete.append(df_btd_mipas)

mean_btd_mipas = df_btd_mipas.iloc[:, 0:10011].mean()
var_btd_mipas = df_btd_mipas.iloc[:, 0:10011].var()
plt.plot(np.arange(0,10011), var_btd_mipas, label = "mipas")
plt.plot(np.arange(0,10011), var_btd_csdb, label = "csdb")
"""