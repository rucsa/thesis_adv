from pyfancy import pyfancy
import pandas as pd


def rank_etfs():
    etfs = pd.read_hdf('ETFs.hdf5', 'Datataset1/X')
    etfs = etfs[['Name', '1YrPercentChange']]
    etfs = etfs.sort_values(by='1YrPercentChange', ascending = False)
    etfs = etfs['Name'].values.tolist()
    return etfs

def recommend_stock (list_):
    yield from list_
    
def reverse_recommend_stock (list_):
    list_ = list(reversed(list_))
    yield from list_

def recommend_etf (list_):
    yield from list_
    
def reversed_recommend_etf (list_):
    list_ = list(reversed(list_))
    yield from list_
    

def bc_sector_allocation(economy):
    if economy == 'Mid':
        return ['Consumer, Non-cyclical', 'Technology', 'Financial',
                  'Industrial', 'Consumer, Cyclical', 
                  'Energy', 'Communications', 'Basic Materials',
                  'Utilities'], \
                [24, 18, 17, 15, 9, 6, 5, 3, 3]
    elif economy == 'Late':
        return ['Consumer, Non-cyclical', 'Financial', 'Industrial', 
                  'Energy', 'Basic Materials', 'Technology',
                  'Consumer, Cyclical', 'Utilities', 'Communications'], \
                [24, 18, 17, 15, 9, 6, 5, 3, 3]
    elif economy == 'Recession':
        return ['Consumer, Non-cyclical', 'Financial', 'Consumer, Cyclical', 
                  'Utilities', 'Communications', 'Energy', 
                   'Technology', 'Industrial', 'Basic Materials'], \
                [24, 18, 17, 15, 9, 6, 5, 3, 3]
    elif economy == 'Early':
        return ['Technology', 'Industrial', 'Financial', 
                   'Consumer, Cyclical', 'Consumer, Non-cyclical', 
                  'Basic Materials', 'Energy', 'Utilities', 'Communications'], \
                [24, 18, 17, 15, 9, 6, 5, 3, 3]
    else:
        print ('Incorrect parameter for economy')
        
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

def recommend_asset_type(portfolio, allSecurities):
    stocks_alloc, bonds_alloc = portfolio.current_asset_allocation(allSecurities)
    recommended_stock_alloc, recommended_bonds_alloc = portfolio.recommended_asset_allocation(portfolio.client['Risk_profile'])
    which_type = []
    if (stocks_alloc < recommended_stock_alloc):
        which_type.append('Equity')
        which_type.append(recommended_stock_alloc - stocks_alloc)
    if (bonds_alloc < recommended_bonds_alloc):
        which_type.append('Bond')
        which_type.append(recommended_bonds_alloc - bonds_alloc)
    return which_type