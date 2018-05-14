# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:55:53 2018

@author: RuxandraV
"""

import pandas as pd
import numpy as np
from random import randint
from sklearn.cluster import KMeans, AgglomerativeClustering
from collections import Counter
from ClientPortfolio8 import ClientPortfolio
import utils as ut
from sklearn.preprocessing import MinMaxScaler
#import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelBinarizer
#from matplotlib import style
#style.use("ggplot")
#from mpl_toolkits.mplot3d import Axes3D

import visualizations as visual
from rank_by_preferences import rank_by_preferences

allsecurities = pd.read_hdf('processed_similarity.hdf5', 'Datataset1/X')
select_features = ['Return_last_year', 'Size', 'Sector', 'Region']
X = allsecurities[select_features]
Y = allsecurities.copy()
Y = Y[['Return_last_year', 'Size', 'Sector_string', 'Region_string']]
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
header = X.columns.values.tolist()

"""         Configure weights         """
#weigths = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2]
weigths = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
X = np.multiply(X, weigths)


"""         Pick a client and a portfolio         """
#portfolio = ['Broadcom', 3, 'Teledyne Technologies Inc', 3, 'Liquidity Services', 8, 'Brookline Bancorp', 9, 'Steel Dynamics Inc', 4, 'Dentsply Sirona', 6, 'Miller, Herman Inc', 9, 'FirstEnergy Corp', 6, 'Green Plains Energy', 6]
investors = pd.read_hdf('clients-sim.hdf5', 'DatatasetCli').set_index('Id')
portfolios = pd.read_hdf('portfolios-sim.hdf5', 'DatatasetPort')
client_id = 46#randint(1, 99)
client = investors.iloc[client_id]
client_portfolio = ClientPortfolio(portfolios.iloc[client['Portfolio_Id']].tolist(),
                                   client)

"""         Transform portfolio into dataframe         """
held = pd.DataFrame(columns = header)
for k, v in client_portfolio.portfolio.items():
    current_security = X.loc[k].to_frame(name = X.loc[k].name).T
    held = pd.concat([held, current_security], axis = 0)
    
"""         KMEANS Split data into clusters         """
c = 2
found = False
X_matrix = X.as_matrix()
held_matrix = held.as_matrix()

while (not found and c < 11):
    print ("Trying to split in {} clusters".format(c))
    kmeans = KMeans(n_clusters=c, init='k-means++', n_init=10, max_iter=300, tol=0.0001, 
                    precompute_distances='auto', verbose=0, random_state=None, 
                    copy_x=True, n_jobs=1, algorithm='auto')
    
    pred = kmeans.fit_predict(X)
    
    countX= Counter(pred)
    prediction = kmeans.predict(held)
    countP = Counter(prediction)
    
    if len(countP) + 4 <= len(countX):
        found = True
        countX_keys = list(countX.keys())
        countP_keys = list(countP.keys())
        # find the unused cluster
        diff = np.setdiff1d(countX_keys, countP_keys)
        # save securities that are in the new cluster
        option_list = pd.DataFrame()
        for i in range(0, len(pred)):
            for j in range (0, len(diff)):
                if pred[i] == diff[j]:
                    # the new security to add will be taken from 
                    current_security = allsecurities.iloc[i].to_frame(name = allsecurities.iloc[i].name).T
                    current_security['Cluster'] = pred[i]
                    option_list = pd.concat([option_list, current_security], axis = 0)
    else:
       c = c+1
     
#client_portfolio.pretty_print_portfolio(allsecurities.T.to_dict())
"""         Transform output into dataframe         """
kmean_out = pd.DataFrame(columns = allsecurities.columns.values.tolist())
for k, v in client_portfolio.portfolio.items():
    current_security = allsecurities.loc[k].to_frame(name = allsecurities.loc[k].name).T
    kmean_out = pd.concat([kmean_out, current_security], axis = 0)
 
"""         AgglomerativeClustering Split data into clusters         """    
c_agg = 2
found = False
while (not found and c < 11):
    agg = AgglomerativeClustering(n_clusters=c_agg, linkage="average", affinity="euclidean")
    pred_agg = agg.fit_predict(X)
    
    countX_agg = Counter(pred_agg)
    prediction_agg = agg.fit_predict(held)
    countP_agg = Counter(prediction_agg)
    
    if len(countP_agg) + 4 <= len(countX_agg):
        found = True
        countX_keys_agg = list(countX_agg.keys())
        countP_keys_agg = list(countP_agg.keys())
        # find the unused cluster
        diff_agg = np.setdiff1d(countX_keys_agg, countP_keys_agg)
        # save securities that are in the new cluster
        option_list_agg = pd.DataFrame()
        for i in range(0, len(pred_agg)):
            for j in range (0, len(diff_agg)):
                if pred_agg[i] == diff_agg[j]:
                    # the new security to add will be taken from 
                    current_security_agg = allsecurities.iloc[i].to_frame(name = allsecurities.iloc[i].name).T
                    current_security['Cluster'] = pred_agg[i]
                    option_list_agg = pd.concat([option_list_agg, current_security_agg], axis = 0)
    else:
       c_agg = c_agg+1
       
"""         Transform output into dataframe         """
agg_out = pd.DataFrame(columns = allsecurities.columns.values.tolist())
for k, v in client_portfolio.portfolio.items():
    current_security = allsecurities.loc[k].to_frame(name = allsecurities.loc[k].name).T
    agg_out = pd.concat([agg_out, current_security], axis = 0)

"""         Visualization         """    
print ("Check browser for visualization")
visual.visualize(kmean_out, option_list, 'temp-plot.html')
visual.visualize(agg_out, option_list_agg, 'temp-plot2.html')

"""         Recommendations         """
# TODO: fix data frame index - security - name confusion
option_list['Name'] = option_list.index
option_list_agg['Name'] = option_list_agg.index
#option_list.reset_index(level = 0, inplace = True)
ranked_options = rank_by_preferences([1,3,4,5,6], option_list, None, False).index.values.tolist()
ranked_options_agg = rank_by_preferences([1,3,4,5,6], option_list_agg, None, False).index.values.tolist()
print ("\nRecommendations from KMeans")
ranked_options_kmeans = pd.DataFrame(columns = Y.columns.values.tolist())
for i in range(0, len(ranked_options)):
    opt = Y.loc[ranked_options[0]]
    ranked_options_kmeans = pd.concat([ranked_options_kmeans, Y.loc[ranked_options[i]]], axis = 0)

print ("\nTop 5 recommendations from AgglomerativeClustering")
print (Y.loc[ranked_options_agg[0]])
print (Y.loc[ranked_options_agg[1]])
print (Y.loc[ranked_options_agg[2]])
print (Y.loc[ranked_options_agg[3]])
print (Y.loc[ranked_options_agg[4]])