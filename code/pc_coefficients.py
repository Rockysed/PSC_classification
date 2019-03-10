# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 12:55:14 2019

@author: 754672
"""

#PC 1

plt.plot(np.arange(0, 18282), pc[0:18282,0], 'b', linewidth=0.05, label='Ice')

plt.plot(np.arange(18282, 31348), pc[18282:31348,0], 'g', linewidth=0.05, label='NAT')

plt.plot(np.arange(31348, 64335), pc[31348:64335,0], 'r', linewidth=0.05, label='STS')

leg = plt.legend()

for line in leg.get_lines():
    line.set_linewidth(4.0)

plt.title("Analyzing PC 1, CSDB")

plt.xlabel("Measurements #")

plt.ylabel("coefficients")

#PC 2

plt.plot(np.arange(0, 18282), pc[0:18282,1], 'b', linewidth=0.05, label='Ice')

plt.plot(np.arange(18282, 31348), pc[18282:31348,1], 'g', linewidth=0.05, label='NAT')

plt.plot(np.arange(31348, 64335), pc[31348:64335,1], 'r', linewidth=0.05, label='STS')

leg = plt.legend()

for line in leg.get_lines():
    line.set_linewidth(4.0)

plt.title("Analyzing PC 2, CSDB")

plt.xlabel("Measurements #")

plt.ylabel("coefficients")

#PC 3

plt.plot(np.arange(0, 18282), pc[0:18282,2], 'b', linewidth=0.05, label='Ice')

plt.plot(np.arange(18282, 31348), pc[18282:31348,2], 'g', linewidth=0.05, label='NAT')

plt.plot(np.arange(31348, 64335), pc[31348:64335,2], 'r', linewidth=0.05, label='STS')

leg = plt.legend()

for line in leg.get_lines():
    line.set_linewidth(4.0)

plt.title("Analyzing PC 3, CSDB")

plt.xlabel("Measurements #")

plt.ylabel("coefficients")