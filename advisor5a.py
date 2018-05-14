import scipy as sy
import pandas as pd
import numpy as np
from operator import itemgetter
from random import randint
import recommender as recom
import utils as ut
from collections import OrderedDict

from ClientPortfolio4 import ClientPortfolio

import advisor5worker as advise

# import data
allSecurities = pd.read_hdf('stocks&etfs.hdf5', 'Datataset1/X').set_index('Name').T.to_dict()
investors = pd.read_hdf('clients.hdf5', 'DatatasetCli').set_index('Id')
portfolios = pd.read_hdf('portfolios.hdf5', 'DatatasetPort')

# take on investor
client = investors.iloc[randint(1, 99)]

# instantiate class
client_portfolio = ClientPortfolio(portfolios.iloc[client['Portfolio_Id']].tolist(), 
                                   client)
    
# process portfolio recommendations
final_portfolio = advise.advisor5(client_portfolio, allSecurities)