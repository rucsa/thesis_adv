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

alldata = pd.read_hdf('processed_similarity_new_regs.hdf5', 'Datataset1/X', format = 'table')
alldata = alldata.drop(['Sector'], axis = 1)

# encode sector
economy = 'Mid' #input('Insert economy (Mid, Late, Recession, Early).. ')
keys, vals = recom.bc_sector_allocation(economy)
alldata = pd.concat([alldata, ut.encode_sector_from_bc(alldata, keys, vals)], axis=1)
alldata = alldata.drop(['Sector_string', 'Region_string'], axis = 1)

del keys, vals, economy

""" Cluster stocks on regions and sectors """

data = alldata[['Sector', 'Region']]
portfolio = {'Amazon.com Inc': 5, 'Ameren Corp': 5, 'Progress':5}
held = ut.dict_to_df(portfolio, ['Sector', 'Region'], data)

# KMEANS Split data into clusters      
kmeans = KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=300, tol=0.0001, 
                        precompute_distances='auto', verbose=0, random_state=None, 
                        copy_x=True, n_jobs=1, algorithm='auto')
option_list, port_clusters, rest_of_stocks, labels = ut.get_recommendations_from_clusters(data, held, data, kmeans, 20, 1)
held_str = ut.dict_to_df(portfolio, alldata.columns.values.tolist(), alldata)

#append cluster labels to data df
clusters = pd.DataFrame(labels, index = list(data.index.values), columns = ['Cluster'])
data = pd.concat([data, clusters], axis = 1)
del clusters 
cluster_count = Counter(labels)

""" pick a stocks """
neigh = NearestNeighbors(n_neighbors=1, radius=1.0, algorithm='auto', leaf_size=30, metric='chebyshev', p=2, metric_params=None, n_jobs=1)
neigh.fit(alldata.loc[list(option_list.index.values)]) 

neighbours = neigh.kneighbors(alldata.loc[list(held.index.values)], n_neighbors=None, return_distance=True)
stocks = []
for d, x in zip(np.nditer(neighbours[0]), np.nditer(neighbours[1])):
    n = alldata.iloc[[x.item()]]
    stocks.append(n.index[0])
    print("{} with index {} and distance {}".format(n.index[0], x, d))

""" plooot plot plot plot plot ploooooot """ 
colors = ['lightcoral', 'darkorange', 'olive', 'g', 'c', 'maroon', 'yellowgreen', 
          'mediumblue', 'pink', 'dimgrey', 'peru', 'limegreen', 'royalblue',
          'mediumorchid', 'tomato', 'orangered', 'lime', 'crimson', 'deepskyblue']

fig = plt.figure(figsize=(6, 6))
fig.tight_layout()
fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)

ax = fig.add_subplot(311)
for i in range(0, len(cluster_count)):
    d = option_list[option_list.Cluster == i]
    scatter = ax.scatter(d['Sector'], d['Region'], c = colors[i], s=10)
scatter = ax.scatter(held['Sector'],held['Region'], c='black', s=25, marker = 'x')
for i in range(0, len(stocks)):
    scatter = ax.scatter(alldata.loc[stocks[i]]['Sector'], alldata.loc[stocks[i]]['Region'], c='red', s=30, marker = '+')
ax.set_xlabel('Sector')
ax.set_ylabel('Region')
ax.set_xlim(1, 25)
ax.set_ylim(1, 12)
ax.set_title('Recommended stocks clusters')

ax = fig.add_subplot(312)
for i in range(0, len(cluster_count)):
    d = rest_of_stocks[rest_of_stocks.Cluster == i]
    scatter = ax.scatter(d['Sector'], d['Region'], c = colors[i], s=10)
scatter = ax.scatter(held['Sector'],held['Region'], c='black', s=25, marker = 'x')
ax.set_xlabel('Sector')
ax.set_ylabel('Region')
ax.set_xlim(1, 25)
ax.set_ylim(1, 12)
ax.set_title('Not recommended stocks clusters')

ax = fig.add_subplot(313)
for i in range(0, len(cluster_count)):
    d = data[data.Cluster == i]
    scatter = ax.scatter(d['Sector'], d['Region'], c = colors[i], s=10)
scatter = ax.scatter(held['Sector'], held['Region'], c ='black', s=25, marker = 'x')
ax.set_xlabel('Sector')
ax.set_ylabel('Region')
ax.set_xlim(1, 25)
ax.set_ylim(1, 12)
ax.set_title('All data clusters')

