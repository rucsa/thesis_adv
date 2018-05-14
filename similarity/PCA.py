import pandas as pd
import numpy as np
from random import randint, choice
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

allsecurities = pd.read_hdf('processed_similarity.hdf5', 'Datataset1/X')
#allsecurities = allsecurities.drop('Asset')

k = 10
security_id = 85#randint(1, 99) #85 Amazon
target = 'ANR'


y = allsecurities[target]
allsecurities = allsecurities.drop(target, axis = 1)
target_names = ['strong sell', 'sell', 'hold', 'buy', 'strong buy']

pca = PCA(n_components=2, copy=True, whiten=False, svd_solver='auto', tol=0.0, iterated_power='auto', random_state=None)
dim = pca.fit(allsecurities).transform(allsecurities)

# Percentage of variance explained for each components
print('explained variance ratio: {}'.format(str(pca.explained_variance_ratio_)))

plt.figure()
colors = ['navy', 'turquoise', 'darkorange', 'red', 'green']
plt.legend(loc='best', shadow=False, scatterpoints=1)

for color, i, target_name in zip(colors, [0,1,2,3, 4], target_names):
    plt.scatter(dim[y == i, 0], dim[y == i, 1], color=color, alpha=.4, lw=0.5,
                label=target_name)
    plt.title('PCA for class {}'.format(target_name))
    plt.show()
