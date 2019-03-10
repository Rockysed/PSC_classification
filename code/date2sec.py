# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 23:24:41 2019

@author: rocco
"""
#function to convert datetime to seconds
def datetime2seconds(date_time): 
    return time.mktime(date_time.timetuple())
#function to convert datetime to seconds
def dateinterv2date(interval): 
    return interval.left.to_pydatetime().date()
#map
list1 = list(map(datetime2seconds, idx))
#map
list3 = list(map(dateinterv2date, ser))

#bin the latitude
lat_min =  [-90.000000, -77.800003, -72.713684, -68.787941, -65.458900, -62.508518, -59.825134, -57.342499]
lat_max =  [-77.800003, -72.713684, -68.787941, -65.458900, -62.508518, -59.825134, -57.342499, -55.017498]
a_tot = 46178707.119740881
bins = pd.IntervalIndex.from_tuples([(lat_min[0], lat_max[0]), (lat_min[1], lat_max[1]), (lat_min[2], lat_max[2]),\
                                     (lat_min[3], lat_max[3]), (lat_min[4], lat_max[4]), (lat_min[5], lat_max[5]), \
                                     (lat_min[6], lat_max[6]), (lat_min[7], lat_max[7])])
#binning
sr_binned = pd.cut(df_lt["lat"], bins)
sr_binned_total, bins_date = pd.cut(df_lt.date, 10, retbins = True)
bins_date = pd.to_datetime(bins_date)
sr_binned_clouds = pd.Series(pd.cut(df_data.index, bins_date))
#count
counts = pd.value_counts(sr_binned)
counts_clouds = pd.value_counts(sr_binned_clouds)

#fun to compute , c1 is cloud counts, c2 is total counts
def counts_ratio(c1, c2): 
    return c1/c2
#map
list2 = list(map(counts_ratio, counts_cl, counts))
#compute mean
np.asarray(list2).mean()
#covered area

    #fun to extract info
(df_data["lat"] < lat_max[0]) & (df_data["lat"] > lat_min[0])
#histogram
plt.hist2d(list1, df_data["htang"], bins=[10, 20])

p1 = pd.value_counts(df_data[df_data["data_range"] == counts.index[0]]["lat_range"]).sort_index()[7]

pd.date_range(start='2/1/2018', periods=11, freq='3D')[-1]

