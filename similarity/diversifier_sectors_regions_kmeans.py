# -*- coding: utf-8 -*-
"""
Created on Fri May 18 10:40:36 2018

@author: RuxandraV
"""

import pandas as pd
from random import choice
import utils as ut
import numpy as np
from sklearn import preprocessing
import recommender as recom
from sklearn.cluster import KMeans, AgglomerativeClustering
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import diversifier_stock_picker
from diversifier_visual import diversifier_visual

alldata = pd.read_hdf('processed_similarity_new_regs.hdf5', 'Datataset1/X', format = 'table')
alldata = alldata.drop(['Sector'], axis = 1)

# encode sector
economy = 'Early' #input('Insert economy (Mid, Late, Recession, Early).. ')
keys, vals = recom.bc_sector_allocation(economy)
alldata = pd.concat([alldata, ut.encode_sector_from_bc(alldata, keys, vals)], axis=1)
alldata = alldata.drop(['Sector_string', 'Region_string'], axis = 1)
del keys, vals, economy

""" Cluster stocks on regions and sectors """

data = alldata[['Sector', 'Region']]
portfolio = {'Amazon.com Inc': 5}
held = ut.dict_to_df(portfolio, ['Sector', 'Region'], data)

# KMEANS Split data into clusters      
model = KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=300, tol=0.0001, 
                        precompute_distances='auto', verbose=0, random_state=None, 
                        copy_x=True, n_jobs=1, algorithm='auto')
#model = AgglomerativeClustering(n_clusters=2, linkage="average", affinity="chebyshev")

option_list, port_clusters, rest_of_stocks, labels, option_list_cs, rest_of_stocks_cs = ut.get_recommendations_from_clusters(data, held, data, model, 20, 5)
cluster_count = Counter(labels)

""" pick a stock """
stocks = diversifier_stock_picker.pick_closest_stock(option_list, held) #rank closest stocks
s = held['Sector'].unique()
r = held['Region'].unique()
pop = diversifier_stock_picker.recommend_stock(stocks.index.values)  
stock = next(pop)
ss = stocks.loc[stock]['Sector']
rr = stocks.loc[stock]['Region']
while ss in s or rr in r:
    stock = next(pop)
    ss = stocks.loc[stock]['Sector']
    rr = stocks.loc[stock]['Region']


""" plooot plot plot plot plot ploooooot """ 
colors = ['lightcoral', 'darkorange', 'olive', 'g', 'c', 'maroon', 'yellowgreen', 
          'mediumblue', 'pink', 'dimgrey', 'peru', 'limegreen', 'royalblue',
          'mediumorchid', 'tomato', 'orangered', 'lime', 'crimson', 'deepskyblue']
option_list['Cluster'] = option_list_cs
rest_of_stocks['Cluster'] = rest_of_stocks_cs
diversifier_visual(option_list, rest_of_stocks, held, stocks.loc[stock], cluster_count, colors, labels, data)

# add stock to portfolio
held = pd.concat([held, stocks], axis = 0)


