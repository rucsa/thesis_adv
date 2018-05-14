import pandas as pd
import numpy as np
from random import randint
from sklearn.cluster import KMeans
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
weigths = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
X = np.multiply(X, weigths)


"""         Pick a client and a portfolio         """
investors = pd.read_hdf('clients-sim.hdf5', 'DatatasetCli').set_index('Id')
portfolios = pd.read_hdf('portfolios-sim.hdf5', 'DatatasetPort')
client_id = randint(1, 99)
client = investors.iloc[client_id]
client_portfolio = ClientPortfolio(portfolios.iloc[client['Portfolio_Id']].tolist(), 
                                   client)

"""         Transform portfolio into dataframe         """
held = pd.DataFrame(columns = header)
for k, v in client_portfolio.portfolio.items():
    current_security = X.loc[k].to_frame(name = X.loc[k].name).T
    held = pd.concat([held, current_security], axis = 0)
    
"""         Split data into clusters         """
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
                current_security = allsecurities.iloc[i].to_frame(name = allsecurities.iloc[i].name).T
                option_list = pd.concat([option_list, current_security], axis = 0)
    else:
       c = c+1
     
#client_portfolio.pretty_print_portfolio(allsecurities.T.to_dict())
"""         Transform output into dataframe         """
held = pd.DataFrame(columns = allsecurities.columns.values.tolist())
for k, v in client_portfolio.portfolio.items():
    current_security = allsecurities.loc[k].to_frame(name = allsecurities.loc[k].name).T
    held = pd.concat([held, current_security], axis = 0)
    
"""         Visualization         """    
print ("Check browser for visualization")
visual.visualize(held, option_list)

"""         Recommendations         """
# TODO: fix data frame index - security - name confusion
option_list['Name'] = option_list.index
#option_list.reset_index(level = 0, inplace = True)
ranked_options = rank_by_preferences([1,3,4,5,6], option_list, None, False).index.values.tolist()

print (Y.loc[ranked_options[0]])
print (Y.loc[ranked_options[1]])
print (Y.loc[ranked_options[2]])
print (Y.loc[ranked_options[3]])
print (Y.loc[ranked_options[4]])