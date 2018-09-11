import operator
import pandas as pd
import random
import math

from collections import OrderedDict

def scaleOutMarketCap (df, features):
    for feature in features:
        df.loc[:,feature] = df.loc[:,feature]/df.loc[:,'Market_cap'] * 10000
    return df

def encode_sector (df):
    sector = df ['Sector']
    encoding = []
    for index, row in sector.iteritems():
        if (row == 'Technology'):
            tup = (index, 1)
            encoding.append(tup)
        if (row == 'Industrial'):
            encoding.append((index, 2))
        if (row == 'Communications'):
            encoding.append((index, 3))
        if (row == 'Financial'):
            encoding.append((index, 4))
        if (row == 'Basic Materials'):
            encoding.append((index, 5))
        if (row == 'Consumer, Non-cyclical'):
            encoding.append((index, 6))
        if (row == 'Consumer, Cyclical'):
            encoding.append((index, 7))
        if (row == 'Utilities'):
            encoding.append((index, 8))
        if (row == 'Energy'):
            encoding.append((index, 9))
    encoding = pd.DataFrame(encoding, columns=['Security', 'Sector'])
    encoding = encoding.set_index('Security')
    return encoding

def encode_binary (df):
    bribery = df['Bribery']
    ethics = df['Ethics']
    bribery_l = []
    for index, row in bribery.iteritems():
        if (row == 'N'):
            bribery_l.append((index, 0))
        if (row == 'Y'):
            bribery_l.append((index, 1))
    ethics_l = []
    for index, row in ethics.iteritems():
        if (row == 'N'):
            ethics_l.append((index, 0))
        if (row == 'Y'):
            ethics_l.append((index, 1))
    bribery_l = pd.DataFrame(bribery_l, columns=['Security', 'Bribery'])
    bribery_l = bribery_l.set_index('Security')
    ethics_l = pd.DataFrame(ethics_l, columns=['Security', 'Ethics'])
    ethics_l = ethics_l.set_index('Security')
    
    return bribery_l, ethics_l

def encodeMarketCap(df):
    size = df['Market_cap'] * 1000000
    encoded_size = []
    for index, row in size.iteritems():
        if (10000000000 <= row ):
            encoded_size.append((index, 4)) #'large cap'
        elif (2000000000 <= row and row < 10000000000):
            encoded_size.append((index, 3)) #'mid cap'
        elif (300000000 <= row and row < 2000000000):
             encoded_size.append((index, 2)) #'small cap'
        elif (50000000 <= row and row < 300000000):
             encoded_size.append((index, 1)) #'micro cap'
        elif (row < 50000000):
            encoded_size.append((index, 0))  #'nano cap'
        else: 
            encoded_size.append((index, math.nan))
    encoded_size = pd.DataFrame(encoded_size, columns=['Security', 'Size'])
    encoded_size = encoded_size.set_index('Security')
    return encoded_size

def normalize_value(value, minimum, maximum, x = 1, y = 100):
    return ((value-minimum) / (maximum-minimum)) * (y - x) + x

def collect_sectors(securities):
    sectors = {}
    for row in securities.itertuples():
        s = getattr(row, "Sector")
        n = getattr(row, "Security")
        if s in sectors:
            sectors[s].append(n)
        else:
            sectors[s] = []
            sectors[s].append(n)
    return sectors
    

def check_bc(economy):
    if (economy == 'Mid'):
        return ['Technology', 'Communications', 'Consumer, Non-cyclical']
    elif (economy == 'Late'):
        return ['Financial',  'Energy', 'Basic Materials']
    elif (economy == 'Recession'):
        return ['Utilities',  'Consumer, Cyclical']
    elif (economy == 'Early'):
        return ['Industrial']
    
    
def score_sectors(df, criterion, score):
    if (type(criterion)==list):
        for row in df.itertuples():
             s = getattr(row, "Sector")
             n = getattr(row, "Name") 
             if n not in score:
                 score[n] = []
             if s in criterion:
                 score[n].append(100)
             else:
                 score[n].append(0)
    return score


def score_feature(df, score, feature):
    col = df[feature].values.flatten()
    minimum = min(col)
    maximum = max(col)
    for row in df.itertuples():
        n = getattr(row, "Name") 
        a = getattr(row, feature) 
        if n not in score:
            score[n] = []
        score[n].append(normalize_value(a, minimum, maximum))
    return score


def rank_scores(d):
    rank = {}
    for key, value in d.items():
        rank[key] = sum(value)
    return rank
    
def sort_scores(rank):
    return sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
      
def recommended_allocation (risk_profile):
    alloc = {}
    if (risk_profile == 'Defensive'):
        alloc['Stocks'] = 10
    elif (risk_profile == 'Moderate Defensive'):
        alloc['Stocks'] = 25
    elif (risk_profile == 'Balanced'):
        alloc['Stocks'] = 40
    elif (risk_profile == 'Moderate Offensive'):
        alloc['Stocks'] = 60
    elif (risk_profile == 'Offensive'):
        alloc['Stocks'] = 75
    else:
        print ('Risk profile not found, set to default 50-50')
        alloc['Stocks'] = 50
    alloc['Bonds'] = 100 - alloc['Stocks']
    return alloc['Stocks'], alloc['Bonds']

def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""
    dividers = sorted(random.sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

def check_security_in_portfolio (portfolio, security):
    for item in portfolio:
        if item == security:
            return True
    return False

def calculate_portfolio_value (portfolio_dict, security_dict):
    exposure_dict = {}
    for name, shares in portfolio_dict.items():
        current_security = security_dict.get(name)
        price = current_security.get('Price')
        exposure_dict[name] = shares * price
    return sum(exposure_dict.values())


def current_allocation (security_dict, portfolio_dict, capital):
    exposure_dict = {}
    for name, shares in portfolio_dict.items():
        current_security = security_dict[name]
        price = current_security['Price']
        exposure = shares * price / capital
        exposure_dict[name] = exposure
    stocks, bonds = 0, 0
    for key, exposure in exposure_dict.items():
        current_security = security_dict[key]
        current_security_type = current_security['Asset']
        if (current_security_type == 'Equity'):
            stocks += exposure * 100
        elif (current_security_type == 'Bond'):
            bonds += exposure * 100 
    return stocks, bonds

def check_portfolio_exposure (portfolio_dict, security_dict, capital):
    exposure_dict = {}
    for name, shares in portfolio_dict.items():
        current_security = dict(security_dict[name])
        price = current_security['Price']
        exposure = shares * price / capital
        exposure_dict[name] = exposure
    return exposure_dict
    
           
def check_portfolio_alloc (exposure_dict, security_dict):
    stocks, bonds = 0, 0
    for key, exposure in exposure_dict.items():
        current_security = security_dict[key]
        current_security_type = current_security['Asset']
        if (current_security_type == 'Equity'):
            stocks += exposure * 100
        elif (current_security_type == 'Bond'):
            bonds += exposure * 100
    return stocks, bonds

def sort_dict(unsorted_dict):
    sorted_list=sorted(unsorted_dict.items(), key=lambda x: x[1])
    return OrderedDict(sorted_list)