# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 16:15:31 2019

@author: 754672
"""

i_lower = np.tril_indices(142, 1)

result[i_lower] = result.T[i_lower]

fig = plt.matshow(df_fi, norm=LogNorm())

plt.axhline(84, linewidth = 1, color = 'k')

plt.axhline(99, linewidth = 1, color = 'k')

plt.axhline(107, linewidth = 1, color = 'k')

plt.axhline(113, linewidth = 1, color = 'k')

plt.axhline(125, linewidth = 1, color = 'k')

plt.axhline(131, linewidth = 1, color = 'k')

plt.axhline(137, linewidth = 1, color = 'k')

plt.axvline(84, linewidth = 1, color = 'k')

plt.axvline(99, linewidth = 1, color = 'k')

plt.axvline(107, linewidth = 1, color = 'k')

plt.axvline(113, linewidth = 1, color = 'k')

plt.axvline(125, linewidth = 1, color = 'k')

plt.axvline(131, linewidth = 1, color = 'k')

plt.axvline(137, linewidth = 1, color = 'k')

[84, 99, 107, 113, 125, 131, 137]