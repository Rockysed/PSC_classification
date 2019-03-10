import os
import numpy as np
from netCDF4 import Dataset
import datetime
from dateutil.relativedelta import relativedelta

def date2string(t): 
    delta = relativedelta(years=30)
    return (datetime.datetime.fromtimestamp(t)+delta).strftime("%Y-%m-%d")
#iterate over files
files = [i for i in os.listdir("../data/mipas/2009") if i.endswith(".nc")]
lat_app = np.empty([0,1])
for file in files:
    date = file.split("_")[1]+"_"+file.split("_")[2].split(".")[0]
    dataset = Dataset(os.path.join('../data/mipas/2009', file))
    # load variables
    lat = dataset.variables['latitude'][:]
    time = dataset.variables['time'][:]
    htang = dataset.variables['htang'][:]
    dataset.close()
    df_lt = pd.DataFrame(lat, columns = ["lat"])
    df_lt["time"]=time
    df_lt["htang"]=htang
    list_date = list(map(date2string, time))
    list_date = pd.to_datetime(list_date)    
    df_lt["date"]=list_date
    df_lt.to_hdf(os.path.join('../data/mipas_pd_lat_time', date + '.h5'), key='df_lt',
          format='table')

#print variables length
print(np.shape(lat_app))