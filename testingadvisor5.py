import time
import pandas as pd
from pyfancy import pyfancy
from random import randint, choice
import utils as ut

from ClientPortfolio4 import ClientPortfolio
from advisor1worker import advisor1, select_preferences
from advisor3worker import advisor3
from advisor5worker import advisor5

import warnings
warnings.filterwarnings("ignore")

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
portfolio_sector_dict = client_portfolio.categorize_stocks_by_sector(allSecurities)