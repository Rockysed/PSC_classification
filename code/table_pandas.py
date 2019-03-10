import seaborn as sns
import pandas as pd
#name features
columns=['CI','NI','BTD1',
     'BTD2','BTD3','BTD4',
     'BTD5']
#from numpy array to Pandas dataframe CSDB
df_features_csdb = pd.DataFrame(features_scaled,columns=columns)
#from numpy array to Pandas dataframe MIPAS
df_features_mipas = pd.DataFrame(features_mipas_scaled,columns=columns)
#compute correlation CSDB
corr_csdb = df_features_csdb.corr()
sns.heatmap(corr_csdb, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),  square=True)
plt.title("Correlation Matrix CSDB")
plt.show()
#compute correlation MIPAS
corr_mipas = df_features_mipas.corr()
sns.heatmap(corr_mipas, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),  square=True)
plt.title("Correlation Matrix MIPAS")
plt.show()