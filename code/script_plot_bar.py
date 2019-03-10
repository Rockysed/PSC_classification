# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 09:41:23 2019

@author: rocco
"""
#import libraries
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from table_coincidence import plot_bar
#load files
files = [i for i in os.listdir("../data/mipas_pd")]
files = files[19:24]
#list of classifier types
classifier_type = ["labels_bc", "labels_svm_auto", "labels_svm_kpca", "labels_svm_pc_rf_2", "labels_svm_pc_h_rf"]
for clt in classifier_type:
    plot_bar(files, clt, cl = False)