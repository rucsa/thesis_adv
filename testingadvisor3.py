import time
import pandas as pd
from pyfancy import pyfancy
from random import randint, choice
import utils as ut

from ClientPortfolio4 import ClientPortfolio
from advisor1worker import advisor1
from advisor3worker import advisor3, getAllocations
from advisor5worker import advisor5

import recommender as recom

import warnings
warnings.filterwarnings("ignore")

def addBondsToBalance(security_dict, bonds_alloc, recommended_bonds_alloc, recommendations, exposure = True, exposure_threshold = 5):
    recommendations = recom.rank_etfs()  
    pop = recom.recommend_etf(recommendations)  
    while (bonds_alloc < recommended_bonds_alloc):
        # get a recommendation
        security = next(pop)
        print ('Checking if bond {} exists in portfolio'.format(security))
        # check if the recommended security is in the portfolio already and get the second best if it is
        while client_portfolio.check_security_in_portfolio(client_portfolio.portfolio, security):
            print ('Bond {} exists in portfolio'.format(security))
            security = next(pop)
            print ('Checking if bond {} exists in portfolio'.format(security))
        # desired exposure
        if (exposure):
            fit_exposure = min(exposure_threshold, (recommended_bonds_alloc - bonds_alloc))  
        else:
            fit_exposure = recommended_bonds_alloc - bonds_alloc
        # add shares to portfolio
        client_portfolio.addNewSecurity(security, fit_exposure)
        # increase bond allocation
        bonds_alloc += fit_exposure 
        
def removeBondsToBalance(security_dict, bonds_alloc, recommended_bonds_alloc, recommendations, exposure = True):
    recommendations = recom.rank_etfs()  
    pop = recom.reversed_recommend_etf(recommendations) 
    while (bonds_alloc > recommended_bonds_alloc):
        security = next(pop)
        while (not client_portfolio.check_security_in_portfolio(client_portfolio.portfolio, security)):
            security = next(pop)
        security_exposure = client_portfolio.portfolio[security]
        if (exposure):
            fit_exposure = min (security_exposure, bonds_alloc - recommended_bonds_alloc)
        else:
            fit_exposure = bonds_alloc - recommended_bonds_alloc
        if (fit_exposure == security_exposure): 
            # delete dictionary entry
            client_portfolio.deteleSecurity(security)
            bonds_alloc -= fit_exposure
        elif (fit_exposure < security_exposure):
            # delete some of the shares
            
            client_portfolio.setExposure(security, fit_exposure)
            bonds_alloc -= fit_exposure        

def addStocksToBalance(security_dict, stocks_alloc, recommended_stock_alloc, recommendations, exposure = True, exposure_threshold = 5):
    pop = recom.recommend_stock(recommendations)      
    while (stocks_alloc < recommended_stock_alloc):
        # get a recommendation
        security = next(pop)
        print ('Checking if stock {} exists in portfolio'.format(security))
        # check if the recommended security is in the portfolio already and get the second best if it is
        while client_portfolio.check_security_in_portfolio(client_portfolio.portfolio, security):
            print ('Stock {} exists in portfolio'.format(security))
            security = next(pop)
            print ('Checking if stock {} exists in portfolio'.format(security))
        # desired exposure
        if (exposure):
            fit_exposure = min(exposure_threshold, (recommended_stock_alloc - stocks_alloc))
        else:
            fit_exposure = recommended_stock_alloc - stocks_alloc
        # add shares to portfolio
        client_portfolio.addNewSecurity(security, fit_exposure)
        # increase bond allocation
        stocks_alloc += fit_exposure

def removeStocksToBalance(security_dict, stocks_alloc, recommended_stock_alloc, recommendations, exposure = True): 
    recommendations = recom.rank_stocks('Mid')  
    pop = recom.reverse_recommend_stock(recommendations) 
    while (stocks_alloc > recommended_stock_alloc):
        security = next(pop)
        while (not client_portfolio.check_security_in_portfolio(client_portfolio.portfolio, security)):
            security = next(pop)
        security_exposure = client_portfolio.portfolio[security]
        if (exposure):
            fit_exposure = min (security_exposure, stocks_alloc - recommended_stock_alloc)
        else:
            fit_exposure = stocks_alloc - recommended_stock_alloc
        if (fit_exposure == security_exposure): 
            # delete dictionary entry
            client_portfolio.deteleSecurity(security)
            stocks_alloc -= fit_exposure
        elif (fit_exposure < security_exposure):
            # delete some of the shares
            client_portfolio.setExposure(security, fit_exposure)
            stocks_alloc -= fit_exposure


# import data
allSecurities = pd.read_hdf('stocks&etfs.hdf5', 'Datataset1/X').set_index('Name').T.to_dict()
data = pd.read_hdf('stocks.hdf5', 'Datataset1/X').drop_duplicates().dropna(axis = 0, how = 'any')
#data = pd.read_excel('../Data/BLB_values_SP1500_22feb.xlsx', 
#                     names = ['Ticker symbol',	'Security', 'Sector', 'Region',
#                              'Raw_beta', 'Adjusted_beta', 'Volatility_30',	 
#                              'Volatility_90', 'Volatility_360', 
#                              'Returns_3_months', 'Returns_6_months', 'Return_last_year',
#                              'Returns_5_years', 'Ethics', 'Bribery', 'Quick_ratio', 
#                              'Inventory_turnover', 'Revenue', 'Gross_profit', 'Net_income', 
#                              'Operational_cash_flow', 'PE', 'EPS', 
#                              'Market_cap', 'Assets', 'ANR']).drop_duplicates().dropna(axis = 0, how = 'any')
investors = pd.read_hdf('clients.hdf5', 'DatatasetCli').set_index('Id')
portfolios = pd.read_hdf('portfolios.hdf5', 'DatatasetPort')

client = investors.iloc[randint(1, 99)]
client_portfolio = ClientPortfolio(portfolios.iloc[client['Portfolio_Id']].tolist(), 
                                   client)
preferences = advisor1([1], data).index.values.tolist()
exposure = False

stocks_alloc, bonds_alloc, recommended_stock_alloc, recommended_bonds_alloc = getAllocations(client_portfolio, allSecurities)

if (bonds_alloc < recommended_bonds_alloc):
    addBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc, preferences, exposure)
if (bonds_alloc > recommended_bonds_alloc):
    removeBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc, preferences, exposure)
if (stocks_alloc < recommended_stock_alloc):   
    addStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc, preferences, exposure)
if (stocks_alloc > recommended_stock_alloc):
    removeStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc, preferences, exposure)
    
    
    
