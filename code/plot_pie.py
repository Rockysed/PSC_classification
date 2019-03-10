# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 14:14:33 2019

@author: rocco
"""
import os
import matplotlib.pyplot as plt
from table_coincidence import plot_pie
"""
classifier_type = ["labels_bc", "labels_svm_auto", "labels_svm_kpca", "labels_svm_pc_rf_2", "labels_svm_pc_h_rf",\
                   "labels_svm_kpca_ms", "labels_svm_kpca_h_ms", "labels_svm_pc_rf_ms", "labels_svm_pc_h_rf_ms", \
                   "labels_svm_pk_pc_rf_ms", "labels_svm_pk_pc_h_rf_ms", "labels_svm_pk_pc_rf", "labels_svm_pk_pc_h_rf",\
                   "labels_svm_rk_pc_rf", "labels_svm_rk_pc_h_rf", "labels_svm_rk_pc_rf_ms", "labels_svm_rk_pc_h_rf_ms"]
"""
classifier_type = ["labels_svm_auto", "labels_bc", "labels_svm_lk_pc_rf_scale_v1", "labels_svm_kpca"]

for clt in classifier_type:
    my_path = "../progetti/pie_chart/new/"
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    if clt == "labels_svm_lk_pc_rf_scale_v1":
        cl_type = "SVM (RF + PCA)"
    if clt == "labels_svm_kpca":
        cl_type = "SVM (KPCA)"  
    if clt == "labels_svm_auto":
        cl_type = "SVM (autoenc)" 
    if clt == "labels_bc":
        cl_type = "Bayesian cl."
    plot_pie(clt)
    plt.title("Pie chart using " + cl_type)   
    my_file =  cl_type + ".png"
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()
