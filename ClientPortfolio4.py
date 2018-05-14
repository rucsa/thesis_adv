from random import randint
import recommender as recom

from pyfancy import pyfancy
from advisor3worker import getAllocations


import time

class ClientPortfolio(object):
    portfolio = {}
    client = {}
    exposures = {}
    extra_exposure = 0 
    
    def __init__(self, security_list, client_series):
        self.portfolio = {}
        self.client = {}
        for i in range(0, len(security_list)-1, 2):
            if security_list[i] != 'nan':
                self.portfolio[security_list[i]] = security_list[i+1]
        self.client = client_series.to_dict()  
        self.extra_exposure = 0
        
    def changeRiskProfile (self, new_profile):
        if (new_profile not in ['Balanced', 'Defensive', 'Moderate Defensive', 'Moderate Offensive', 'Offensive']):
            print ("The risk profile you want to set is unknown")
            return False
        self.client['Risk_profile'] = new_profile
        return True
    
    def setCapital(self, capital):
        self.client['Capital'] = capital
        self.client['Goal'] = capital + randint(15, 30) /100 * capital
       
    def getCapital(self):
        return self.client['Capital']
    
    def setExposure(self, security, new_exposure):
        time.sleep(1)
        pyfancy.pyfancy().bold().yellow("Modified exposure for security {} from {} % to {} % \n".format(security, self.portfolio[security], new_exposure)).output()
        self.extra_exposure = self.extra_exposure + self.portfolio[security] - new_exposure
        self.portfolio[security] = new_exposure
        print ("You now have in CASH : {} % exposure".format(self.extra_exposure))
        
        
    def addNewSecurity(self, security, shares, allSecurities):
        current_security = allSecurities[security]
        security_type = current_security['Asset']
        self.portfolio[security] = shares
        time.sleep(1)
        if security_type == 'Equity':
            pyfancy.pyfancy().bold().yellow("Added to portfolio stock {} with {} exposure \n".format(security, shares)).output()
        elif security_type == 'Bond':
            pyfancy.pyfancy().bold().yellow("Added to portfolio bond {} with {} exposure \n".format(security, shares)).output()    
        self.extra_exposure = self.extra_exposure - shares
        print ("You now have in CASH : {} % exposure".format(self.extra_exposure))
        
    def deleteSecurity(self, security, allSecurities):
        current_security = allSecurities[security]
        security_type = current_security['Asset']
        exposure = self.portfolio.pop(security, None)
        time.sleep(1)
        if security_type == 'Equity':
            pyfancy.pyfancy().bold().yellow("Deleted stock {} that had {} exposure \n".format(security, exposure)).output()
        elif security_type == 'Bond':
            pyfancy.pyfancy().bold().yellow("Deleted bond {} that had {} exposure \n".format(security, exposure)).output()
        self.extra_exposure = self.extra_exposure + exposure
        print ("You now have in CASH : {} % exposure".format(self.extra_exposure))
        
    def deleteSector(self, sector, security_dict):
        pyfancy.pyfancy().cyan("Scanning portfolio to delete securities from sector {}".format(sector)).output()
        time.sleep(1)
        securities_to_del = []
        for key, value in self.portfolio.items():
            current_security = security_dict[key]
            if current_security['Sector'] == sector:
                securities_to_del.append(key)
        for key in securities_to_del:
            self.deleteSecurity(key, security_dict)
        print ('Deleted sector {}'.format(sector))
                
    def current_allocation (self, security_dict):
        stocks, bonds = 0, 0
        for key, exposure in self.portfolio.items():
            current_security = security_dict[key]
            current_security_type = current_security['Asset']
            if (current_security_type == 'Equity'):
                stocks += exposure 
            elif (current_security_type == 'Bond'):
                bonds += exposure 
        return stocks, bonds
    
    def extract_securities_by_type(self, security_dict):
        stocks_held = {}
        stock_exp, bonds_exp = 0, 0
        bonds_held = {}
        for key, value in self.portfolio.items():
            current_security = security_dict[key]
            current_security_type = current_security['Asset']
            if (current_security_type == 'Equity'):
                stocks_held[key] = current_security
                stock_exp += self.portfolio[key]
            elif (current_security_type == 'Bond'):
                bonds_held[key] = current_security
                bonds_exp += self.portfolio[key]
            else: 
                print('Asset type {} unknown'.format(current_security_type))
        print ('You have {} stock(s) ({} exposure) and {} bond(s) ({} exposure)'.format(len(stocks_held), stock_exp, len(bonds_held), bonds_exp))
#        print ('\n Stocks are:')
#        for k, v in stocks_held.items():
#            print(k, v)
#        print ('\n Bonds are:')
#        if (len(bonds_held) == 0):
#            print ('None')
#        else: 
#            for k, v in bonds_held.items():
#                print(k, v)
        
        return stocks_held, bonds_held

    def categorize_stocks_by_sector(self, allSecurities):
        portfolio_sector_dict = {}
        for key, value in self.portfolio.items():
            current_security = allSecurities[key]
            if (current_security['Asset'] == 'Equity'):
                current_security_sector = current_security['Sector']
                if (portfolio_sector_dict.get(current_security_sector, 0) == 0):
                    portfolio_sector_dict[current_security_sector] = value
                else:
                    portfolio_sector_dict[current_security_sector] += value
        for k, v in portfolio_sector_dict.items():
            print(k, v)
        return portfolio_sector_dict
    
    def extract_securities_by_sector(self, sector, allSecurities):
        security_dict_per_sector = {}
        for key, value in self.portfolio.items():
            current_security = allSecurities[key]
            if current_security['Sector'] == sector:
                security_dict_per_sector[key] = value
        return security_dict_per_sector
    
    def sectors_you_should_not_have(self, recom_sect, actual_sect):
        sect_to_delete = []
        for key, value in actual_sect.items():
            if (recom_sect.get(key, 0) == 0):
                print ('\n You should not have {} in your portfolio'.format(key))
                sect_to_delete.append(key)
        return sect_to_delete
    
    def recommended_allocation (self, risk_profile):
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
                
    def addBondsToBalance(self, security_dict, bonds_alloc, recommended_bonds_alloc, exposure = True, exposure_threshold = 5):
        recommendations = recom.rank_etfs()  
        pop = recom.recommend_etf(recommendations)  
        while (bonds_alloc < recommended_bonds_alloc):
            # get a recommendation
            security = next(pop)
            print ('Checking if bond {} exists in portfolio'.format(security))
            # check if the recommended security is in the portfolio already and get the second best if it is
            while self.check_security_in_portfolio(self.portfolio, security):
                print ('Bond {} exists in portfolio'.format(security))
                security = next(pop)
                print ('Checking if bond {} exists in portfolio'.format(security))
            # desired exposure
            if (exposure):
                fit_exposure = min(exposure_threshold, (recommended_bonds_alloc - bonds_alloc))  
            else:
                fit_exposure = recommended_bonds_alloc - bonds_alloc
            # add shares to portfolio
            self.addNewSecurity(security, fit_exposure, security_dict)
            # increase bond allocation
            bonds_alloc += fit_exposure 
            
    def removeBondsToBalance(self, security_dict, bonds_alloc, recommended_bonds_alloc, exposure = True):
        recommendations = recom.rank_etfs()  
        pop = recom.reversed_recommend_etf(recommendations) 
        while (bonds_alloc > recommended_bonds_alloc):
            security = next(pop)
            while (not self.check_security_in_portfolio(self.portfolio, security)):
                security = next(pop)
            security_exposure = self.portfolio[security]
            if (exposure):
                fit_exposure = min (security_exposure, bonds_alloc - recommended_bonds_alloc)
            else:
                fit_exposure = bonds_alloc - recommended_bonds_alloc
            if (fit_exposure <= security_exposure): 
                # delete dictionary entry
                self.deleteSecurity(security, security_dict)
                bonds_alloc -= security_exposure
            elif (fit_exposure < security_exposure):
                # delete some of the shares
                self.setExposure(security, security_exposure - fit_exposure)
                bonds_alloc -= fit_exposure        
    
    def addStocksToBalance(self, security_dict, stocks_alloc, recommended_stock_alloc, recommendations, exposure = True, exposure_threshold = 5):
        pop = recom.recommend_stock(recommendations)      
        while (stocks_alloc < recommended_stock_alloc):
            # get a recommendation
            security = next(pop)
            print ('Checking if stock {} exists in portfolio'.format(security))
            # check if the recommended security is in the portfolio already and get the second best if it is
            while self.check_security_in_portfolio(self.portfolio, security):
                print ('Stock {} exists in portfolio'.format(security))
                security = next(pop)
                print ('Checking if stock {} exists in portfolio'.format(security))
            # desired exposure
            if (exposure):
                fit_exposure = min(exposure_threshold, (recommended_stock_alloc - stocks_alloc))
            else:
                fit_exposure = recommended_stock_alloc - stocks_alloc
            # add shares to portfolio
            self.addNewSecurity(security, fit_exposure, security_dict)
            # increase bond allocation
            stocks_alloc += fit_exposure
    
    def removeStocksToBalance(self, security_dict, stocks_alloc, recommended_stock_alloc, recommendations, exposure = True):   
        pop = recom.reverse_recommend_stock(recommendations) 
        while (stocks_alloc > recommended_stock_alloc):
            security = next(pop)
            while (not self.check_security_in_portfolio(self.portfolio, security)):
                security = next(pop)
            security_exposure = self.portfolio[security]
            if (exposure):
                fit_exposure = min (security_exposure, stocks_alloc - recommended_stock_alloc)
            else:
                fit_exposure = stocks_alloc - recommended_stock_alloc
            if (fit_exposure >= security_exposure): 
                # delete dictionary entry
                self.deleteSecurity(security, security_dict)
                stocks_alloc -= security_exposure
            elif (fit_exposure < security_exposure):
                # delete some of the shares
                self.setExposure(security, security_exposure - fit_exposure)
                stocks_alloc -= fit_exposure
                                 
                
    def check_security_in_portfolio (self, portfolio, security):
        for item in portfolio:
            if item == security:
                return True
        return False
    
    def refine_exposures(self, exposure_threshold = 5):
        for key, exposure in self.portfolio.items():
            if (key != 'nan'):
                if exposure > exposure_threshold:
                    self.setExposure(key, exposure_threshold)
            elif (key == 'nan'):
                break
        return self.extra_exposure
    
    def remove_one_item(self, recommendations, asset_type, allSecurities):
        stocks_alloc, bonds_alloc = self.current_allocation(allSecurities)
        if (asset_type == 'Equity' or asset_type == 'equity' or asset_type == 'stock'):
            if stocks_alloc == 0:
                print ("You have no stocks to delete")
            else:
                pop = recom.reverse_recommend_stock(recommendations) 
                security = next(pop)    
                while not self.check_security_in_portfolio(self.portfolio, security):
                    security = next(pop)
                self.deleteSecurity(security, allSecurities)
                print ("You now have {} % exposure in CASH.".format(self.extra_exposure))
        elif (asset_type == 'Bond' or asset_type == 'bond'):
            if bonds_alloc == 0:
                print ("You have no bonds to delete")
            else:
                recommendations = recom.rank_etfs()  
                pop = recom.reverse_recommend_stock(recommendations)    
                security = next(pop)    
                while not self.check_security_in_portfolio(self.portfolio, security):
                    security = next(pop)
                self.deleteSecurity(security, allSecurities)
                print ("You now have {} % exposure in CASH.".format(self.extra_exposure))
                
    def buy_bonds(self, budget, allSecurities):
        recommendations = recom.rank_etfs()  
        pop = recom.recommend_etf(recommendations)  
        security = next(pop)
        print ('Checking if bond {} exists in portfolio'.format(security))
        while self.check_security_in_portfolio(self.portfolio, security):
            print ('Bond {} exists in portfolio'.format(security))
            security = next(pop)
        self.addNewSecurity(security, budget, allSecurities)   
        
    def buy_stocks(self, budget, preferences, allSecurities):
        pop = recom.recommend_stock(preferences)      
        security = next(pop)
        print ('Checking if stock {} exists in portfolio'.format(security))
        while self.check_security_in_portfolio(self.portfolio, security):
            print ('Stock {} exists in portfolio'.format(security))
            security = next(pop)
        self.addNewSecurity(security, budget, allSecurities)  
        
    def refine_portfolio_to_preferences(self, allSecurities, preferences):
        print ("Checking your cash...")
        if (self.extra_exposure > 0):
            stocks_alloc, bonds_alloc = self.current_allocation(allSecurities)
            recommended_stock_alloc, recommended_bonds_alloc = self.recommended_allocation(self.client['Risk_profile'])
            print ("You have {} % exposure in cash \n".format(self.extra_exposure))
            if (stocks_alloc < recommended_stock_alloc):
                pyfancy.pyfancy().cyan("You don't have as many stocks as recommended, let's buy some \n").output()
                self.addStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc, preferences, True)
            if (bonds_alloc < recommended_bonds_alloc):
                pyfancy.pyfancy().cyan("You don't have as many bonds as recommended, let's buy some \n").output()
                self.addBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc, True)
            