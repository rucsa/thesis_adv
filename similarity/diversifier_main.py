# -*- coding: utf-8 -*-
"""
Created on Thu May 10 13:32:30 2018

@author: RuxandraV
"""
import pandas as pd
import numpy as np
import utils as ut
import visualizations as visual
import matplotlib.pyplot as plt

from random import randint
from itertools import combinations
from diversifier_prepare_data import covariance, cov_matrix, variance, portfolio_variance, portfolio_volatility
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
row = ['HealthStream', 6, 'AT&T Inc', 9, 'Verisign Inc.', 8]
client_portfolio = ClientPortfolio(row, #portfolios.iloc[client['Portfolio_Id']].tolist(),
                                   client)

"""         Transform portfolio into dataframe with binarized values         """
held = ut.dict_to_df(client_portfolio.portfolio, header, X)

"""         Configure weights         """
weigths = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
X = np.multiply(X, weigths)

"""         KMEANS Split data into clusters         """
kmeans = KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=300, tol=0.0001, 
                        precompute_distances='auto', verbose=0, random_state=None, 
                        copy_x=True, n_jobs=1, algorithm='auto')
option_list, p_cls_k = ut.get_recommendations_from_clusters(X, held, Y, kmeans, 20)
held_str = ut.dict_to_df(client_portfolio.portfolio, alldata.columns.values.tolist(), alldata)
visual.visualize(held_str, option_list, 'temp-plot.html')

"""         AgglomerativeClustering Split data into clusters         """    
agg = AgglomerativeClustering(n_clusters=2, linkage="average", affinity="euclidean")
option_list_agg, p_cls_agg = ut.get_recommendations_from_clusters(X, held, Y, agg, 20)
visual.visualize(held_str, option_list_agg, 'temp-plot2.html')

"""         Calculate statistics         """  
var_m = 13.16

#print ("Portfolio variance {}".format(portfolio_variance(client_portfolio.portfolio, var_m)))
#print ("Portfolio volatility {}".format(portfolio_volatility(client_portfolio.portfolio, var_m)))
#print("Portfolio has stocks in clusters {}".format(p_cls_k))
#print("Agg Portfolio has stocks in clusters {}".format(p_cls_agg))

""" Add stocks from RANDOM recommendations """ 
random_port = ClientPortfolio(row, client)

n, p_vars = [], []
n.append(len(random_port.portfolio))
p_vars.append(portfolio_variance(random_port.portfolio, var_m))
for i in range (1, 20):
    pick = alldata.iloc[randint(0, len(alldata.index))].name 
    random_port.addNewSecurity(pick, 5, all_data)
    n.append(len(random_port.portfolio))
    p_vars.append(portfolio_variance(random_port.portfolio, var_m))

plt.figure(1, figsize=(15, 15))   
plt.subplot(311) 
plt.plot(n, p_vars, color='red')
plt.xlabel('number of stocks')
plt.ylabel('portfolio variance')
plt.title("Portfolio variance with RANDOM recommendations")


""" Add stocks from KMEANS recommendations """   
client_portfolio = ClientPortfolio(row, client)
n, p_vars = [], []
n.append(len(client_portfolio.portfolio))
p_vars.append(portfolio_variance(client_portfolio.portfolio, var_m))
for i in range (1, 20):
    pick = option_list.iloc[randint(0, len(option_list.index)-1)].name 
    client_portfolio.addNewSecurity(pick, 5, all_data)
#    print ("\nRecommender picks {} for KMEANS from cluster {}".format(pick, option_list.loc[pick]['Cluster']))
#    print ("Portfolio variance {}".format(portfolio_variance(client_portfolio.portfolio, var_m)))
#    print ("Portfolio volatility {}".format(portfolio_volatility(client_portfolio.portfolio, var_m)))
    n.append(len(client_portfolio.portfolio))
    p_vars.append(portfolio_variance(client_portfolio.portfolio, var_m))
    
plt.subplot(312)
plt.plot(n, p_vars, color='red')
plt.xlabel('number of stocks')
plt.ylabel('portfolio variance')
plt.title("Portfolio variance with kmeans recommendations")

  
""" Add stocks from AGG recommendations """  
portfolio_copy = ClientPortfolio(row, client)
 
n, p_vars = [], []
n.append(len(portfolio_copy.portfolio))
p_vars.append(portfolio_variance(portfolio_copy.portfolio, var_m))  
for i in range (1, 20):  
    pick = option_list_agg.iloc[randint(0, len(option_list_agg.index)-1)].name  
    portfolio_copy.addNewSecurity(pick, 5, all_data)
#    print ("\nRecommender picks {} for AGG from cluster {}".format(pick, option_list_agg.loc[pick]['Cluster']))
#    print ("Portfolio variance {}".format(portfolio_variance(portfolio_copy.portfolio, var_m)))
#    print ("Portfolio volatility {}".format(portfolio_volatility(portfolio_copy.portfolio, var_m)))
    n.append(len(portfolio_copy.portfolio))
    p_vars.append(portfolio_variance(portfolio_copy.portfolio, var_m))
   
plt.subplot(313)
plt.plot(n, p_vars, color='red')
plt.xlabel('number of stocks')
plt.ylabel('portfolio variance')
plt.title("Portfolio variance with agglomerative recommendations")
plot_name = 'portofolio_variance_plots/plot_' + str(randint(1, 1000)) + '.png'
plt.savefig(plot_name)
plt.show()
plt.close()