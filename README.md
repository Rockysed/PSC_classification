# PSC_classification
Scripts and functions for PSC classification

In this repository the code developed during the thesis research has been added.
The code can be find in the folder "code". All the code is compatible with Python3.
Installation of specific packages is needed.

**The most important files are:**

* "load_mipas.py" for extracting data from NETCDF4 files of MIPAS
* "filter_mipas.py" for filtering the HDF files (on altitude and cloud index)
  and calculating the BTDs of MIPAS dataset
* "load_csdb.py" for extracting data from NETCDF4 files of CSDB
* "filter_csdb.py" for filtering the HDF files (on altitude and cloud index)
  and calculating the BTDs of CSDB (case with Gaussian noise added to the spectra)
* "autoencoder_classification.py" for performing feature reduction using the autoencoder and classification of MIPAS dataset after training on CSDB
* "random_forest_classification.py" for performing feature reduction using RF and PCA and classification of MIPAS dataset after training on CSDB
* "kpca_classification.py" for performing feature reduction using KPCA and classification of MIPAS dataset after training on CSDB
* "plot_psc.py" for plotting PSCs in specific days for MIPAS
* "plot_mat.py" for plotting time series and bin counts for MIPAS
* "plot_pie.py" for plotting pie charts for MIPAS
* "plot_bar_mipas.py" for plotting coincidence statistics of class predictions among the different classification schemes

**In the "plots" folder plots  not included in the thesis document can be found**
