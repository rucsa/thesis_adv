import scipy as sy
import pandas as pd
import numpy as np
from operator import itemgetter
from random import randint
import recommender as recom
import utils as ut
from collections import OrderedDict

from ClientPortfolio4 import ClientPortfolio

#random.seed(27)

allSecurities = pd.read_hdf('stocks&etfs.hdf5', 'Datataset1/X').set_index('Name').T.to_dict()

investors = pd.read_hdf('clients.hdf5', 'DatatasetCli')
investors = investors.set_index('Id')
portfolios = pd.read_hdf('portfolios.hdf5', 'DatatasetPort')

exposure_threshold = 5

# take on investor
client_id = randint(1, 99)
client = investors.iloc[client_id]

# take his randomly allocated portfolio
c_port = portfolios.iloc[client['Portfolio_Id']]

# instantiate class
client_portfolio = ClientPortfolio(portfolios.iloc[client['Portfolio_Id']].tolist(), 
                                   client)

divers_sectors = ['Consumer, Non-cyclical', 'Financial', 'Technology',
                  'Industrial', 'Consumer, Cyclical', 
                  'Energy', 'Basic Materials',
                  'Utilities', 'Communications']
divers_percent = [24.02, 18.1, 16.8, 14.73, 9.04, 6.32, 5.25, 2.97, 2.77]

# categorize existing securities by type of asset
print ('\n*** Portfolio analysis.... ***\n')
stocks_held, bonds_held = client_portfolio.extract_securities_by_type(allSecurities)

# categorize existing securities by sector
portfolio_sector_dict = client_portfolio.categorize_stocks_by_sector(allSecurities)

# calculate recommended percentages per sector
recomm_sector_dict = recom.recomm_sector_allocation(client_portfolio.portfolio, divers_percent, divers_sectors, sum(portfolio_sector_dict.values()))

# add recommended sectors that do not exist
sectors_to_del = client_portfolio.sectors_you_should_not_have(recomm_sector_dict, portfolio_sector_dict)
if (len(sectors_to_del)==0):
    print ('No sectors to remove')
else:
    for sector_del in sectors_to_del:
        client_portfolio.deleteSector(sector_del, allSecurities)
    

# refine securities per sector
print ('\n *** Refining exposure for sectors you hold ***')
for key, value in recomm_sector_dict.items():
    
    diff = recomm_sector_dict[key] - portfolio_sector_dict.get(key, 0) 
    
    if (diff == recomm_sector_dict[key]):
        # portfolio does not contain the recommended sector
        print ('\n No {} in the portfolio. You should add {} of them'.format(key, value))
        recommendations = recom.rank_stocks_without_bc(key)
        pop = recom.recommend_stock(recommendations)  
        security = next(pop)
        client_portfolio.addNewSecurity(security, value)
        
    elif (diff > 0):
        print ('\n You have {} of {}. You should have {} of sector {}. diff is {}'.format(portfolio_sector_dict.get(key, 0), key, recomm_sector_dict.get(key, 0), key, diff))
        current_holdings = client_portfolio.extract_securities_by_sector(key, allSecurities)
        print (current_holdings)
        print (len(current_holdings))

        recommendations = recom.rank_stocks_without_bc(key)
        pop = recom.recommend_stock(recommendations)  
        security = next(pop)
        client_portfolio.addNewSecurity(security, diff)
        
    elif (diff < 0):
        print ('\n You have {} of {}. You should have {} of sector {}. diff is {}'.format(portfolio_sector_dict.get(key, 0), key, recomm_sector_dict.get(key, 0), key, diff))
        current_holdings = client_portfolio.extract_securities_by_sector(key, allSecurities)
        print (current_holdings)
        print (len(current_holdings))
        current_holdings_list = sorted(current_holdings, key=current_holdings.get, reverse=True)
        diff = diff * (-1)
        for k in current_holdings_list:
            v = current_holdings[k]
            if diff == 0:
                break
            elif (diff > 0  and v > diff):
                client_portfolio.setExposure(k, v - diff)
                diff = 0
            elif (diff > 0  and v <= diff):
                client_portfolio.deteleSecurity(k)
                diff -= v
                

print ('\n \n Exposure left in portfolio: {}'.format(client_portfolio.extra_exposure))
stocks_held, bonds_held = client_portfolio.extract_securities_by_type(allSecurities)       
        
