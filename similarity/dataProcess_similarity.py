import pandas as pd
from random import choice
import utils as ut
from sklearn import preprocessing

data = pd.read_hdf('SP1500_similarity.hdf5', 'Datataset1/X')
data = data.drop('Raw_beta ', axis = 1)
data = data.drop('Region', axis = 1)
data = data.drop('Asset', axis = 1)

#add random regions
regions = ['South Asia', 'Europe & Central Asia', 'Middle East & North Africa', 'East Asia & Pacific', 'Latin America & Caribbean', 'North America', 'Sub-Saharan Africa']
region = []
for row in data.itertuples():
    region.append(choice(regions))
data['Region'] = pd.Series(region, index=data.index)

# encode the new regions
encoded_region = ut.encode_new_region(data)
data.rename(columns={'Region': 'Region_string'}, inplace=True)
data = pd.concat([data, encoded_region], axis=1)
data = data.set_index('Security')


#target = 'ANR'
#
#if False:
#    # don't serialize target column
#    temp = data[target]
#    data = data.drop(target, axis = 1)
#    scaler = preprocessing.StandardScaler() 
#    data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns, index=data.index) 
#    data[target] = temp
#    
#if False:
#    label_digits = [1, 2, 3, 4, 5]
#    label_str = ['strong sell', 'sell', 'hold', 'buy', 'strong buy']
#    y =  data['ANR']
#    data = data.drop('ANR', axis = 1)
#    y_class = pd.cut(y, bins=[0, 1, 2, 3, 4, 5], include_lowest=True, labels=label_digits)
#    data['ANR'] = y_class
    
data.to_hdf('processed_similarity_new_regs.hdf5', 'Datataset1/X', format = 'table')