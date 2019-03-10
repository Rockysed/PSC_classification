# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 09:13:58 2019

@author: rocco
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
files = [i for i in os.listdir("../data/mipas_pd")]
files = files[19:24]
classifier_type = "labels_svm_pc_rf_2"
def plot_bar(files, classifier_type, cl_max):
    if cl_max == True:
        cl = "cal_max_cl"
    else:
        cl = "caliop_class_dense"
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year = files[0].split("_")[0]
    month_b = int(files[0].split("_")[1])
    month_e = int(files[-1].split("_")[1])
    if classifier_type == "labels_bc":
        mat_tot = np.zeros([9, 7])
    else:
        mat_tot = np.zeros([9, 5])
    
    for file in files:
        #load mipas df
        if classifier_type == "labels_bc":
            mat = np.empty([0, 7])
        else:
            mat = np.empty([0, 5])
        df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
        for i in range(0, 9):
            ind = (pd.value_counts(df_reduced[df_reduced[cl] == i][classifier_type]).index).astype(int)
            print(ind)
            if classifier_type == "labels_bc":
                arr = np.zeros([1, 7])
            else:
                arr = np.zeros([1, 5])
            for j in ind:
                if classifier_type == "labels_bc":
                    arr[0][j] = pd.value_counts(df_reduced[df_reduced[cl] == i][classifier_type])[j]
                else:
                    arr[0][j-1] = pd.value_counts(df_reduced[df_reduced[cl] == i][classifier_type])[j]
            mat = np.vstack([mat, arr])
        mat_tot = mat_tot.__add__(mat)
    #plot on MIPAS support
    if classifier_type == "labels_bc":
        mat_perc = np.zeros([9, 7])
    else: 
        mat_perc = np.zeros([9, 5])
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
    labels = ["no_cloud", "sts", "nat_mix", "not_used", "ice", "nat_enh", "w_ice", "not_ret", "p>215hPa"]
    colors = ["k", "r", "g", "w", "b", "g", "b", "w", "w"]
    plt.figure()
    for i in range(0, mat_perc.shape[0]):
        if classifier_type == "labels_bc":
            supp = ["unsp.", "ice", "nat", "sts mix", "ice_nat", "nat_sts", "ice_sts"]
        else: 
            supp = ["ice", "nat", "sts_mix1", "sts_mix2", "sts_mix3"]
        y = mat_perc[i, :]
        plt.bar(supp, y, bottom=bottom.ravel(), label = labels[i], color = colors[i])
        bottom = bottom + y
    plt.legend()
    plt.title("Coincidence count statistics " + classifier_type + " " + months[month_b-1] + "-" + months[month_e-1] + \
              " "  + year)
    my_file = year +  classifier_type + "_m_s" +".png"
    my_path = "../progetti/coinc_stat/"
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()
    
    #plot on Caliop support  
    for i in range(0, 9):
        mat_perc[i, :] = (mat_tot[i, :]/mat_tot[i, :].sum())*100
    mat_perc = np.nan_to_num(mat_perc)
    bottom = np.zeros([1,9])
    if classifier_type == "labels_bc":
        labels = ["unsp.", "ice", "nat", "sts mix", "ice_nat", "nat_sts", "ice_sts"]
        colors = ["w", "b", "g", "r", "c", "m", "k"]
    else: 
        labels = ["ice", "nat", "sts_mix1", "sts_mix2", "sts_mix3"]
        colors = ["b", "g", "r", "r", "r"]
    plt.figure()
    for i in range(0, mat_perc.shape[1]):
        supp = ["no_cloud", "sts", "nat_mix", "not_used", "ice", "nat_enh", "w_ice", "not_ret", "p>215hPa"]
        y = mat_perc[:, i]
        plt.bar(supp, y, bottom=bottom.ravel(), label = labels[i], color = colors[i])
        bottom = bottom + y
    plt.title("Coincidence count statistics " + classifier_type + " " + months[month_b-1] + "-" + months[month_e-1] + \
              " "  + year)
    plt.legend()
    my_file = year +  classifier_type + "_m_c" +".png"
    my_path = "../progetti/coinc_stat/"
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()
#pie chart
def plot_pie(classifier_type):
    if classifier_type.split("_")[-1] == "ms": 
        labels = ["ice", "nat", "sts"]
        colors = ["b", "g", "r"]
        bv = False
        ms = True
    else:
        labels = ["ice", "nat", "sts_mix1", "sts_mix2", "sts_mix3"]
        colors = ["b", "g", "r", "r", "r"]
        bv = False
        ms = False
    if classifier_type == "labels_bc":
        labels = ["unsp.", "ice", "nat", "sts mix", "ice_nat", "nat_sts", "ice_sts"]
        colors = ["w", "b", "g", "r", "c", "m", "k"]
        bv = True
    print(bv)
    if bv == True:
        arr_tot = np.zeros([1, 7])
        arr = np.zeros([1, 7])
    else:
         if ms == False:
             arr_tot = np.zeros([1, 5])
             arr = np.zeros([1, 5])
         else:
             arr_tot = np.zeros([1, 3])
             arr = np.zeros([1, 3]) 
    for file in files:
        df_reduced = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_reduced')
        ind = (pd.value_counts(df_reduced[classifier_type]).index).astype(int)
            
        if bv == True:
            arr = np.zeros([1, 7])
        else:
            if ms == True:
                arr = np.zeros([1, 3])
            else:
                arr = np.zeros([1, 5])
        for i in ind:
            if bv == True:
                arr[0][i] = pd.value_counts(df_reduced[classifier_type])[i]
            else:
                arr[0][i-1] = pd.value_counts(df_reduced[classifier_type])[i]
        arr_tot = arr_tot + arr
    plt.pie(arr_tot.ravel(), labels=labels, autopct='%1.1f%%', colors = colors)
    print(labels)
    print(ind)
#plot it
