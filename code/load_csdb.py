import numpy as np
from netCDF4 import Dataset
import h5py
#define Gaussian random generator function to add noise to all channels
def add_gaussian_noise(x):
    a = np.true_divide(np.random.normal(0, 20, 84), np.sqrt(40))
    b = np.true_divide(np.random.normal(0, 10, 23), np.sqrt(40))
    d = np.true_divide(np.random.normal(0, 2, 30), np.sqrt(40))
    s1 = np.true_divide(np.random.normal(0, 20, 3), np.sqrt(120))
    s2 = np.true_divide(np.random.normal(0, 20, 1), np.sqrt(160))   
    x = np.hstack((a, b, d, s1, s2))
    return x
#open ICE file
dataset_1 = Dataset('..\data\csdb\sp_ia_mws.nc')
#load variables
radiance = dataset_1.variables['radiance'][:]
htang = dataset_1.variables['htang'][:]
wave_min = dataset_1.variables['wave_min'][:]
wave_max = dataset_1.variables['wave_max'][:]
label_1=np.ones((htang.shape[0],1), dtype = np.int8)
iscen = dataset_1["iscen"][:]
radius = dataset_1["radius"][:]
radius = radius[iscen]
#close ICE file
dataset_1.close()
#open NAT file
dataset_2 = Dataset('..\data\csdb\sp_na_extd1_mws.nc')
#load variables
radiance_nat = dataset_2.variables['radiance'][:]
htang_nat = dataset_2.variables['htang'][:]
label_2=2*(np.ones((htang_nat.shape[0],1), dtype = np.int8))
iscen_2 = dataset_2["iscen"][:]
radius_2 = dataset_2["radius"][:]
radius_2 = radius_2[iscen_2]
#close NAT file
dataset_2.close()
#open STS mix 1 file
dataset_3 = Dataset('..\data\csdb\sp_sa0248_extd1_mws.nc')
#load variables
radiance_sp1 = dataset_3.variables['radiance'][:]
htang_sp1 = dataset_3.variables['htang'][:]
label_3=3*(np.ones((htang_sp1.shape[0],1), dtype = np.int8))
iscen_3 = dataset_3["iscen"][:]
radius_3 = dataset_3["radius"][:]
radius_3 = radius_3[iscen_3]
#close STS mix 1 file
dataset_3.close()
#open STS mix 2 file
dataset_4 = Dataset('..\data\csdb\sp_sa2525_extd1_mws.nc')
#load variables
radiance_sp2 = dataset_4.variables['radiance'][:]
htang_sp2= dataset_4.variables['htang'][:]
label_4=4*(np.ones((htang_sp2.shape[0],1), dtype = np.int8))
iscen_4 = dataset_4["iscen"][:]
radius_4 = dataset_4["radius"][:]
radius_4 = radius_4[iscen_4]
#close STS mix 2 file
dataset_4.close()
#open STS mix 3 file
dataset_5 = Dataset('..\data\csdb\sp_sa4802_extd1_mws.nc')
#load variables
radiance_sp3 = dataset_5.variables['radiance'][:]
htang_sp3= dataset_5.variables['htang'][:]
label_5=5*(np.ones((htang_sp3.shape[0],1), dtype = np.int8))
iscen_5 = dataset_5["iscen"][:]
radius_5 = dataset_5["radius"][:]
radius_5 = radius_5[iscen_5]
#close STS mix 3 file
dataset_5.close()
#stacking data
radiance_complete = np.vstack((radiance, radiance_nat, radiance_sp1, radiance_sp2, radiance_sp3))
htang = htang.reshape(-1, 1)
htang_nat = htang_nat.reshape(-1, 1)
htang_sp1 = htang_sp1.reshape(-1, 1)
htang_sp2 = htang_sp2.reshape(-1, 1)
htang_sp3 = htang_sp3.reshape(-1, 1)
radius = radius.reshape(-1, 1)
radius_2 = radius_2.reshape(-1, 1)
radius_3 = radius_3.reshape(-1, 1)
radius_4 = radius_4.reshape(-1, 1)
radius_5 = radius_5.reshape(-1, 1)

wave_min = wave_min.reshape(142,1)
wave_max = wave_max.reshape(142,1)
htang_complete = np.vstack((htang, htang_nat, htang_sp1, htang_sp2, htang_sp3))
label_complete = np.vstack((label_1, label_2, label_3, label_4, label_5))
radius_complete = np.vstack((radius, radius_2, radius_3, radius_4, radius_5))
#save to file
new_file = h5py.File('csdb_stacked_radius.h5', 'w')
new_file.create_dataset('radiance', data=radiance_complete)
new_file.create_dataset('htang', data=htang_complete)
new_file.create_dataset('wave_min', data=wave_min)
new_file.create_dataset('wave_max', data=wave_max)
new_file.create_dataset('labels', data=label_complete)
new_file.create_dataset('radius', data=radius_complete)
new_file.close()