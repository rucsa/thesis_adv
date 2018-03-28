import scipy as sy
import pandas as pd
import numpy as np
import utils as ut

from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing

data = pd.read_excel('data/SP1500.xlsx')
#data = data.set_index('Security')
if False:
    data = data.drop('Ticker symbol', axis = 1)
    data = data.drop('Region', axis = 1)

#fetaures = list(data.columns.values)

# create features
data['PSR'] = data.loc[:,'Market_cap'] / data.loc[:,'Revenue']
feature_set = ['Inventory_turnover', 'Revenue', 'Gross_profit', 
               'Net_income', 'Operational_cash_flow',
                            'Assets']
size = ut.encodeMarketCap(data)
data = pd.concat([data, size], axis=1)
data = ut.scaleOutMarketCap(data, feature_set)
if False:
    data.loc[:,'Market_cap'] = data.loc[:,'Market_cap']/1000
    data.loc[:,'Revenue'] = data.loc[:,'Revenue']/100
    data.loc[:,'Gross_profit'] = data.loc[:,'Gross_profit']/100
    data.loc[:,'Net_income'] = data.loc[:,'Net_income']/10
    data.loc[:,'Operational_cash_flow'] = data.loc[:,'Operational_cash_flow']/100
    data.loc[:,'Assets'] = data.loc[:,'Assets']/100
    
if True:
    data.loc[:,'Ethics'] = data.loc[:,'Ethics'].fillna(value='N', inplace = False)
    data.loc[:,'Bribery'] = data.loc[:,'Bribery'].fillna(value='N', inplace = False)
    encoded_ethics, encoded_bribery = ut.encode_binary(data)
    data = data.drop('Ethics', axis = 1)
    data = data.drop('Bribery', axis = 1)
    data = pd.concat([data, encoded_ethics, encoded_bribery], axis=1)

# encode sector
if False:
    encoded_sector = ut.encode_sector(data)
    data = data.drop('Sector', axis = 1)
    data = pd.concat([data, encoded_sector], axis=1)

#data = data.dropna(axis = 0, how = 'any')
#df = data[['Inventory_turnover', 'Market_cap']].copy()
#df = pd.DataFrame(df)
#df = df.sort_values(by='Market_cap')

# remove samples with no ANR
if True:
    data = data.fillna(0)
    data = data.loc[data['ANR'] > 0]
    
y = data.loc[:, 'ANR']
#data = data.drop('ANR', axis=1)
# create bins for classification
if False:
    y_class = pd.cut(y, bins=[0, 1.5, 2.5, 3.5, 4.5, 5], include_lowest=True, labels=[1, 2, 3, 4, 5])
    y_class = pd.DataFrame(y_class)

nans_n = data.isnull().sum()

if False:
    scaler = preprocessing.StandardScaler() 
    data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns, index=data.index) 
    data = pd.concat([data, y], axis='columns')
    
data.to_hdf('SP1500.hdf5', 'Datataset1/X')