import time
import pandas as pd
from pyfancy import pyfancy
from random import randint, choice
import utils as ut

from ClientPortfolio4 import ClientPortfolio
from advisor1worker import advisor1, select_preferences
from advisor3worker import refine_alloc_with_risk_profile, refine_exposure_to_5
from advisor5worker import advisor5

import warnings
warnings.filterwarnings("ignore")

# import data
allSecurities = pd.read_hdf('stocks&etfs.hdf5', 'Datataset1/X').set_index('Name').T.to_dict()
data = pd.read_hdf('stocks.hdf5', 'Datataset1/X').drop_duplicates().dropna(axis = 0, how = 'any')
#data = pd.read_excel('../Data/BLB_values_SP1500_22feb.xlsx', 
#                     names = ['Ticker symbol',	'Security', 'Sector', 'Region',
#                              'Raw_beta', 'Adjusted_beta', 'Volatility_30',	 
#                              'Volatility_90', 'Volatility_360', 
#                              'Returns_3_months', 'Returns_6_months', 'Return_last_year',
#                              'Returns_5_years', 'Ethics', 'Bribery', 'Quick_ratio', 
#                              'Inventory_turnover', 'Revenue', 'Gross_profit', 'Net_income', 
#                              'Operational_cash_flow', 'PE', 'EPS', 
#                              'Market_cap', 'Assets', 'ANR']).drop_duplicates().dropna(axis = 0, how = 'any')
investors = pd.read_hdf('clients.hdf5', 'DatatasetCli').set_index('Id')
portfolios = pd.read_hdf('portfolios.hdf5', 'DatatasetPort')
client_id = randint(1, 99)
client = investors.iloc[client_id]
client_portfolio = ClientPortfolio(portfolios.iloc[client['Portfolio_Id']].tolist(), 
                                   client)

setTimer = True


print ("Hello!...")
if setTimer:
    time.sleep(1)
    
print ("Welcome to BestAdvisor!")
if setTimer:
    time.sleep(1)
    
print ("I'm Best and I'm going to help you invest your money wisely ...")
if setTimer:
    time.sleep(1)
    
print ("And you are...?")
pyfancy.pyfancy().cyan("Randomly generating investor...").output()
if setTimer:
    time.sleep(1)
    
print ("{}! Nice to meet you!".format(client["Name"]))
print ("Client ID: {}".format(client_id))
if setTimer:
    time.sleep(1)
    
print ("I see that you are {} years old..".format(client["Age"]))
if setTimer:
    time.sleep(1)
    
print ("... you want to retire at {} and your goal is to have {} euros by then".format(client["Retirement"], client["Goal"])) 
if setTimer:
    time.sleep(1)
    
print ("... your initial capital is {} and your risk profile is {}".format(client["Capital"], client["Risk_profile"]))
if setTimer:
    time.sleep(1)
    
print ("... so we have {} years to gain {} euros".format(client["Timeline"], client["Goal"] - client["Capital"]))
if setTimer:
    time.sleep(2)
    
print ("How nice! Now let's see what you have gathered in your investement portfolio...")
pyfancy.pyfancy().cyan("Randomly generating investment portfolio...").output()
if setTimer:
    time.sleep(2)
    
pyfancy.pyfancy().cyan("Portfolio successfully generated").output()
if setTimer:
    time.sleep(1)
    
stocks_held, bonds_held = client_portfolio.extract_securities_by_type(allSecurities)

pyfancy.pyfancy().cyan("Generating random economy...").output()
economy = choice(['Mid', 'Late', 'Recession', 'Early'])
if setTimer:
    time.sleep(1)
print ('We are using cycle {} for economy'.format(economy))

options = [0, 1, 2, 3, 4]
compliments = ["Briliant!", "Well done!", "Excellent!", "Magnificent!", "You're investements are growing!"]
user_in = 'start'
preferences = advisor1([1], data, economy, False).index.values.tolist()
preferences_default = True

while (user_in != 'exit'):
    print ("\n")
    print (choice(compliments))
    print ("What would you like to do next?..\n")
    print ("1 -  Visualize portfolio")
    print ("2 -  Visualize client")
    print ("3 -  Set / reset stock preferences")
    print ("4 -  Refine allocation according to risk profile")
    print ("5 -  Refine sector allocation for stocks according to business cycle")
    print ("6 -  Refine exposure to max 5% per security")
    print ("7 -  Generate another portfolio")
    print ("8 -  Change economy")
    print ("9 -  Change risk profile")
    print ("10 -  Delete 1 stock")
    print ("11 - Delete 1 bond")
    print ("12 - Add 1 stock")
    print ("13 - Add 1 bond")
    print ("14 - Refine portfolio according to preferences")
    print ("0 - Exit")
    
    user_in = [int(x) for x in input('Insert your options.. ').split()]
    for val in user_in:
        if (val < 0 or val > 14):
            print ('Inserted value unknown.. Try again.. ')
            user_in = [int(x) for x in input('Insert your options.. ').split()]

    if (0 in user_in):
        user_in = 'exit'
        pyfancy.pyfancy().bold().cyan("GOODBYE!").output()
        break
    
    if (1 in user_in):
        print ("ASSET TYPE ..... SECTOR ..... SECURITY ..... EXPOSURE ..... \n")
        for k, v in client_portfolio.portfolio.items():
            current_security = allSecurities[k]
            if current_security['Asset'] == 'Equity':
                print ("{} .. {} ..... {} .. {} %".format(current_security['Asset'], current_security['Sector'], k, v))
        for k, v in client_portfolio.portfolio.items():
            current_security = allSecurities[k]
            if current_security['Asset'] == 'Bond':
                print ("{} .. {} ..... {} .. {} %".format(current_security['Asset'], current_security['Sector'], k, v))
        print ("{} ..... {} %".format('CASH', client_portfolio.extra_exposure))
        
    if (2 in user_in):
        pyfancy.pyfancy().cyan("Current client: \n").output()
        for k,v in client_portfolio.client.items():
            print ('{} ..... {}'.format(k,v))
    
    if (3 in user_in):
        u_in = select_preferences()
        preferences_default = False
        preferences = advisor1(u_in, data, economy).index.values.tolist()
        
    if (4 in user_in):
        # Refine allocation according to risk profile
        if (preferences_default):
            pyfancy.pyfancy().cyan("You have not set your preferences. Using defaults...\n").output()
        else:
            pyfancy.pyfancy().cyan("Using preferences set earlier...\n").output()
        if setTimer:
            time.sleep(2)
        portfolio = refine_alloc_with_risk_profile(client_portfolio, allSecurities, preferences, economy)
        
    if (5 in user_in):
        advisor5(client_portfolio, allSecurities, economy)
    
    if (6 in user_in):
        pyfancy.pyfancy().cyan("Refining exposure to max 5% per security...").output()
        portfolio = refine_exposure_to_5(client_portfolio, allSecurities)
        
    if (7 in user_in):
        pyfancy.pyfancy().cyan("Randomly generating investment portfolio...").output()
        if setTimer:
            time.sleep(1.5)
        client = investors.iloc[randint(1, 99)]
        client_portfolio = ClientPortfolio(portfolios.iloc[client['Portfolio_Id']].tolist(), 
                                   client)
        stocks_held, bonds_held = client_portfolio.extract_securities_by_type(allSecurities)
        
    if (8 in user_in):
        print('Insert business cycle')
        economy = input('Choose from \'Mid\', \'Late\', \'Recession\', \'Early\'.. ')
        if (economy not in ['Mid', 'Late', 'Recession', 'Early']):
            print ('Inserted value not unknown.. Try again.. ')
            economy = input('Choose from \'Mid\', \'Late\', \'Recession\', \'Early\'.. ')
        pyfancy.pyfancy().cyan("Economy changed to {} \n".format(economy)).output()
            
    if (9 in user_in):
        print('Insert new risk profile')
        profile = input('Choose from \'Defensive\', \'Moderate Defensive\', \'Balanced\', \'Moderate Offensive\', \'Offensive\'.. ')
        if (profile not in ['Balanced', 'Defensive', 'Moderate Defensive', 'Moderate Offensive', 'Offensive']):
            print ('Inserted value not unknown.. Try again.. ')
            profile = input('Choose from \'Defensive\', \'Moderate Defensive\', \'Balanced\', \'Moderate Offensive\', \'Offensive\'.. ')
        changed = client_portfolio.changeRiskProfile(profile) 
        if (changed):
            pyfancy.pyfancy().cyan("Risk_profile changed to {} \n".format(client_portfolio.client["Risk_profile"])).output()
        
    if (10 in user_in):
        client_portfolio.remove_one_item(preferences, 'Equity', allSecurities)
        
    if (11 in user_in):
        client_portfolio.remove_one_item(preferences, 'Bond', allSecurities)
    
    if (12 in user_in):
        if (client_portfolio.extra_exposure == 0):
            print('You have no exposure in cash. Delete some items to get cash')
        else:
            client_portfolio.buy_stocks(min(5, client_portfolio.extra_exposure), preferences, allSecurities)
    
    if (13 in user_in):
        if (client_portfolio.extra_exposure == 0):
            print('You have no exposure in cash. Delete some items to get cash')
        else:
            client_portfolio.buy_bonds(min(5, client_portfolio.extra_exposure), allSecurities)
        
    if (14 in user_in):
        if (client_portfolio.extra_exposure == 0):
            print('You have no exposure in cash. Delete some items to get cash')
        else:
            client_portfolio.refine_portfolio_to_preferences(allSecurities, preferences)