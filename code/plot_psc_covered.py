# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 15:17:24 2019

@author: rocco
"""

mat = [mat_ice, mat_nat, mat_sts]
name = ["ICE", "NAT", "STS"]
classifier = ["kpca"]
for i in range(0, len(name)):
    plotmatrix_psc(mat[i], bins_date, False)
    plt.title("Covered area [$km^2$] by " + name[i] + ", " + classifier[0])