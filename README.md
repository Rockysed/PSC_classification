# PSC_classification
Scripts and functions for PSC classification

In this repository the code developed during the thesis research has been added.
The code can be find in the folder "code"

The most important files are:

* "load_mipas.py" for extracting data from NETCDF4 files of MIPAS
* "filter_mipas.py" for filtering the HDF files (on altitude and cloud index)
  and calculating the BTDs of MIPAS dataset
* "load_csdb.py" for extracting data from NETCDF4 files of CSDB
* "filter_csdb.py" for filtering the HDF files (on altitude and cloud index)
  and calculating the BTDs of CSDB (case with Gaussian noise added to the spectra)
* "autoencoder_classification.py" for performing feature reduction using the autoencoder and classification of MIPAS dataset after training on CSDB
* "random_forest_classification.py" for performing feature reduction using RF and PCA and classification of MIPAS dataset after training on CSDB
* "kpca_classification.py" for performing feature reduction using KPCA and classification of MIPAS dataset after training on CSDB
