import pandas as pd
import numpy as np
from random import uniform


'''ETFs'''
if True:
    etfs = pd.read_excel('data/ETFList.xlsx')
    #etfs = etfs.set_index('Name')
    etfs = etfs[['Name', 'Symbol', 'LastSale', 'Asset', '1YrPercentChange']]
    
    for index, row in etfs.iterrows():
        if row['LastSale']>200:
            etfs = etfs.drop(index)
    etfs = etfs[['Name', 'Symbol', 'Asset', 'LastSale', '1YrPercentChange']]
    etfs.to_hdf('ETFs.hdf5', 'Datataset1/X')

''''Stocks'''
if True:
    stocks = pd.read_hdf('SP1500.hdf5', 'Datataset1/X')
    stocks = stocks[['Security', 'Ticker symbol', 'Asset', 'Return_last_year']]
    stocks.to_hdf('stocks.hdf5', 'Datataset1/X')
    
    
'''ETFs & STocks'''
if True:
    stocks = pd.read_hdf('stocks.hdf5', 'Datataset1/X')
    etfs = pd.read_hdf('ETFs.hdf5', 'Datataset1/X')
    
    # add random prices in stocks 
    random_price = []
    for row in stocks.itertuples():
        random_price.append(round(uniform(0.5, 150), 2))
    stocks.loc[:,'Price'] = pd.Series(random_price, index=stocks.index)
    
    stocks = stocks.rename(columns={'Ticker symbol':'Symbol', 'Return_last_year': '1YReturn', 'Security':'Name'})
    etfs = etfs.rename(columns={'1YrPercentChange':'1YReturn', 'LastSale':'Price'})
    data = pd.concat([stocks, etfs], axis = 0, ignore_index = True)
    data.to_hdf('stocks&etfs.hdf5', 'Datataset1/X')