# -*- coding: utf-8 -*-
"""
Created on Thu May 10 13:24:34 2018

@author: RuxandraV
"""
import utils as ut

import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelBinarizer
    
"""         Data      """
all_data = pd.read_hdf('processed_similarity.hdf5', 'Datataset1/X')
selected_features = ['Return_last_year', 'Size', 'Sector', 'Region']
# X will contain data with binarized variables
X = all_data[selected_features]
# Y keeps selected data in original (string) form 
Y = all_data.copy()
Y = Y[['Return_last_year', 'Size', 'Sector_string', 'Region_string']]
# list of all stocks in data
X_index = X.index.tolist()


"""         Scale feature size to [0,1]      """
size = ut.encodeSize(X)
X = X.drop('Size', axis = 1)

"""         Binarize Sector and Region      """
sector = X['Sector'].values.reshape(-1, 1)
lb = LabelBinarizer().fit(sector).transform(sector)
sector_lb = pd.DataFrame(data = lb, index = X_index, columns = ['Sector_1', 'Sector_2', 'Sector_3', 'Sector_4', 
                                                                'Sector_5', 'Sector_6', 'Sector_7', 'Sector_8', 
                                                                'Sector_9'])
region = X['Region'].values.reshape(-1, 1)
lb = LabelBinarizer().fit(region).transform(region)
region_lb = pd.DataFrame(data = lb, index = X_index, columns = ['Region_1', 'Region_2', 'Region_3', 'Region_4', 
                                                                'Region_5', 'Region_6', 'Region_7', 'Region_8'])
"""         Scale returns to [0,1]          """
returns = X['Return_last_year'].values.reshape(-1, 1)
X = X.drop('Return_last_year', axis = 1)
returns_scaled = MinMaxScaler().fit(returns).transform(returns)
returns_scaled = pd.DataFrame(returns_scaled, columns = ['Return_last_year'], index = X_index)

"""         Put everything together in a new df         """
X = pd.concat([returns_scaled, size, sector_lb, region_lb], axis=1)

"""         Export         """
X.to_hdf('diversifier_data.hdf5', 'X', format = 'table')
Y.to_hdf('diversifier_data.hdf5', 'Y', format = 'table')

"""         Functions         """
def covariance(name_stock1, name_stock2, var_market):
    beta1 = round(all_data.loc[name_stock1]['Adjusted_beta'], 3)
    beta2 = round(all_data.loc[name_stock2]['Adjusted_beta'], 3)
    
    return round(beta1 * beta2 * var_market, 3)

def cov_matrix(port_arr, var_m):
    df = pd.DataFrame(columns = port_arr)
    for i in range (0, len(port_arr)):
        row = []
        for j in range (0, len(port_arr)):
            row.append(covariance(port_arr[i], port_arr[j], var_m))
        df.loc[port_arr[i]] = row
    return df

def variance(stock, var_m):
    beta = round(all_data.loc[stock]['Adjusted_beta'], 3)
    return round(beta * beta* var_m, 3)

import math
def portfolio_variance(port_dict, var_m):
    cov_port = 1
    stocks = [*port_dict]
    weigths = list(port_dict.values())
    for i in range (0, len(stocks)):
        for j in range (0, len(stocks)):
            cov_port = cov_port + (weigths[i] * weigths[j] * covariance(stocks[i], stocks[j], var_m))
    return round(math.sqrt(cov_port), 2)

def portfolio_volatility(port_dict, var_m):
    stocks = [*port_dict]
    weigths = list(port_dict.values())
    p_vol = 0
    for i in range (0, len(stocks)):
        p_vol = p_vol + weigths[i] * weigths[i] * variance(stocks[i], var_m)
    for i in range(0, len(stocks)):
        for j in range(i+1, len(stocks)):
            p_vol = p_vol + 2 * weigths[i] * weigths[j] * covariance(stocks[i], stocks[j], var_m)
    return round(math.sqrt(p_vol), 2)

def portfolio_returns(port_dict):
    ret = 0
    for k, v in port_dict.items():
        r = round(all_data.loc[k]['Return_last_year'], 3)
        ret = ret + v * r
    return ret
        

    