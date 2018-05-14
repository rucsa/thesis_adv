import pandas as pd
import numpy as np
from random import uniform, choice, randint


sectors_to_add = ['Financial', 'Technology', 'Consumer, Non-cyclical', 
                  'Industrial', 'Consumer, Cyclical', 
                  'Energy', 'Basic Materials',
                  'Utilities', 'Communications']
regions = ['USA', 'Europe ex UK', 'Emerging Markets', 'Japan', 'UK', 'Canada', 'Other', 'Asia ex Japan']

''''Stocks'''
if True:
    stocks = pd.read_hdf('hdfs/SP1500.hdf5', 'Datataset1/X')
    stocks = stocks[['Security', 'Asset', 'Return_last_year', 'Sector', 'Bribery', 'Ethics', 'ANR', 'PE', 'Returns_3_months']]
    
    stocks = stocks.drop_duplicates().dropna(axis = 0, how = 'any')
    
    # add random dividents, prices and regions
    dividents, prices, region = [], [], []
    for row in stocks.itertuples():
        dividents.append(randint(0,1))
        #prices.append(round(uniform(0.5, 150), 2))
        region.append(choice(regions))
        
    stocks['Dividents'] = pd.Series(dividents, index=stocks.index)
    #stocks['Price'] = pd.Series(prices, index=stocks.index)
    stocks['Region'] = pd.Series(region, index=stocks.index)
    stocks = stocks.rename(columns={'Return_last_year': 'Returns2017', 'Security':'Name'})
    stocks.to_hdf('hdfs/stocks.hdf5', 'Datataset1/X')
    
'''ETFs'''
if True:
    etfs = pd.read_excel('data/ETFList.xlsx')
    #etfs = etfs.set_index('Name')
    etfs = etfs[['Name', 'LastSale', 'Asset', '1YrPercentChange']]
    
    # drop rows with unreal prices
    for index, row in etfs.iterrows():
        if row['LastSale']>200:
            etfs = etfs.drop(index)
       
    etfs = etfs.drop(columns = ['LastSale'])
    # add sectors, bribery, ethics and dividents columns for etfs
    bribery, ethics, dividents, sectors, anr, pe, returns3months, region = [], [], [], [], [], [], [], []
    for index, row in etfs.iterrows():
        bribery.append(randint(0,1))
        ethics.append(randint(0,1))
        dividents.append(randint(0,1))
        sectors.append(choice(sectors_to_add))
        anr.append(round(uniform(0, 5), 2))
        pe.append(round(uniform(0, 300), 2))
        returns3months.append(round(uniform(-35, 75), 2))
        region.append(choice(regions))
        
        
    etfs['Bribery'] = pd.Series(bribery, index = etfs.index)
    etfs['Ethics'] = pd.Series(ethics, index = etfs.index)
    etfs['Dividents'] = pd.Series(dividents, index=etfs.index)
    etfs['Sector'] = pd.Series(sectors, index = etfs.index)
    etfs['ANR'] = pd.Series(anr, index=etfs.index)
    etfs['PE'] = pd.Series(pe, index=etfs.index)
    etfs['Returns_3_months'] = pd.Series(returns3months, index=etfs.index)
    etfs['Region'] = pd.Series(region, index = etfs.index)
    
    etfs = etfs.rename(columns={'1YrPercentChange':'Returns2017'})
    etfs.to_hdf('hdfs/ETFs.hdf5', 'Datataset1/X')


'''ETFs & Stocks'''
if True:
    stocks = pd.read_hdf('hdfs/stocks.hdf5', 'Datataset1/X')
    stocks = stocks[['Name', 'Asset', 'Returns2017', 'Sector', 'Bribery', 'Ethics', 'Dividents', 'ANR', 'PE', 'Returns_3_months', 'Region']]
    etfs = pd.read_hdf('hdfs/ETFs.hdf5', 'Datataset1/X')
    
    
    data = pd.concat([stocks, etfs], axis = 0, ignore_index = True)
    
#    # add random returns 2016
#    random_price = []
#    for row in data.itertuples():
#        random_price.append(round(uniform(-60, 120), 4))
#    data.loc[:,'Retruns2016'] = pd.Series(random_price, index=data.index)
#    
#    # add random returns 2015
#    random_price = []
#    for row in data.itertuples():
#        random_price.append(round(uniform(-60, 120), 4))
#    data.loc[:,'Retruns2015'] = pd.Series(random_price, index=data.index)
    
    
    data.to_hdf('hdfs/stocks&etfs.hdf5', 'Datataset1/X')
