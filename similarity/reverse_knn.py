import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances

def reverse_knn(X, Y, n_neighbors):
    dist = pairwise_distances(allsecurities, security.values.reshape(1,-1), 'euclidean', n_jobs=1, squared=True)
    dist = np.array(dist).reshape(-1,)
    # sorted by highest distance first
    n_ind = dist.argsort()[::-1][:k]
    return n_ind, dist[n_ind]

allsecurities = pd.read_hdf('processed_similarity.hdf5', 'Datataset1/X')
security_id = 44
k = 10
print("\nChosen security:")
security = allsecurities.iloc[security_id, :]
print(allsecurities.iloc[[security_id]].index)

neighbours = reverse_knn(allsecurities, security, k)

print("\nFarthest {} neighbours:".format(k-1))
for x, d in zip(np.nditer(neighbours[0]), np.nditer(neighbours[1])):
    if (x.item() != security_id):
        n = allsecurities.iloc[[x.item()]]
        print("{} with index {} and distance {}".format(n.index, x, d))

