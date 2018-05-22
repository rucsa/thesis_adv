import pandas as pd
import numpy as np
from random import randint, choice
from sklearn.neighbors import NearestNeighbors


allsecurities = pd.read_hdf('processed_similarity_new_regs.hdf5', 'Datataset1/X', format = 'table')
allsecurities = allsecurities.drop(['Sector_string', 'Region_string'], axis =1 )
#allsecurities = allsecurities.drop('Asset')
features = allsecurities.columns.tolist()
k = 11
security_id = 85#randint(1, 99) #85 Amazon

print("\nChosen security:")
#security = allsecurities.iloc[security_id, :]
security = allsecurities.loc['Amazon.com Inc']
print(allsecurities.iloc[[security_id]].index)

neigh = NearestNeighbors(n_neighbors=k, radius=1.0, algorithm='auto', leaf_size=30, metric='chebyshev', p=2, metric_params=None, n_jobs=1)
neigh.fit(allsecurities) 

neighbours = neigh.kneighbors([security], n_neighbors=None, return_distance=True)
print("\nClosest {} neighbours:".format(k-1))
result = pd.DataFrame()
stocks = []
for d, x in zip(np.nditer(neighbours[0]), np.nditer(neighbours[1])):
    if (x.item() != security_id):
        n = allsecurities.iloc[[x.item()]]
        stocks.append(n.index)
        print("{} with index {} and distance {}".format(n.index, x, d))
        



