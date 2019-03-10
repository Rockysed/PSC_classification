# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 17:35:26 2019

@author: 754672
"""

nat_coinc = predicted_test.size - np.sum((predicted_test==2) == (y_test.ravel() == 2))

nat_count = np.count_nonzero(y_test.ravel() == 2)

perc_nat = (nat_coinc/nat_count)*100