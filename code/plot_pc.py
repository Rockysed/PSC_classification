# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 09:50:20 2019

@author: rocco
"""

def plot_pc(comp1, comp2, labels, title, classifier_type):
    comp1 = comp1.reshape(-1,1)
    comp2 = comp2.reshape(-1,1)
    if classifier_type == "labels_bc":
        markers = ['s', 's', '^', 'o', 'D', 'v', '>']
        colors = ['w', 'b', 'r', 'chartreuse', 'cyan', 'goldenrod', 'steelblue']
        edges = ['k', 'b', 'r', 'chartreuse', 'cyan', 'goldenrod', 'steelblue']
        labels_n = ['unspec.', 'ICE', 'NAT', 'STSmix', 'ICE_NAT', "NAT_STS", "ICE_STS"]
        for j in range (7):
            plt.scatter(comp1[labels == j] , comp2[labels == j], c = colors[j], s=2 \
                        , marker=markers[j], label=labels_n[j], edgecolors=edges[j])
    else:
        markers = ['s', '^', 'o', 'D', 'v']
        colors = ['b', 'r', 'chartreuse', 'chartreuse', 'chartreuse']
        edges = ['k', 'b', 'r', 'chartreuse', 'cyan', 'goldenrod', 'steelblue']
        labels_n = ['ICE', 'NAT', 'STS_1', 'STS_2', 'STS_3']
        for j in range (0, 5):
            plt.scatter(comp1[labels == j] , comp2[labels == j], c = colors[j], s=2 \
                        , marker=markers[j], label=labels_n[j], edgecolors=edges[j])
    plt.show()
    plt.legend()
    plt.title(title)