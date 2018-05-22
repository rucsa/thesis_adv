# -*- coding: utf-8 -*-
"""
Created on Thu May 17 10:59:27 2018

@author: RuxandraV
"""

import pandas as pd
import numpy as np
import utils as ut
import visualizations as visual
import matplotlib.pyplot as plt

from random import randint
from itertools import combinations
from diversifier_prepare_data import covariance, cov_matrix, variance, portfolio_variance, portfolio_volatility, portfolio_returns
from rank_by_preferences import rank_by_preferences
from ClientPortfolio8 import ClientPortfolio
from sklearn.cluster import KMeans, AgglomerativeClustering


X = pd.read_hdf('diversifier_data.hdf5', 'X', format = 'table')
Y = pd.read_hdf('diversifier_data.hdf5', 'Y', format = 'table')
all_data = pd.read_hdf('processed_similarity.hdf5', 'Datataset1/X').T.to_dict()
alldata = pd.read_hdf('processed_similarity.hdf5', 'Datataset1/X')
header = X.columns.values.tolist()

"""         Pick a client and a portfolio         """
#portfolio = ['Broadcom', 3, 'Teledyne Technologies Inc', 3, 'Liquidity Services', 8, 'Brookline Bancorp', 9, 'Steel Dynamics Inc', 4, 'Dentsply Sirona', 6, 'Miller, Herman Inc', 9, 'FirstEnergy Corp', 6, 'Green Plains Energy', 6]
investors = pd.read_hdf('clients-sim.hdf5', 'DatatasetCli').set_index('Id')
portfolios = pd.read_hdf('portfolios-sim.hdf5', 'DatatasetPort')
client_id = randint(1, 99)
client = investors.iloc[client_id]
#row = ['HealthStream', 6, 'AT&T Inc', 9, 'Verisign Inc.', 8]
#row = ['Corindus Vascular Robotics', 2, 'Scholastic', 3, 'HealthStream', 6, 'AT&T Inc', 9, 'Verisign Inc.', 8, 'DHI Group', 4, 'Comtech', 4]
row = ['Jack Henry & Associates Inc', 7, 'ITT Inc', 6, 'News Corp. Class A', 4, 'Northwest Bancshares', 7, 'Neenah Paper', 4, 'Molina Healthcare Inc', 6]
client_portfolio = ClientPortfolio(row, #portfolios.iloc[client['Portfolio_Id']].tolist(),
                                   client)

"""         Transform portfolio into dataframe with binarized values         """
held = ut.dict_to_df(client_portfolio.portfolio, header, X)
held_str = ut.dict_to_df(client_portfolio.portfolio, alldata.columns.values.tolist(), alldata)

"""         Configure weights         """
weigths = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
X = np.multiply(X, weigths)

"""         KMEANS Split data into clusters         """
kmeans = KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=300, tol=0.0001, 
                        precompute_distances='auto', verbose=0, random_state=None, 
                        copy_x=True, n_jobs=1, algorithm='auto')
option_list, p_cls_k, k_rest_of_stocks = ut.get_recommendations_from_clusters(X, held, Y, kmeans, 30)
held_str = ut.dict_to_df(client_portfolio.portfolio, alldata.columns.values.tolist(), alldata)
visual.visualize(held_str, option_list, 'temp-plot.html')

"""         AgglomerativeClustering Split data into clusters         """    
agg = AgglomerativeClustering(n_clusters=2, linkage="average", affinity="euclidean")
option_list_agg, p_cls_agg, rest_of_stocks = ut.get_recommendations_from_clusters(X, held, alldata, agg, 30)
visual.visualize(held_str, option_list_agg, 'temp-plot2.html')

"""         Evaluate clusters         """  
var_m = 13.16


""" Add stocks from RANDOM recommendations """ 
random_port = ClientPortfolio(row, client)

n, p_vars, r = [], [], []
n.append(len(random_port.portfolio))
p_vars.append(portfolio_variance(random_port.portfolio, var_m))
r.append(portfolio_returns(random_port.portfolio))
for i in range (1, 15):
    pick = alldata.iloc[randint(0, len(alldata.index)-1)].name 
    random_port.addNewSecurity(pick, 5, all_data)
    n.append(len(random_port.portfolio))
    p_vars.append(portfolio_variance(random_port.portfolio, var_m))
    r.append(portfolio_returns(random_port.portfolio))

plt.figure(1, figsize=(15, 15))   
plt.subplot(211) 
plt.plot(n, p_vars, color='red', label = 'variance')
plt.plot(n, r, color='purple', label = 'returns last year')
plt.xlabel('number of stocks')
plt.ylabel('portfolio variance')
plt.legend()
plt.title("Portfolio variance with RANDOM recommendations")

""" Add stocks from AGG recommendations """  
portfolio_copy = ClientPortfolio(row, client)
 
n, p_vars, r = [], [], []
n.append(len(portfolio_copy.portfolio))
p_vars.append(portfolio_variance(portfolio_copy.portfolio, var_m))  
r.append(portfolio_returns(portfolio_copy.portfolio))
for i in range (1, 15):  
    pick = option_list_agg.iloc[randint(0, len(option_list_agg.index)-1)].name  
    portfolio_copy.addNewSecurity(pick, 5, all_data)
#    print ("\nRecommender picks {} for AGG from cluster {}".format(pick, option_list_agg.loc[pick]['Cluster']))
#    print ("Portfolio variance {}".format(portfolio_variance(portfolio_copy.portfolio, var_m)))
#    print ("Portfolio volatility {}".format(portfolio_volatility(portfolio_copy.portfolio, var_m)))
    n.append(len(portfolio_copy.portfolio))
    p_vars.append(portfolio_variance(portfolio_copy.portfolio, var_m))
    r.append(portfolio_returns(portfolio_copy.portfolio))
    held = ut.dict_to_df(client_portfolio.portfolio, header, X)
    #recalculate clusters
    #option_list_agg, p_cls_agg = ut.get_recommendations_from_clusters(X, held, Y, agg, 30)
   
plt.subplot(212)
plt.plot(n, p_vars, color='red', label = 'variance')
plt.plot(n, r, color='purple', label = 'returns last year')
plt.xlabel('number of stocks')
plt.ylabel('portfolio variance')
plt.title("Portfolio variance with agglomerative recommendations")
plot_name = 'portofolio_variance_plots/plot_iter_' + str(randint(1, 1000)) + '.png'
plt.legend()
plt.savefig(plot_name)
plt.show()
plt.close()

