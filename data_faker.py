from random import randint
from random import choice
import pandas as pd
import utils as ut
import numpy as np
import math


''''CLIENTS'''
if False:
    columns = ['Id', 'Age', 'Retirement', 'Goal', 'Timeline', 'Risk_profile', 'Capital', 'Portfolio_Id']
    df = pd.DataFrame(columns = columns)
    risk_profiles = ['Defensive', 'Moderate Defensive', 'Balanced', 'Moderate Offensive', 'Offensive']
    
    for i in range (1, 101):
        age = randint(25, 45)
        retirement = randint(55, 68)
        goal = randint(10, 1000) * 100
        #capital = goal - (randint(10, 100) * 100)
        row = pd.DataFrame([[i,                          #client id
                             age,                        #client age
                             retirement,                 #retirement age
                             goal,                       #goal
                             retirement - age,           #timeline
                             choice(risk_profiles),      #risk profile
                             0,  #capital
                             randint(1, 100)]],            #portfolio id
                             columns = columns)          
        df = df.append(row, ignore_index=True)
    df.to_hdf('clients.hdf5', 'DatatasetCli')

''' PORTFOLIOS '''
if True:
    data = pd.read_hdf('stocks&etfs.hdf5', 'Datataset1/X')
        
    columns = ['Shares1', 'Asset1', 'Shares2', 'Asset2', 'Shares3', 'Asset3', 'Shares4', 'Asset4', 'Shares5', 'Asset5',
               'Shares6', 'Asset6', 'Shares7', 'Asset7', 'Shares8', 'Asset8', 'Shares9', 'Asset9', 'Shares10', 'Asset10',
               'Shares11', 'Asset11', 'Shares12', 'Asset12', 'Shares13', 'Asset13', 'Shares14', 'Asset14', 'Shares15', 'Asset15', 
               'Shares16', 'Asset16', 'Shares17', 'Asset17', 'Shares18', 'Asset18', 'Shares19', 'Asset19', 'Shares20', 'Asset20']
    port = []
    for j in range (0, 110):
        shares = ut.constrained_sum_sample_pos(randint(2, 20), 100)
        row = []
        for i in range(0, len(shares)):
            pick = data.iloc[randint(0, 1578)]
            row.append(pick['Name'])
            row.append(shares[i])   
        for i in range (len(shares), 20):
            row.append(str(math.nan))
            row.append(0)
        port.append(row)    
        portfolios = pd.DataFrame(port, columns = columns)
    
    portfolios.to_hdf('portfolios.hdf5', 'DatatasetPort')
       