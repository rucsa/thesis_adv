import scipy as sy
import pandas as pd
import numpy as np
import utils as ut

def rank_stocks(economy):
    data = pd.read_hdf('SP1500.hdf5', 'Datataset1/X')
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