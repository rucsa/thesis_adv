from pyfancy import pyfancy

import pandas as pd
from random import randint, choice

from ClientPortfolio7 import ClientPortfolio

allSecurities = pd.read_hdf('../hdfs/stocks&etfs.hdf5', 'Datataset1/X').set_index('Name').T.to_dict()
allsecurities = pd.read_hdf('../hdfs/stocks&etfs.hdf5', 'Datataset1/X').drop_duplicates().dropna(axis = 0, how = 'any')
stocks = pd.read_hdf('../hdfs/stocks.hdf5', 'Datataset1/X').drop_duplicates().dropna(axis = 0, how = 'any')
bonds = pd.read_hdf('../hdfs/ETFs.hdf5', 'Datataset1/X').drop_duplicates().dropna(axis = 0, how = 'any')

investors = pd.read_hdf('../hdfs/clients.hdf5', 'DatatasetCli').set_index('Id')
portfolios = pd.read_hdf('../hdfs/portfolios.hdf5', 'DatatasetPort')

client_id = 64
client = investors.iloc[client_id]
client_portfolio = ClientPortfolio(portfolios.iloc[client['Portfolio_Id']].tolist(), 
                                   client)
sectors = ['Consumer, Non-cyclical', 'Financial', 'Industrial', 
                  'Energy', 'Basic Materials', 'Technology',
                  'Consumer, Cyclical', 'Utilities', 'Communications']
sectors_list = {}

for sector in sectors:
    portfolio_sector_dict = {}
    for key, value in client_portfolio.portfolio.items():
        current_security = allSecurities[key]
        if current_security['Sector'] == sector:
            portfolio_sector_dict[key] = value
    sectors_list[sector] = portfolio_sector_dict
