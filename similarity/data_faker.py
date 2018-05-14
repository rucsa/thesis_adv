from random import randint
from random import choice
import pandas as pd
import utils as ut
import numpy as np
import math

import names


''''CLIENTS'''
if True:
    columns = ['Id', 'Name', 'Age', 'Retirement', 'Goal', 'Timeline', 'Risk_profile', 'Capital', 'Portfolio_Id']
    df = pd.DataFrame(columns = columns)
    risk_profiles = ['Defensive', 'Moderate Defensive', 'Balanced', 'Moderate Offensive', 'Offensive']
    
    for i in range (1, 101):
        age = randint(25, 45)
        retirement = randint(55, 68)
        goal = randint(100, 1000) * 100
        capital = goal - (randint(10, 100) * 100)
        row = pd.DataFrame([[i,                          #client id
                             names.get_first_name(),
                             age,                        #client age
                             retirement,                 #retirement age
                             goal,                       #goal
                             retirement - age,           #timeline
                             choice(risk_profiles),      #risk profile
                             capital,                    #capital
                             randint(1, 100)]],          #portfolio id
                             columns = columns)          
        df = df.append(row, ignore_index=True)
    df.to_hdf('clients-sim.hdf5', 'DatatasetCli')

''' PORTFOLIOS '''
if True:
    data = pd.read_hdf('processed_similarity.hdf5', 'Datataset1/X')
        
    columns = ['Asset1', 'Exposure1', 'Asset2', 'Exposure2', 'Asset3', 'Exposure3', 'Asset4', 'Exposure4', 'Asset5', 'Exposure5', 
               'Asset6', 'Exposure6', 'Asset7', 'Exposure7', 'Asset8', 'Exposure8', 'Asset9', 'Exposure9', 'Asset10', 'Exposure10', 
               'Asset11', 'Exposure11', 'Asset12', 'Exposure12', 'Asset13', 'Exposure13', 'Asset14', 'Exposure14', 'Asset15', 'Exposure15', 
               'Asset16', 'Exposure16', 'Asset17', 'Exposure17', 'Asset18', 'Exposure18', 'Asset19', 'Exposure19', 'Asset20', 'Exposure20']
    port = []
    for j in range (0, 110):
        shares = ut.constrained_sum_sample_pos(randint(2, 20), 100)
        row = []
        for i in range(0, len(shares)):
            pick = data.iloc[randint(0, 1419)]
            row.append(pick.name)
            row.append(shares[i])   
        for i in range (len(shares), 20):
            row.append(str(math.nan))
            row.append(0)
        port.append(row)    
        portfolios = pd.DataFrame(port, columns = columns)
    
    portfolios.to_hdf('portfolios-sim.hdf5', 'DatatasetPort')
       