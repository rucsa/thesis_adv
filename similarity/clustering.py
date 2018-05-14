import pandas as pd
import numpy as np
from random import randint
from sklearn.cluster import KMeans
from collections import Counter
from ClientPortfolio8 import ClientPortfolio
import utils as ut
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

allsecurities = pd.read_hdf('processed_similarity.hdf5', 'Datataset1/X')
select_features = [ 'Return_last_year', 'Size']
X = allsecurities[select_features]
X_index = X.index.tolist()

size = ut.encodeSize(X)
X = X.drop('Size', axis = 1)

returns = X['Return_last_year'].values.reshape(-1, 1)
X = X.drop('Return_last_year', axis = 1)
returns_scaled = MinMaxScaler().fit(returns).transform(returns)
returns_scaled = pd.DataFrame(returns_scaled, columns = ['Return_last_year'], index = X_index)

X = pd.concat([returns_scaled, size], axis=1)

weigths = np.ones(shape = (1, 2), dtype = np.float64)

investors = pd.read_hdf('clients-sim.hdf5', 'DatatasetCli').set_index('Id')
portfolios = pd.read_hdf('portfolios-sim.hdf5', 'DatatasetPort')

client_id = 97#randint(1, 99)
client = investors.iloc[client_id]
client_portfolio = ClientPortfolio(portfolios.iloc[client['Portfolio_Id']].tolist(), 
                                   client)

held = pd.DataFrame(columns = select_features)
for k, v in client_portfolio.portfolio.items():
    current_security = X.loc[k].to_frame(name = X.loc[k].name).T
    held = pd.concat([held, current_security], axis = 0)

c = 2
found = False
X_matrix = X.as_matrix()
held_matrix = held.as_matrix()

while (not found and c < 11):
    print ("Splitting in {} clusters".format(c))
    kmeans = KMeans(n_clusters=c, init='k-means++', n_init=10, max_iter=300, tol=0.0001, 
                    precompute_distances='auto', verbose=0, random_state=None, 
                    copy_x=True, n_jobs=1, algorithm='auto')
    
    pred = kmeans.fit_predict(X)
    
    countX= Counter(pred)
    prediction = kmeans.predict(held)
    countP = Counter(prediction)
    
    if len(countP) < len(countX):
        found = True
        countX_keys = list(countX.keys())
        countP_keys = list(countP.keys())
        # find the unused cluster
        diff = np.setdiff1d(countX_keys, countP_keys)
        # save securities that are in the new cluster
        option_list = pd.DataFrame()
        for i in range(0, len(pred)):
            if pred[i] == diff[0]:
                # the new security to add will be taken from 
                option_list = option_list.append(X.iloc[i])
    else:
       c = c+1
       
    # plot
    color = ["green", "red", "blue", "cyan", "yellow", "magenta"]
    color = color[: c+1]
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    plt.scatter(centroids[:, 0],centroids[:, 1], marker = "x", s=50, linewidths = 5, zorder = 10, color = 'black')
    
    for i in range(0, len(X_matrix)):
        plt.scatter(X_matrix[i][0], X_matrix[i][1], c=color[labels[i]])
    for i in range(0, len(held_matrix)):
        plt.scatter(held_matrix[i][0], held_matrix[i][1], c='black', marker = 'o')
    option_matrix = option_list.as_matrix()
    for i in range(0, len(option_matrix)):
        plt.scatter(option_matrix[i][0], option_matrix[i][1], c='yellow', marker = 'o')
    
    plt.show()
    plt.close()
   
print(option_list)
    