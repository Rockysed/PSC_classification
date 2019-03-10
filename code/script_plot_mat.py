# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 11:43:13 2019

@author: rocco
"""
#load libraries
from interval2hist import compute_mat
from matrixplot import plotmatrix_psc
from matrixplot import plotmatrix_psc_count
import matplotlib.pyplot as plt
import os

#load 2009 data
files = [i for i in os.listdir("../data/mipas_pd/")]
files = files[19:24]
"""
classifier_type = ["labels_bc", "labels_svm_auto", "labels_svm_kpca", "labels_svm_pc_rf_2", "labels_svm_pc_h_rf",\
                   "labels_svm_kpca_ms", "labels_svm_kpca_h_ms", "labels_svm_pc_rf_ms", "labels_svm_pc_h_rf_ms", \
                   "labels_svm_pk_pc_rf_ms", "labels_svm_pk_pc_h_rf_ms", "labels_svm_pk_pc_rf", "labels_svm_pk_pc_h_rf",\
                   "labels_svm_rk_pc_rf", "labels_svm_rk_pc_h_rf", "labels_svm_rk_pc_rf_ms", "labels_svm_rk_pc_h_rf_ms"]
"""
classifier_type = ["labels_svm_lk_pc_rf_scale_v1", "labels_svm_kpca", "labels_svm_auto", "labels_bc"]
for clt in classifier_type:
    """
    if clt == "labels_bc":
        bl = True
    else:
        bl = False
    """
    if clt == "labels_svm_lk_pc_rf_scale_v1":
        cl_type = "SVM (RF + PCA)"
    if clt == "labels_svm_kpca":
        cl_type = "SVM (KPCA)"  
    if clt == "labels_svm_auto":
        cl_type = "SVM (autoenc)" 
    if clt == "labels_bc":
        cl_type = "Bayesian cl."
    #compute histograms
    mat_cl, mat_ice, mat_nat, mat_sts, mat_count_ice, mat_count_nat, mat_count_sts, bins_date = compute_mat(files, clt)
    #plot histograms
    my_path = "../progetti/time_series/new" + clt
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    bl = True
    
    plotmatrix_psc( mat_cl, bins_date, bl)
    plt.title("Covered area by all PSC types [$km^2$]")   
    my_file =  "all_clouds" + ".png"
    figure = plt.gcf()
    figure.set_size_inches(16, 12)
    plt.show()
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()
    bl = False
    
    plotmatrix_psc( mat_ice, bins_date, bl)
    plt.title("Covered area by Ice PSC [$km^2$], " + cl_type)
    my_file =  "ice_cov" + ".png"
    figure = plt.gcf()
    figure.set_size_inches(16, 12)
    plt.show()
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()
    
    plotmatrix_psc_count(mat_count_ice, bins_date)
    plt.title("Bins count of Ice PSC, " + cl_type)
    my_file =  "ice_count" + ".png"
    figure = plt.gcf()
    figure.set_size_inches(16, 12)
    plt.show()
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()
    
    plotmatrix_psc( mat_nat, bins_date, bl)
    plt.title("Covered area by NAT PSC [$km^2$], " + cl_type)
    my_file =  "nat_cov" + ".png"
    figure = plt.gcf()
    figure.set_size_inches(16, 12)
    plt.show()
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()
    
    plotmatrix_psc_count(mat_count_nat, bins_date)
    plt.title("Bins count of NAT PSC, " + cl_type)
    my_file =  "nat_count" + ".png"
    figure = plt.gcf()
    figure.set_size_inches(16, 12)
    plt.show()
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()
    
    plotmatrix_psc( mat_sts, bins_date, bl)
    plt.title("Covered area by STS PSC [$km^2$], " + cl_type)
    my_file =  "sts_cov" + ".png"
    figure = plt.gcf()
    figure.set_size_inches(16, 12)
    plt.show()
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()
    
    plotmatrix_psc_count(mat_count_sts, bins_date)
    plt.title("Bins count of STS PSC, " + cl_type)
    my_file =  "sts_count" + ".png"
    figure = plt.gcf()
    figure.set_size_inches(16, 12)
    plt.savefig(os.path.join(my_path, my_file))
    plt.close()