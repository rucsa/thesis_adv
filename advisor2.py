import scipy as sy
import pandas as pd
import numpy as np
import utils as ut
from random import randint
import recommender as recom

from ClientPortfolio import ClientPortfolio

allSecurities = pd.read_hdf('stocks&etfs.hdf5', 'Datataset1/X').set_index('Name').T.to_dict()

investors = pd.read_hdf('clients.hdf5', 'DatatasetCli')
investors = investors.set_index('Id')
portfolios = pd.read_hdf('portfolios.hdf5', 'DatatasetPort')

exposure_threshold = 0.05

# take on investor
client_id = randint(1, 99)
client = investors.iloc[client_id]

# take his randomly allocated portfolio
c_port = portfolios.iloc[client['Portfolio_Id']]

# instantiate class
client_portfolio = ClientPortfolio(portfolios.iloc[client['Portfolio_Id']].tolist(), 
                                   client)

#set capital of client from portfolio value --sets also a doable goal
portfolio_val, exposure_dict = ut.calculate_portfolio_value(client_portfolio.portfolio, allSecurities)
client_portfolio.setCapital(portfolio_val)

print('\n   ....Logging starts here....\n \n')
print('CLIENT {} \n'.format(client_portfolio.client))
print('PORTFOLIO {} \n \n'.format(client_portfolio.portfolio))

''' refine exposure'''
print ('\n Checking if each security in portfolio complies with 0.05 max exposure \n')

# cut shares from securities with too much exposure
client_portfolio.refine_exposure(allSecurities)

''' check allocation'''
#check allocations after cutting shares
print ('\n Checking allocation after application of max 0.05 exposure \n')
stocks_alloc, bonds_alloc = ut.current_allocation(allSecurities, client_portfolio.portfolio, client_portfolio.getCapital())
print ('Current allocation: {} stocks and {} bonds \n'.format(stocks_alloc, bonds_alloc))

# recommended allocation
recommended_stock_alloc, recommended_bonds_alloc = ut.recommended_allocation(client_portfolio.client['Risk_profile'])

''' balance portfolio '''
print ('\n Started portfolio balancing \n')
if (bonds_alloc < recommended_bonds_alloc):
    # add more bonds
    print ('Not enough bonds. Current bond allocation: {}. Recommended allocation for {} profile: {} \n'.format(bonds_alloc, client_portfolio.client['Risk_profile'], recommended_bonds_alloc))
    client_portfolio.addBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc)
    stocks_alloc, bonds_alloc = ut.current_allocation(allSecurities, client_portfolio.portfolio, client_portfolio.getCapital())   
    print ('\n Modified allocation to: {} stocks and {} bonds'.format(stocks_alloc, bonds_alloc))
    
if (bonds_alloc > recommended_bonds_alloc):
    # remove from bonds
    print ('Too many bonds. Current bond allocation: {}. Recommended allocation for {} profile: {} \n'.format(bonds_alloc, client_portfolio.client['Risk_profile'], recommended_bonds_alloc))
    client_portfolio.removeBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc)
    stocks_alloc, bonds_alloc = ut.current_allocation(allSecurities, client_portfolio.portfolio, client_portfolio.getCapital())   
    print ('\n Modified allocation to: {} stocks and {} bonds'.format(stocks_alloc, bonds_alloc))
    
if (stocks_alloc < recommended_stock_alloc):
    # add more stocks 
    print ('Not enough stocks. Current stock allocation: {}. Recommended allocation for {} profile: {}\n'.format(stocks_alloc, client_portfolio.client['Risk_profile'], recommended_stock_alloc))
    client_portfolio.addStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc)
    stocks_alloc, bonds_alloc = ut.current_allocation(allSecurities, client_portfolio.portfolio, client_portfolio.getCapital())
    print ('\n Modified allocation to: {} stocks and {} bonds'.format(stocks_alloc, bonds_alloc))
    
if (stocks_alloc > recommended_stock_alloc):
    # remove from stocks 
    print ('Too many stocks. Current stock allocation: {}. Recommended allocation for {} profile: {}\n'.format(stocks_alloc, client_portfolio.client['Risk_profile'], recommended_stock_alloc))
    client_portfolio.removeStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc)
    stocks_alloc, bonds_alloc = ut.current_allocation(allSecurities, client_portfolio.portfolio, client_portfolio.getCapital())
    print ('\n Modified allocation to: {} stocks and {} bonds'.format(stocks_alloc, bonds_alloc))