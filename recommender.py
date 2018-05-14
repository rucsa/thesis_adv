import scipy as sy
import pandas as pd
import numpy as np
import utils as ut
import time
from pyfancy import pyfancy

def rank_stocks(economy):
    data = pd.read_hdf('stocks.hdf5', 'Datataset1/X')
    data = data.dropna()
    scor = {}
    rank = {}
    scor = ut.score_feature(data, scor, 'ANR')
    scor = ut.score_feature(data, scor, 'Returns_3_months')
    scor = ut.score_feature(data, scor, 'PE')
    sectors = ut.check_bc(economy)
    scor = ut.score_sectors(data, sectors, scor)
    rank = ut.rank_scores(scor)
    rank = pd.DataFrame(list(rank.items()), columns = ['Name', 'Score'])
    rank = rank.sort_values(by='Score', axis=0, ascending=False)
    securities = rank['Name'].values.tolist()
    return securities

def rank_stocks_without_bc(sector = 'all'):
    data = pd.read_hdf('stocks.hdf5', 'Datataset1/X')
    data = data.dropna()
    data = pd.DataFrame(data)
    if (sector != 'all'):
        data = data[(data['Sector'] == sector)]
    scor = {}
    rank = {}
    scor = ut.score_feature(data, scor, 'ANR')
    scor = ut.score_feature(data, scor, 'Returns_3_months')
    scor = ut.score_feature(data, scor, 'PE')
    rank = ut.rank_scores(scor)
    rank = pd.DataFrame(list(rank.items()), columns = ['Name', 'Score'])
    rank = rank.sort_values(by='Score', axis=0, ascending=False)
    securities = rank['Name'].values.tolist()
    return securities

def recommend_stock (list_):
    yield from list_
    
def reverse_recommend_stock (list_):
    list_ = list(reversed(list_))
    yield from list_
    
def rank_etfs():
    etfs = pd.read_hdf('ETFs.hdf5', 'Datataset1/X')
    etfs = etfs[['Name', '1YrPercentChange']]
    etfs = etfs.sort_values(by='1YrPercentChange', ascending = False)
    etfs = etfs['Name'].values.tolist()
    return etfs

def recommend_etf (list_):
    yield from list_
    
def reversed_recommend_etf (list_):
    list_ = list(reversed(list_))
    yield from list_
    
def recomm_sector_allocation (portfolio_dict, divers_percent, divers_sectors, sum_stocks):
    # assert len(divers_percent) == len(divers_sectors)
    part_list = []
    for j in range(0, min(len(portfolio_dict), len(divers_percent))):
        part_list.append(divers_percent[j]) 
    total_part = sum(part_list)
    percent_list = []
    for j in range(0, len(part_list)):
        percent_list.append(part_list[j]*sum_stocks/total_part)
    recomm_sector_dict = {}
    for i in range(0, len(percent_list)):
        recomm_sector_dict[divers_sectors[i]] = percent_list[i]
    for k, v in recomm_sector_dict.items():
        print("{}      {} %".format(k, v))
    return recomm_sector_dict


def bc_sector_allocation(economy):
    if economy == 'Mid':
        return ['Consumer, Non-cyclical', 'Technology', 'Financial',
                  'Industrial', 'Consumer, Cyclical', 
                  'Energy', 'Communications', 'Basic Materials',
                  'Utilities'], \
                [24.02, 18.1, 16.8, 14.73, 9.04, 6.32, 5.25, 2.97, 2.77]
    elif economy == 'Late':
        return ['Consumer, Non-cyclical', 'Financial', 'Industrial', 
                  'Energy', 'Basic Materials', 'Technology',
                  'Consumer, Cyclical', 'Utilities', 'Communications'], \
                [24.02, 18.1, 16.8, 14.73, 9.04, 6.32, 5.25, 2.97, 2.77]
    elif economy == 'Recession':
        return ['Consumer, Non-cyclical', 'Financial', 'Consumer, Cyclical', 
                  'Utilities', 'Communications', 'Energy', 
                   'Technology', 'Industrial', 'Basic Materials'], \
                [24.02, 18.1, 16.8, 14.73, 9.04, 6.32, 5.25, 2.97, 2.77]
    elif economy == 'Early':
        return ['Technology', 'Industrial', 'Financial', 
                   'Consumer, Cyclical', 'Consumer, Non-cyclical', 
                  'Basic Materials', 'Energy', 'Utilities', 'Communications'], \
                [24.02, 18.1, 16.8, 14.73, 9.04, 6.32, 5.25, 2.97, 2.77]
    else:
        print ('Incorrect parameter for economy')


def normalize_value(value, minimum, maximum, x = 1, y = 100):
    return ((value-minimum) / (maximum-minimum)) * (y - x) + x

def balance_allocation (client_portfolio, allSecurities, bonds_alloc, stocks_alloc, recommended_bonds_alloc, recommended_stock_alloc, preferences, economy, exposure):
    if (bonds_alloc < recommended_bonds_alloc):
        # add more bonds
        pyfancy.pyfancy().cyan("Not enough bonds. Current bond allocation: {}%. Recommended allocation for {} profile: {}%. Need to add {}% bonds exposure... \n".format(bonds_alloc, client_portfolio.client['Risk_profile'], recommended_bonds_alloc, recommended_bonds_alloc-bonds_alloc)).output()
        time.sleep(2)
        client_portfolio.addBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc, exposure)
        stocks_alloc, bonds_alloc = client_portfolio.current_allocation(allSecurities)   
        time.sleep(1)
        pyfancy.pyfancy().cyan("Modified allocation to: {}% stocks and {}% bonds \n".format(stocks_alloc, bonds_alloc)).output()
            
    if (bonds_alloc > recommended_bonds_alloc):
        # remove from bonds
        pyfancy.pyfancy().cyan("Too many bonds. Current bond allocation: {}%. Recommended allocation for {} profile: {}%. Need to remove {}% bonds exposure... \n".format(bonds_alloc, client_portfolio.client['Risk_profile'], recommended_bonds_alloc, bonds_alloc-recommended_bonds_alloc)).output()
        time.sleep(2)
        client_portfolio.removeBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc, exposure)
        stocks_alloc, bonds_alloc = client_portfolio.current_allocation(allSecurities) 
        time.sleep(1)
        pyfancy.pyfancy().cyan("Modified allocation to: {}% stocks and {}% bonds".format(stocks_alloc, bonds_alloc)).output()

        
    if (stocks_alloc < recommended_stock_alloc):
        # add more stocks 
        pyfancy.pyfancy().cyan("Not enough stocks. Current stock allocation: {}%. Recommended allocation for {} profile: {}%. Need to add {}% stocks exposure... \n".format(stocks_alloc, client_portfolio.client['Risk_profile'], recommended_stock_alloc, recommended_stock_alloc-stocks_alloc)).output()
        time.sleep(2)
        client_portfolio.addStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc, preferences, exposure)
        stocks_alloc, bonds_alloc = client_portfolio.current_allocation(allSecurities)
        time.sleep(1)
        pyfancy.pyfancy().cyan("Modified allocation to: {}% stocks and {}% bonds".format(stocks_alloc, bonds_alloc)).output()
        
    if (stocks_alloc > recommended_stock_alloc):
        # remove from stocks 
        pyfancy.pyfancy().cyan("Too many stocks. Current stock allocation: {}%. Recommended allocation for {} profile: {}%. Need to remove {}% stock exposure... \n".format(stocks_alloc, client_portfolio.client['Risk_profile'], recommended_stock_alloc, stocks_alloc-recommended_stock_alloc)).output()
        time.sleep(2)
        client_portfolio.removeStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc, preferences, exposure)
        stocks_alloc, bonds_alloc = client_portfolio.current_allocation(allSecurities)
        time.sleep(1)
        pyfancy.pyfancy().cyan("Modified allocation to: {}% stocks and {}% bonds".format(stocks_alloc, bonds_alloc)).output()


    