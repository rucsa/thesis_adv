from random import randint
import recommender as recom
from pyfancy import pyfancy

import time

class ClientPortfolio(object):
    portfolio = {}
    client = {}
    exposures = {}
    cash = 0
    
    def __init__(self, security_list, client_series):
        self.portfolio = {}
        self.client = {}
        for i in range(0, len(security_list)-1, 2):
            if security_list[i] != 'nan':
                self.portfolio[security_list[i]] = security_list[i+1]
        self.client = client_series.to_dict()  
        self.cash = 0
        
    def pretty_print_portfolio(self, allSecurities):
        
        print ("SECTOR .. REGION .. SECURITY ..... EXPOSURE")
        for k, v in self.portfolio.items():
            current_security = allSecurities[k]
            print ("{} .. {} ..... {} .. {} %".format(current_security['Sector'], current_security['Region'], k, v))
            
        
    def pretty_print_client(self):
        for k,v in self.client.items():
            print ('{} ..... {}'.format(k,v))
            
    def getAssetType(self, security, allSecurities):
        current_security = allSecurities[security]
        return current_security['Asset']
           
    # allSecurities should be dict
    def addNewSecurity(self, security, shares, allSecurities):
        self.portfolio[security] = shares
        
#        security_type = allSecurities[security]['Asset']
#        if security_type == 'Equity':
#            pyfancy.pyfancy().bold().yellow("Added to portfolio stock {} with {} exposure \n".format(security, shares)).output()
#        elif security_type == 'Bond':
#            pyfancy.pyfancy().bold().yellow("Added to portfolio bond {} with {} exposure \n".format(security, shares)).output()    
#        self.cash = self.cash - shares
#        print ("You now have in CASH : {} % exposure".format(self.cash))
        return self.portfolio
        
    def deleteSecurity(self, security, allSecurities):
        current_security = allSecurities[security]
        security_type = current_security['Asset']
        exposure = self.portfolio.pop(security, None)
        time.sleep(1)
        if security_type == 'Equity':
            pyfancy.pyfancy().bold().yellow("Deleted stock {} that had {} exposure \n".format(security, exposure)).output()
        elif security_type == 'Bond':
            pyfancy.pyfancy().bold().yellow("Deleted bond {} that had {} exposure \n".format(security, exposure)).output()
        self.cash = self.cash + exposure
        print ("You now have in CASH : {} % exposure".format(self.cash))
        return self.portfolio
        
    def setExposure(self, security, new_exposure):
        time.sleep(1)
        pyfancy.pyfancy().bold().yellow("Modified exposure for security {} from {} % to {} % \n".format(security, self.portfolio[security], new_exposure)).output()
        self.cash = self.cash + self.portfolio[security] - new_exposure
        self.portfolio[security] = new_exposure
        print ("You now have in CASH : {} % exposure".format(self.cash))
        return self.portfolio[security]
        
    def current_asset_allocation (self, security_dict):
        stocks, bonds = 0, 0
        for key, exposure in self.portfolio.items():
            current_security = security_dict[key]
            current_security_type = current_security['Asset']
            if (current_security_type == 'Equity'):
                stocks += exposure 
            elif (current_security_type == 'Bond'):
                bonds += exposure 
        return stocks, bonds
    
    def recommended_asset_allocation (self, risk_profile):
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
    
    def security_exists_in_portfolio (self, portfolio, security):
        for item in portfolio:
            if item == security:
                return True
        return False
    
    def addBondsToBalance(self, security_dict, bonds_alloc, recommended_bonds_alloc, bonds_preferences, exposure = True, exposure_threshold = 5):
        pop = recom.recommend_etf(bonds_preferences)  
        while (bonds_alloc < recommended_bonds_alloc):
            security = next(pop)
            print ('Checking if bond {} exists in portfolio'.format(security))
            while self.security_exists_in_portfolio(self.portfolio, security):
                print ('Bond {} exists in portfolio'.format(security))
                security = next(pop)
                print ('Checking if bond {} exists in portfolio'.format(security))
            if (exposure):
                fit_exposure = min(exposure_threshold, (recommended_bonds_alloc - bonds_alloc))  
            else:
                fit_exposure = recommended_bonds_alloc - bonds_alloc
            self.addNewSecurity(security, fit_exposure, security_dict)
            bonds_alloc += fit_exposure 
            
    def removeBondsToBalance(self, security_dict, bonds_alloc, recommended_bonds_alloc, bonds_preferences, exposure = True):
        pop = recom.reversed_recommend_etf(bonds_preferences) 
        while (bonds_alloc > recommended_bonds_alloc):
            security = next(pop)
            while (not self.security_exists_in_portfolio(self.portfolio, security)):
                security = next(pop)
            security_exposure = self.portfolio[security]
            fit_exposure = min (security_exposure, bonds_alloc - recommended_bonds_alloc)
            if (fit_exposure <= security_exposure): 
                self.deleteSecurity(security, security_dict)
                bonds_alloc -= security_exposure
            elif (fit_exposure < security_exposure):
                self.setExposure(security, security_exposure - fit_exposure)
                bonds_alloc -= fit_exposure        
    
    def addStocksToBalance(self, security_dict, stocks_alloc, recommended_stock_alloc, recommendations, exposure = True, exposure_threshold = 5):
        pop = recom.recommend_stock(recommendations)      
        while (stocks_alloc < recommended_stock_alloc):
            security = next(pop)
            print ('Checking if stock {} exists in portfolio'.format(security))
            while self.security_exists_in_portfolio(self.portfolio, security):
                print ('Stock {} exists in portfolio'.format(security))
                security = next(pop)
                print ('Checking if stock {} exists in portfolio'.format(security))
            if (exposure):
                fit_exposure = min(exposure_threshold, (recommended_stock_alloc - stocks_alloc))
            else:
                fit_exposure = recommended_stock_alloc - stocks_alloc
            self.addNewSecurity(security, fit_exposure, security_dict)
            stocks_alloc += fit_exposure
    
    def removeStocksToBalance(self, security_dict, stocks_alloc, recommended_stock_alloc, recommendations, exposure = True):   
        pop = recom.reverse_recommend_stock(recommendations) 
        while (stocks_alloc > recommended_stock_alloc):
            security = next(pop)
            while (not self.security_exists_in_portfolio(self.portfolio, security)):
                security = next(pop)
            security_exposure = self.portfolio[security]
            fit_exposure = min (security_exposure, stocks_alloc - recommended_stock_alloc)
            if (fit_exposure >= security_exposure): 
                # delete dictionary entry
                self.deleteSecurity(security, security_dict)
                stocks_alloc -= security_exposure
            elif (fit_exposure < security_exposure):
                # delete some of the shares
                self.setExposure(security, security_exposure - fit_exposure)
                stocks_alloc -= fit_exposure
                
    def extract_securities_by_criterion(self, sector, allSecurities, criterion = 'Sector'):
        try:
            portfolio_sector_dict = {}
            for key, value in self.portfolio.items():
                current_security = allSecurities[key]
                if current_security[criterion] == sector:
                    portfolio_sector_dict[key] = value
            return portfolio_sector_dict
        except:
            import pdb
            pdb.set_trace()
#            import pickle
#            pickle.dump(sector, filename)
            raise

    def filter_list_by_criterion(self, alist, region, allSecurities, criterion = 'Sector'):
        new_list = []
        for item in alist:
            if allSecurities[item][criterion] == region:
                new_list.append(item)
        return new_list
    
    def filter_list_by_sector(self, alist, region, allSecurities):
        new_list = []
        for item in alist:
            if allSecurities[item]['Sector'] == region:
                new_list.append(item)
        return new_list
    
    def add_security_with_criterion(self, shares, region, preferences, allSecurities, criterion = 'Sector'):
        preferences = self.filter_list_by_criterion(preferences, region, allSecurities, criterion)
        # give error if list is empty
        pop = recom.recommend_stock(preferences)   
        security = next(pop)
        ok = True
        while self.security_exists_in_portfolio(self.portfolio, security):
            try:
                security = next(pop)
            except StopIteration:
                pyfancy.pyfancy().red("Cound not find a new security in {} {}".format(criterion, region)).output()
                ok = False
                break 
        if ok:
            self.addNewSecurity(security, shares, allSecurities)
            return True
        else:
            return False
        
    def cutExposureOnCriterion (self, new_exposure, region, all_preferences, allSecurities, criterion = 'Sector'):
        region_dict = self.extract_securities_by_criterion(region, allSecurities, criterion)
        current_exposure = sum(region_dict.values())
        diff = current_exposure - new_exposure
        while (diff > 0):
            pop = recom.reverse_recommend_stock(all_preferences) 
            security = next(pop)
            while (not self.security_exists_in_portfolio(region_dict, security)):
                security = next(pop)
            if (diff >= region_dict[security]):
                diff = diff - region_dict[security]
                self.deleteSecurity(security, allSecurities)
                region_dict.pop(security, None)
            else:
                self.setExposure(security, region_dict[security] - diff)
                region_dict[security] = region_dict[security] - diff
                diff = 0
        return True
    
    def deleteCriterion(self, sector, security_dict, criterion = 'Sector'):
        pyfancy.pyfancy().cyan("Scanning portfolio to delete securities from sector {}".format(sector)).output()
        time.sleep(1)
        securities_to_del = []
        for key, value in self.portfolio.items():
            current_security = security_dict[key]
            if current_security[criterion] == sector:
                securities_to_del.append(key)
        for key in securities_to_del:
            self.deleteSecurity(key, security_dict)
        print ('Deleted {} {}'.format(criterion, sector))
        
    def add_to_portfolio_as_preferences(self, allSecurities, preferences):
        print ("Checking your cash...")
        if (self.cash > 0):
            stocks_alloc, bonds_alloc = self.current_allocation(allSecurities)
            recommended_stock_alloc, recommended_bonds_alloc = self.recommended_allocation(self.client['Risk_profile'])
            print ("You have {} % exposure in cash \n".format(self.cash))
            if (stocks_alloc < recommended_stock_alloc):
                pyfancy.pyfancy().cyan("You don't have as many stocks as recommended, let's buy some \n").output()
                self.addStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc, preferences, True)
            if (bonds_alloc < recommended_bonds_alloc):
                pyfancy.pyfancy().cyan("You don't have as many bonds as recommended, let's buy some \n").output()
                self.addBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc, True)
    
    def extract_item_with_most_exposure(self, portfolio):
        sort_exposures_desc = []
        for key, value in sorted(portfolio.items(), key=lambda x:x[1], reverse = True):
            sort_exposures_desc.append(key)
        return sort_exposures_desc
    
    def remove_one_item(self, recommendations, asset_type, allSecurities):
        stocks_alloc, bonds_alloc = self.current_allocation(allSecurities)
        if (asset_type == 'Equity' or asset_type == 'equity' or asset_type == 'stock'):
            if stocks_alloc == 0:
                print ("You have no stocks to delete")
            else:
                pop = recom.reverse_recommend_stock(recommendations) 
                security = next(pop)    
                while not self.security_exists_in_portfolio(self.portfolio, security):
                    security = next(pop)
                self.deleteSecurity(security, allSecurities)
                print ("You now have {} % exposure in CASH.".format(self.extra_exposure))
        elif (asset_type == 'Bond' or asset_type == 'bond'):
            if bonds_alloc == 0:
                print ("You have no bonds to delete")
            else:
                pop = recom.reverse_recommend_stock(recommendations)    
                security = next(pop)    
                while not self.security_exists_in_portfolio(self.portfolio, security):
                    security = next(pop)
                self.deleteSecurity(security, allSecurities)
                print ("You now have {} % exposure in CASH.".format(self.extra_exposure))
                
    def add_one_item (self, preferences, exposure, allSecurities):
        pop = recom.recommend_stock(preferences)     
        security = next(pop)
        while self.security_exists_in_portfolio(self.portfolio, security):
            # stock exists, look for another one
            security = next(pop)
        self.addNewSecurity(security, exposure, allSecurities)
        return True
    

