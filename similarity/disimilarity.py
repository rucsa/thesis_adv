import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from random import randint

allsecurities = pd.read_hdf('processed_similarity.hdf5', 'Datataset1/X')
similar = ['ANR', 'Region', 'Ethics']
disimilar = ['Sector', 'Bribery']

security_id = 85#randint(1, 99) #85 Amazon
k = 10
print("\nChosen security:")
security = allsecurities.iloc[security_id, :]
security_disimilar = security[disimilar]
print("Security {}".format(allsecurities.iloc[[security_id]].index.item()))
print("Looking for similarities in {} values {}".format(similar, security[similar].as_matrix()))
print("Looking for disimilarities in {} values {}".format(disimilar, security_disimilar.as_matrix()))

neigh = NearestNeighbors(n_neighbors=k, radius=1.0, algorithm='auto', leaf_size=30, metric='minkowski', p=2, metric_params=None, n_jobs=1)

X = allsecurities[similar]
neigh.fit(X)

security = security[similar]
neighbours = neigh.kneighbors([security], n_neighbors=k, return_distance=False)

print("\nClosest {} neighbours:".format(k))
i = 1
for x in np.nditer(neighbours):
    if (x.item() != security_id):
        n = allsecurities.iloc[[x.item()]]
        print("{}> Security:{}".format(i, n.index.item())) 
        print("Similarities in {} values {}".format(similar, n[similar].as_matrix()))
        print("Disimilarities in {} values {}".format(disimilar, n[disimilar].as_matrix()))
        found = True
        i = i+1
        for sim in disimilar:
            if (n[sim].item() == security_disimilar[sim]):
                found = False
        if found:
            print("Found one")
    
