# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 09:56:42 2019

@author: rocco
"""

#fun to plot reinhold's plots
def plotdist(df, ind1, ind2):
    f, ax = plt.subplots(1)
    #labels = ["unsp.", "ICE", "NAT", "STS mix", "ICE/NAT", "NAT/STS", "ICE/STS"]
    labels = ["ICE", "NAT", "STS mix 1", "STS mix 2", "STS mix 3"]
    ind = ((np.unique(df["labels"])).astype(int) - 1)
    lab = [labels[i] for i in ind]
    for i in ind:
       plt.scatter(df[df["labels"] == i + 1][ind1], df[df["labels"] == i + 1][ind2],\
                    s=1,  label = lab[i]) 
    ax.legend()
