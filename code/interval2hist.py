# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:38:31 2019

@author: rocco
"""
#import libraries
import numpy as np
import pandas as pd
import os
#function to convert datetime to strin
def date2string(it_obj): 
    return it_obj.date().strftime('%Y-%m-%d')
#function to convert datetime to seconds
def dateinterv2date(interval): 
    return interval.left.to_pydatetime().date()
#function to convert datetime to seconds
def datetime2seconds(date_time): 
    return time.mktime(date_time.timetuple())
 #functiont to compute the mean
"""
def counts_ratio(c1, c2): 
    if c2 != 0:
        return c1/c2
    else:
        return -9999  
"""
def counts_ratio(c1, c2):
    lc2 = len(c2)
    div = np.empty(0)
    for i_c in range(0, lc2):
        if c2[i_c] != 0:
            rat = c1[i_c] / c2[i_c]
            if rat == np.NaN:
                rat = 0
            div = np.append(div, rat)
    if len(div) < 8:
        div = np.append(div, np.zeros([1, (8-len(div))]))
    return div.mean()

#load 2009 data
files = [i for i in os.listdir("../data/mipas_pd/")]
#files = files[5:10]
#files = files[15:19]
files = files[19:24]
#load dataframes
def compute_mat(files, classifier_type):
    #parameters for latitude binning
    lat_min =  [-90.000000, -77.800003, -72.713684, -68.787941, -65.458900, -62.508518, -59.825134, -57.342499]
    lat_max =  [-77.800003, -72.713684, -68.787941, -65.458900, -62.508518, -59.825134, -57.342499, -55.017498]
    a_tot = 46178707.119740881
    bins = pd.IntervalIndex.from_tuples([(lat_min[0], lat_max[0]), (lat_min[1], lat_max[1]), (lat_min[2], lat_max[2]),\
                                         (lat_min[3], lat_max[3]), (lat_min[4], lat_max[4]), (lat_min[5], lat_max[5]), \
                                         (lat_min[6], lat_max[6]), (lat_min[7], lat_max[7])])
    df_data_app = pd.DataFrame()
    df_lt_app = pd.DataFrame()
    for file in files:
        df_data = pd.read_hdf(os.path.join('../data/mipas_pd/', file),'df_reduced')
        df_data_app = df_data_app.append(df_data)
        df_lt = pd.read_hdf(os.path.join('../data/mipas_pd_lat_time', file.split("_")[0] + "_" + file.split("_")[1] + ".h5"),'df_lt')
        df_lt_app = df_lt_app.append(df_lt) 
    
    #binning on date
    sr_binned_total, bins_date = pd.cut(df_lt_app.date, 150, retbins = True)
    bins_date = pd.to_datetime(bins_date)
    sr_binned_cloud = pd.Series(pd.cut(df_data_app.index, bins_date))
    #map
    #list dates clouds
    list_d_tot = list(map(dateinterv2date, sr_binned_total))
    ser_d_tot = pd.Series(list_d_tot)
    list_d_cloud = list(map(dateinterv2date, sr_binned_cloud))
    ser_d_cloud = pd.Series(list_d_cloud)
    sr_binned_htang, bins_htang = pd.cut(df_data_app.htang, 15, retbins = True)
    count_htang = pd.value_counts(sr_binned_htang)
    #creating support for x axis
    a_dates = np.asarray(list_d_cloud)
    b_dates = np.asarray(list_d_tot)
    a=[]
    b=[]
    coverage_list = []
    coverage_ice_list = []
    coverage_nat_list = []
    coverage_sts_list = []
    mean = []
    cl_n = []
    count_tot = []
    ice_n = []
    nat_n = []
    sts_n = []
    ice_mean = []
    nat_mean = []
    sts_mean = []
    ice_count = []
    nat_count = []
    sts_count = []
    mat_cl = np.empty([0, bins_date.size])
    mat_ice = np.empty([0, bins_date.size])
    mat_sts = np.empty([0, bins_date.size])
    mat_nat = np.empty([0, bins_date.size])
    mat_count_ice = np.empty([0, bins_date.size])
    mat_count_nat = np.empty([0, bins_date.size])
    mat_count_sts = np.empty([0, bins_date.size])
    #labels sts definition
    classifier = classifier_type
    bayesian = False
    if classifier == "labels_bc":
        bayesian = True
    if bayesian == True:
        lab_sts = [3]
    else:
        lab_sts = [3, 4, 5]
    for n_bin_htang in count_htang.index:
        for n_bin in bins_date:
             c_a = np.count_nonzero(a_dates == n_bin.date())
             a.append(c_a)
             c_b = np.count_nonzero(b_dates == n_bin.date())
             b.append(c_b)
             #count_cl = pd.value_counts(sl_binned_cloud.sort_index()[ser_d_cloud.values == n_bin.date()])       
             #count_tot = pd.value_counts(sl_binned_total.sort_index()[ser_d_tot.values == n_bin.date()])
             #bool variable to check if count_tot.sum() > 1000
             for bin_lat in bins:
                      count_tot.append(np.count_nonzero(((df_lt_app["htang"].between( n_bin_htang.left - 1, n_bin_htang.right + 1))) \
                       & ((ser_d_tot.values == n_bin.date())) \
                       & ((df_lt_app["lat"].between( bin_lat.left, bin_lat.right)))))
                      if count_tot[-1] > 6:
                          cl_n.append(np.count_nonzero((ser_d_cloud.values == n_bin.date()) \
                                                        & (df_data_app["lat"].between( bin_lat.left, bin_lat.right)) \
                                                        & (df_data_app["htang"].between( n_bin_htang.left - 1, n_bin_htang.right + 1))))
                          ice_n.append(np.count_nonzero((ser_d_cloud.values == n_bin.date()) & (df_data_app[classifier] == 1) \
                                                        & (df_data_app["lat"].between( bin_lat.left, bin_lat.right)) \
                                                        & (df_data_app["htang"].between( n_bin_htang.left - 1, n_bin_htang.right + 1))))
                          nat_n.append(np.count_nonzero((ser_d_cloud.values == n_bin.date()) & (df_data_app[classifier] == 2) \
                                                        & (df_data_app["lat"].between( bin_lat.left , bin_lat.right))
                                                        & (df_data_app["htang"].between( n_bin_htang.left - 1, n_bin_htang.right + 1))))
                          sts_n.append(np.count_nonzero((ser_d_cloud.values == n_bin.date()) & (df_data_app[classifier].between(lab_sts[0], lab_sts[-1])) \
                                                        & (df_data_app["lat"].between( bin_lat.left, bin_lat.right))
                                                        & (df_data_app["htang"].between( n_bin_htang.left - 1, n_bin_htang.right + 1))))
                      else: 
                          cl_n.append(0)
                          ice_n.append(0)
                          nat_n.append(0)
                          sts_n.append(0)
            
             #mean_ratio_ice = np.sum(np.asarray(list(map(counts_ratio, ice_n, count_tot))))/8
             #mean_ratio_nat = np.sum(np.asarray(list(map(counts_ratio, nat_n, count_tot))))/8
             #mean_ratio_sts = np.sum(np.asarray(list(map(counts_ratio, sts_n, count_tot))))/8
             #mean_ratio = np.sum(np.asarray(list(map(counts_ratio, cl_n, count_tot))))/8
             if sum(count_tot) > 20:
                 mean_ratio_ice = counts_ratio(ice_n, count_tot)
                 mean_ratio_nat = counts_ratio(nat_n, count_tot)
                 mean_ratio_sts = counts_ratio(sts_n, count_tot)
                 mean_ratio = counts_ratio(cl_n, count_tot)
             else:
                 mean_ratio_ice = 0
                 mean_ratio_nat = 0
                 mean_ratio_sts = 0
                 mean_ratio = 0
             ice_mean.append(mean_ratio_ice)
             nat_mean.append(mean_ratio_nat)
             sts_mean.append(mean_ratio_sts)
                
             #mean_ratio = np.sum(np.asarray(list(map(counts_ratio, count_cl, count_tot))))/8
             #if ((-9999 not in list(map(counts_ratio, cl_n, count_tot)))):
             coverage = mean_ratio * a_tot
             coverage_ice = mean_ratio_ice * a_tot
             coverage_nat = mean_ratio_nat * a_tot
             coverage_sts = mean_ratio_sts * a_tot
             """
             else:
                 coverage = -9999
                 coverage_ice = -9999
                 coverage_nat = -9999
                 coverage_sts = -9999
             """
        
             coverage_list.append(coverage)
             coverage_ice_list.append(coverage_ice)
             coverage_nat_list.append(coverage_nat)
             coverage_sts_list.append(coverage_sts)
        
             mean.append(mean_ratio)
             """
             cov_arr = np.asarray(coverage_list)
             cov_ice_arr = np.asarray(coverage_ice_list)
             cov_nat_arr = np.asarray(coverage_nat_list)
             cov_sts_arr = np.asarray(coverage_sts_list)
             """
             ice_count.append(sum(ice_n))
             sts_count.append(sum(sts_n))
             nat_count.append(sum(nat_n))
             ice_n.clear()
             nat_n.clear()
             sts_n.clear()
             cl_n.clear()
             count_tot.clear()
        cov_arr = np.asarray(coverage_list)
        cov_ice_arr = np.asarray(coverage_ice_list)
        cov_nat_arr = np.asarray(coverage_nat_list)
        cov_sts_arr = np.asarray(coverage_sts_list)
        ice_count_arr = np.asarray(ice_count)
        nat_count_arr = np.asarray(nat_count)
        sts_count_arr = np.asarray(sts_count)
        mat_cl = np.vstack([mat_cl, cov_arr])
        mat_ice = np.vstack([mat_ice, cov_ice_arr])
        mat_nat = np.vstack([mat_nat, cov_nat_arr])
        mat_sts = np.vstack([mat_sts, cov_sts_arr])
        mat_cl[np.where(np.isnan(mat_cl))]=0
        mat_ice[np.where(np.isnan(mat_ice))]=0
        mat_nat[np.where(np.isnan(mat_nat))]=0
        mat_sts[np.where(np.isnan(mat_sts))]=0
        mat_count_ice = np.vstack([mat_count_ice, ice_count_arr])
        mat_count_nat = np.vstack([mat_count_nat, nat_count_arr])
        mat_count_sts = np.vstack([mat_count_sts, sts_count_arr])
        ice_count.clear()
        nat_count.clear()
        sts_count.clear()
        coverage_list.clear()
        coverage_ice_list.clear()
        coverage_nat_list.clear()
        coverage_sts_list.clear()
    return mat_cl, mat_ice, mat_nat, mat_sts, mat_count_ice, mat_count_nat, mat_count_sts, bins_date
    #out of the cycle



   