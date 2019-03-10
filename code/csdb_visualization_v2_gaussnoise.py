import numpy as np
import h5py
from sklearn.preprocessing import StandardScaler

h5f = h5py.File("../data/csdb/csdb_stacked_radius.h5", "r")

labels_csdb = h5f["labels"][:]
#radiance = h5f["radiance"][:]
wave_min = h5f["wave_min"][:]
wave_max = h5f["wave_max"][:]
htang = h5f["htang"][:]
radius = h5f["radius"][:]

h5f.close()

h5f = h5py.File("../data/csdb/csdb_gaussnoise.h5", "r")

radiance = h5f["csdb_gaussnoise"][:]

h5f.close()

labels = labels_csdb
#index_0 = np.random.choice(labels.shape[0], 70000, replace=False)
#index_0 = np.random.choice(labels.shape[0], 10000, replace=False)
#radiance_l = radiance[index_0,:]
radiance_l = radiance
#htang_l = htang[index_0,:]
htang_l = htang
#radius_l = radius[index_0,:]
radius_l = radius

#labels = labels[index_0,:]
#define CI calculator

def calculate_ci(x):
    return x[137]/x[138]
# function to calculate the NI


def calculate_ni(x):
    return x[139]/x[137]
"""
def gaussian_noise():
    a = np.random.normal(0, np.true_divide(20, np.sqrt(40)), 85)
    b = np.random.normal(0, np.true_divide(10, np.sqrt(40)), 23)
    d = np.random.normal(0, np.true_divide(2, np.sqrt(40)), 30)
    s1 = np.random.normal(0, np.true_divide(20, np.sqrt(120)), 3)
    s2 = np.random.normal(0, np.true_divide(20, np.sqrt(160)), 1)
    noise = np.hstack((a, b, d, s1, s2))
    return noise

def gaussian_noise_matrix(dim):
    matrix = np.empty([0,142])
    for i in range(0, dim):
        matrix = np.vstack((matrix, gaussian_noise()))
    return matrix
#    return np.add(x, noise)
"""  
#function to calculate the btd


def BT(rad, wave):
    return 1.438786 * wave / np.log((1.19106e-12 * wave * wave * wave + rad) / rad)
#initialize empty arrays
rad_app = np.empty([0,142])
ci_idx_app = np.empty([0,1])
labels_app = np.empty([0,1])
htang_app = np.empty([0,1])
radius_app = np.empty([0,1])
btd_app = np.empty([0,1])
btd_app_1 = np.empty([0,1])
btd_app_2 = np.empty([0,1])
btd_app_3 = np.empty([0,1])
btd_app_4 = np.empty([0,1])
btd_app_difference = np.empty([0,10011])
ni_app = np.empty([0,1])

k = 0
ct = 0
#upper right matrix indexes
r,c = np.triu_indices(142,1)
#cycle over arrays
for i in range(0, radiance_l[:, 0].size):
    ci_idx = calculate_ci(radiance_l[i])
    # print(ci_idx)
    if htang[i] >=15 and htang[i] <=30:
     if ci_idx >= 0.5 and ci_idx <= 4.5:
        rad = radiance_l[i,:].reshape(1, 142)
        htang_r = htang_l[i].reshape(1,1)
        rad_app = np.append(rad_app, rad, 0)
        htang_app = np.append(htang_app, htang_r, 0 )
        #append radius
        radius_r = radius_l[i].reshape(1,1)
        radius_app = np.append(radius_app, radius_r, 0 )
        #append CI
        ci_idx_a = np.atleast_1d(ci_idx)
        ci_idx_a_r = ci_idx_a.reshape(1, 1)
        ci_idx_app = np.append(ci_idx_app, ci_idx_a_r, 0)
        #append NI
        ni_r = calculate_ni(radiance_l[i])
        ni_a = np.atleast_1d(ni_r)
        ni_a_r = ni_a.reshape(1, 1)
        ni_app = np.append(ni_app, ni_a_r, 0)
        #append brightness difference BT
        btd_r = BT((abs(rad_app[ct,140])*(1e-9)), 833) - BT(abs(rad_app[ct,141]*(1e-9)), 949)
        btd_a = np.atleast_1d(btd_r)
        btd_a_r = btd_a.reshape(1, 1)
        btd_app = np.append(btd_app, btd_a_r, 0)
        #append brightness difference BT 820-831
        btd_r_1 = BT((abs(rad_app[ct,38])*(1e-9)), 820) - BT(abs(rad_app[ct,49]*(1e-9)), 831)
        btd_a_1 = np.atleast_1d(btd_r_1)
        btd_a_r_1 = btd_a_1.reshape(1, 1)
        btd_app_1 = np.append(btd_app_1, btd_a_r_1, 0)
        #append brightness difference BT 1406-960
        btd_r_2 = BT((abs(rad_app[ct,101])*(1e-9)), 1406) - BT(abs(rad_app[ct,79]*(1e-9)), 960)
        btd_a_2 = np.atleast_1d(btd_r_2)
        btd_a_r_2 = btd_a_2.reshape(1, 1)
        btd_app_2 = np.append(btd_app_2, btd_a_r_2, 0)
        #append brightness difference BT 831-1225
        btd_r_3 = BT((abs(rad_app[ct,49])*(1e-9)), 831) - BT(abs(rad_app[ct,85]*(1e-9)), 1225)
        btd_a_3 = np.atleast_1d(btd_r_3)
        btd_a_r_3 = btd_a_3.reshape(1, 1)
        btd_app_3 = np.append(btd_app_3, btd_a_r_3, 0)
        #append brightness difference BT 960-1225
        btd_r_4 = BT((abs(rad_app[ct,79])*(1e-9)), 960) - BT(abs(rad_app[ct,85]*(1e-9)), 1225)
        btd_a_4 = np.atleast_1d(btd_r_4)
        btd_a_r_4 = btd_a_4.reshape(1, 1)
        btd_app_4 = np.append(btd_app_4, btd_a_r_4, 0)
        #append BTDs windows
        btd_r_difference = BT((abs(rad_app[ct, r].reshape(1, 10011)) * (1e-9)), wave_min[r].reshape(1, 10011)) - BT(abs(rad_app[ct, c].reshape(1, 10011) * (1e-9)),  wave_min[c].reshape(1, 10011))
        btd_a_r_difference = btd_r_difference.reshape(1, 10011)
        btd_app_difference = np.append(btd_app_difference, btd_a_r_difference, 0)   
        #append labels
        lab = labels[i,0].reshape(1,1)
        labels_app = np.append(labels_app, lab, 0)

        ct += 1

features_csdb = [ci_idx_app, ni_app, btd_app, btd_app_1, btd_app_2, btd_app_3, btd_app_4]
myarray = np.asarray(features_csdb)
myarray = myarray.reshape(7, -1)
myarray_t = myarray.transpose()
myarray_scaled = StandardScaler().fit_transform(myarray_t)
btd_complete_scaled = StandardScaler().fit_transform(btd_app_difference)

#save to file
new_file = h5py.File("../data/csdb_blabeled_reinhold_features/csdb_radius_gaussnoise_complete.h5", "w")
new_file.create_dataset('htang', data=htang_app)
new_file.create_dataset('radiance', data=rad_app)
new_file.create_dataset('labels', data=labels_app)
new_file.create_dataset('radius', data=radius_app)
new_file.create_dataset('features', data=myarray_t)
new_file.create_dataset('features_scaled', data=myarray_scaled)
new_file.create_dataset('btd_complete', data=btd_app_difference)
new_file.create_dataset('btd_complete_scaled', data=btd_complete_scaled)
new_file.close()
#svm
#clf = SVC(gamma='auto')
#clf.fit(tsne_results, labels_int_t)
#predicted_labels = clf.predict(tsne_results)
#open file
#new_file = h5py.File('features_reinhold_scaled.h5', 'r')
#print(list(new_file.keys()))
#features=new_file["features"][:]
#new_file.close()