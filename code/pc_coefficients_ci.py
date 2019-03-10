# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 13:33:58 2019

@author: 754672
"""
#PC1

plt.scatter(np.arange(0, 18282), pc[0:18282,0], c = ci[0:18282].ravel(), s=0.05, cmap=plt.cm.Spectral)

plt.scatter(np.arange(18282, 31348), pc[18282:31348,0], c = ci[18282:31348].ravel(), s=0.05, cmap=plt.cm.Spectral)

plt.scatter(np.arange(31348, 64335), pc[31348:64335,0], c = ci[31348: 64335].ravel(), s=0.05, cmap=plt.cm.Spectral)

plt.title("Analyzing PC 1, CSDB")

clb = plt.colorbar()

clb.set_label('cloud index')

plt.xlabel("Measurements #")
           
plt.ylabel("coefficients")

#PC2

plt.scatter(np.arange(0, 18282), pc[0:18282,1], c = ci[0:18282].ravel(), s=0.05, cmap=plt.cm.Spectral)

plt.scatter(np.arange(18282, 31348), pc[18282:31348,1], c = ci[18282:31348].ravel(), s=0.05, cmap=plt.cm.Spectral)

plt.scatter(np.arange(31348, 64335), pc[31348:64335,1], c = ci[31348: 64335].ravel(), s=0.05, cmap=plt.cm.Spectral)

plt.title("Analyzing PC 2, CSDB")

clb = plt.colorbar()

clb.set_label('cloud index')

plt.xlabel("Measurements #")
           
plt.ylabel("coefficients")

#PC3

plt.scatter(np.arange(0, 18282), pc[0:18282,2], c = ci[0:18282].ravel(), s=0.05, cmap=plt.cm.Spectral)

plt.scatter(np.arange(18282, 31348), pc[18282:31348,2], c = ci[18282:31348].ravel(), s=0.05, cmap=plt.cm.Spectral)

plt.scatter(np.arange(31348, 64335), pc[31348:64335,2], c = ci[31348: 64335].ravel(), s=0.05, cmap=plt.cm.Spectral)

plt.title("Analyzing PC 3, CSDB")

clb = plt.colorbar()

clb.set_label('cloud index')

plt.xlabel("Measurements #")
           
plt.ylabel("coefficients")