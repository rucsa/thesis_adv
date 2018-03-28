import scipy as sy
import pandas as pd
import numpy as np
import utils as ut

from sklearn.preprocessing import minmax_scale
data = pd.read_excel('../Data/BLB_values_SP1500_22feb.xlsx', 
                     names = ['Ticker symbol',	'Security', 'Sector', 'Region',
                              'Raw_beta', 'Adjusted_beta', 'Volatility_30',	 
                              'Volatility_90', 'Volatility_360', 
                              'Returns_3_months', 'Returns_6_months', 'Return_last_year',
                              'Returns_5_years', 'Ethics', 'Bribery', 'Quick_ratio', 
                              'Inventory_turnover', 'Revenue', 'Gross_profit', 'Net_income', 
                              'Operational_cash_flow', 'PE', 'EPS', 
                              'Market_cap', 'Assets', 'ANR'])

data = data.dropna()
securities = ut.collect_sectors(data)
economy = 'Mid'
score = {}
description = {}
desc_df = pd.DataFrame()

print('Insert sorting criterion:')
print('\'1\' = sorts by Analyst Rating ')
print('\'2\' = sorts by Returns last 3 months')
print('\'3\' = sorts by PE')
print('\'4\' = filters sectors by Business Cycle \n')
print('Multiple criterions are written as \'1 2 3 4\' ')
user_in = [int(x) for x in input('Sort by.. ').split()]
for val in user_in:
    if (val < 1 & val > 4):
        print ('Inserted value unknown.. Try again.. ')
        user_in = [int(x) for x in input('Sort by.. ').split()]

criterions = []
criterions.append('Security')

if (4 in user_in):
    print('Insert business cycle')
    economy = input('Choose from \'Mid\', \'Late\', \'Recession\', \'Early\'.. ')
    if (economy not in ['Mid', 'Late', 'Recession', 'Early']):
        print ('Inserted value not unknown.. Try again.. ')
        economy = input('Choose from \'Mid\', \'Late\', \'Recession\', \'Early\'.. ')
    
### score anr
if (1 in user_in):
    score = ut.score_feature(data, score, 'ANR')
    criterions.append('ANR')

### score returns last 3 months
if (2 in user_in):
    score = ut.score_feature(data, score, 'Returns_3_months')
    criterions.append('Returns_3_months')
    
### score P/E
if (3 in user_in):
    score = ut.score_feature(data, score, 'PE')
    criterions.append('PE')
    
### score sectors
if (4 in user_in):
    sectors = ut.check_bc(economy)
    score = ut.score_sectors(data, sectors, score)
    criterions.append('Sector')
    
### determine ranking
rank = ut.rank_scores(score)

### make df
reasoning = pd.DataFrame(list(rank.items()), columns=['Company', 'Score'])
reasoning = reasoning.set_index('Company')
desc_df = data[criterions]
desc_df = desc_df.set_index('Security')

ranking = pd.concat([reasoning, desc_df], axis=1)
ranking = ranking.sort_values(by='Score', axis=0, ascending=False)

criterions.remove('Security')
print ('Top 25 companies sorted by {}'.format(criterions))

print (ranking.head(25))