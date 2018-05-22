# -*- coding: utf-8 -*-
"""
Created on Fri May 18 10:40:36 2018

@author: RuxandraV
"""

import pandas as pd
from random import choice, shuffle
import utils as ut
import numpy as np
from sklearn import preprocessing
import recommender as recom
from sklearn.cluster import KMeans, AgglomerativeClustering

import matplotlib.pyplot as plt

from collections import Counter

alldata = pd.read_hdf('processed_similarity_new_regs.hdf5', 'Datataset1/X', format = 'table')
alldata = alldata.drop(['Sector'], axis = 1)

# encode sector
economy = 'Mid' #input('Insert economy (Mid, Late, Recession, Early).. ')
keys, vals = recom.bc_sector_allocation(economy)
alldata = pd.concat([alldata, ut.encode_sector_from_bc(alldata, keys, vals)], axis=1)

del keys, vals, economy

""" Cluster stocks on regions and sectors """

data = alldata[['Sector', 'Region']]
portfolio = {'Amazon.com Inc': 5, 'Ameren Corp': 5}
held = ut.dict_to_df(portfolio, ['Sector', 'Region'], data)

# Agglomerative Split data into clusters      
agg = AgglomerativeClustering(n_clusters=2, linkage="average", affinity="euclidean")
option_list, port_clusters, rest_of_stocks, labels = ut.get_recommendations_from_clusters(data, held, data, agg, 20, 9)
held_str = ut.dict_to_df(portfolio, alldata.columns.values.tolist(), alldata)

#append cluster labels to data df
clusters = pd.DataFrame(labels, index = list(data.index.values), columns = ['Cluster'])
data = pd.concat([data, clusters], axis = 1)
del clusters 
cluster_count = Counter(labels)

""" plooot plot plot plot plot ploooooot """ 
colors = ['lightcoral', 'darkorange', 'olive', 'g', 'c', 'maroon', 'yellowgreen', 
          'mediumblue', 'pink', 'dimgrey', 'peru', 'limegreen', 'royalblue',
          'mediumorchid', 'tomato', 'orangered', 'lime', 'crimson', 'deepskyblue']

fig = plt.figure(figsize=(10, 8))
fig.tight_layout()
fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)

ax = fig.add_subplot(311)
for i in range(0, len(cluster_count)):
    d = option_list[option_list.Cluster == i]
    scatter = ax.scatter(d['Sector'], d['Region'], c = colors[i], s=10)
scatter = ax.scatter(held['Sector'],held['Region'], c='black', s=25, marker = 'x')
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
