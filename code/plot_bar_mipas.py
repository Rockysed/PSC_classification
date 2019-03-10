# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 09:06:51 2019

@author: rocco
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_bar(files, classifier_type, cl):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year = files[0].split("_")[0]
    month_b = int(files[0].split("_")[1])
    month_e = int(files[-1].split("_")[1])
    if classifier_type == "labels_bc":
        mat_tot = np.zeros([5, 7])
    else:
        mat_tot = np.zeros([5, 5])
    
    for file in files:
        #load mipas df
        if classifier_type == "labels_bc":
            mat = np.empty([0, 7])
        else:
            mat = np.empty([0, 5])
        df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
        for i in range(0, 5):
            ind = (pd.value_counts(df_reduced[df_reduced[cl] == i + 1][classifier_type]).index).astype(int)
            print(ind)
            if classifier_type == "labels_bc":
                arr = np.zeros([1, 7])
            else:
                arr = np.zeros([1, 5])
            for j in ind:
                if classifier_type == "labels_bc":
                    arr[0][j] = pd.value_counts(df_reduced[df_reduced[cl] == i +1][classifier_type])[j]
                else:
                    arr[0][j-1] = pd.value_counts(df_reduced[df_reduced[cl] == i][classifier_type])[j]
            mat = np.vstack([mat, arr])
        mat_tot = mat_tot.__add__(mat)
    #plot on MIPAS support
    if classifier_type == "labels_bc":
        mat_perc = np.zeros([5, 7])
    else: 
        mat_perc = np.zeros([5, 5])
    if classifier_type == "labels_bc":
        rl = 7
    else:
        rl = 5
    for i in range(0, rl):
        mat_perc[:, i] = (mat_tot[:, i]/mat_tot[:, i].sum())*100
    mat_perc = np.nan_to_num(mat_perc)
    if classifier_type == "labels_bc":
        bottom = np.zeros([1, 7])
    else:
        bottom = np.zeros([1, 5])
    labels = ["ice", "nat", "sts_mix1", "sts_mix2", "sts_mix3"]
    colors = ["b", "g", "r", "r", "r"]
    plt.figure()
    for i in range(0, mat_perc.shape[0]):
        if classifier_type == "labels_bc":
            supp = ["unsp.", "ice", "nat", "sts mix", "ice_nat", "nat_sts", "ice_sts"]
        else: 
            supp = ["ice", "nat", "sts_mix1", "sts_mix2", "sts_mix3"]
        y = mat_perc[i, :]
        bars = plt.bar(supp, y, bottom=bottom.ravel(), label = labels[i], color = colors[i])
        bottom = bottom + y
    i = 0
    for b in bars:
        x0, y0 = b.xy
        w,h = b.get_width(), b.get_height()
        x2, y2 = x0,y0+h
        t = int(mat_tot[:, i].sum())
        plt.text(x = x2 , y = y2+0.5, s = "N=" +str(t), size = 9)
        i = i + 1
    plt.legend()
    if cl == "labels_svm_lk_pc_rf_scale_v1":
        cl_type = "SVM (RF + PCA)"
    if cl == "labels_svm_kpca":
        cl_type = "SVM (KPCA)"  
    if cl == "labels_svm_auto":
        cl_type = "SVM (autoenc)"         
    plt.title("Coincidence count statistics Bayesian cl. and " + cl_type + "\n " + months[month_b-1] + "-" + months[month_e-1] + \
              " "  + year, y=1.08)
    plt.tight_layout()
    my_file = year +  classifier_type + "_" + cl_type + "_2"+".png"
    my_path = "../progetti/coinc_stat/mipas/"
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()
        #plot on other support  
    for i in range(0, 5):
        mat_perc[i, :] = (mat_tot[i, :]/mat_tot[i, :].sum())*100
    mat_perc = np.nan_to_num(mat_perc)
    bottom = np.zeros([1,5])
    if classifier_type == "labels_bc":
        labels = ["unsp.", "ice", "nat", "sts mix", "ice_nat", "nat_sts", "ice_sts"]
        colors = ["w", "b", "g", "r", "c", "m", "k"]
    else: 
        labels = ["ice", "nat", "sts_mix1", "sts_mix2", "sts_mix3"]
        colors = ["b", "g", "r", "r", "r"]
    plt.figure()
    for i in range(0, mat_perc.shape[1]):
        supp = ["ice", "nat", "sts_mix1", "sts_mix2", "sts_mix3"]
        y = mat_perc[:, i]
        bars = plt.bar(supp, y, bottom=bottom.ravel(), label = labels[i], color = colors[i])
        bottom = bottom + y
        i = 0
    for b in bars:
        x0, y0 = b.xy
        w,h = b.get_width(), b.get_height()
        x2, y2 = x0,y0+h
        t = int(mat_tot[i, :].sum())
        plt.text(x = x2 , y = y2+0.5, s = "N=" +str(t), size = 9)
        i = i + 1
    plt.title("Coincidence count statistics " + cl_type + " and Bayesian classifier \n" + months[month_b-1] + "-" + months[month_e-1] + \
              " "  + year, y=1.08)
    plt.tight_layout()
    plt.legend()
    my_file = year +  classifier_type + "_" + cl_type +".png"
    my_path = "../progetti/coinc_stat/mipas/"
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()