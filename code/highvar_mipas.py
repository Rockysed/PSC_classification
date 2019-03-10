# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 14:45:27 2019

@author: rocco
"""
def BTD_list(a1, a2): 
    return np.array2string(a1)+"-"+np.array2string(a2)

#set file to read
file = files[2]

df_comp = pd.read_hdf(os.path.join('../data/mipas_pd', file),'df_btd')
df_data = df_comp.iloc[:, range(0, 10011)]
#retrieve windows high variance MIPAS
var_mipas_complete = df_data.var()
ind1 = np.where(var_mipas_complete > 460)[0]

r,c = np.triu_indices(142,1)
i_r = r[ind1]
i_c = c[ind1]

list1 = list(map(BTD_list, i_r, i_c))
d = {'Highest variance BTDs: Spectral windows subtraction': list1}
df = pd.DataFrame(data=d)

df_data_2 = df_data[(df_comp.htang> 20) & (df_comp.htang  < 22)]
var_mipas_2 = df_data_2.var()
ind2 = np.where(var_mipas_2 > 430)[0]

i_r = r[ind2]
i_c = c[ind2]

list2 = list(map(BTD_list, i_r, i_c))
d = {'Highest variance BTDs: Spectral windows subtraction': list2}
df_2 = pd.DataFrame(data=d)

df_data_3 = df_data[(df_comp.htang> 18) & (df_comp.htang  < 20)]
var_mipas_3 = df_data_3.var()
ind3 = np.where(var_mipas_3 > 550)[0]

i_r = r[ind3]
i_c = c[ind3]

list3 = list(map(BTD_list, i_r, i_c))
d = {'Highest variance BTDs: Spectral windows subtraction': list3}
df_3 = pd.DataFrame(data=d)