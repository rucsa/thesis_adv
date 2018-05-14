from random import randint
import recommender as recom

class ClientPortfolio(object):
    portfolio = {}
    client = {}
    exposures = {}
    extra_exposure = 0 
    
    def __init__(self, security_list, client_series):
        for i in range(0, len(security_list)-1, 2):
            if security_list[i] != 'nan':
                self.portfolio[security_list[i]] = security_list[i+1]
        self.client = client_series.to_dict()  
        self.extra_exposure = 0
        
    def setCapital(self, capital):
        self.client['Capital'] = capital
        self.client['Goal'] = capital + randint(15, 30) /100 * capital
       
    def getCapital(self):
        return self.client['Capital']
    
    def setExposure(self, security, new_exposure):
        print ('Modified exposure for security {} from {} to {} \n'.format(security, self.portfolio[security], new_exposure))
        self.portfolio[security] = new_exposure
         
    def setExtraExposure(self, new_exposure):
        self.extra_exposure = new_exposure
        
    def addNewSecurity(self, security, shares):
        self.portfolio[security] = shares
        print ('Added to portfolio security {} with {} exposure'.format(security, shares))
        
    def deteleSecurity(self, security):
        exposure = self.portfolio.pop(security, None)
        print('Deleted security {} that had {} exposure'.format(security, exposure))
    
    def check_security_in_portfolio (self, portfolio, security):
        for item in portfolio:
            if item == security:
                return True
        return False
        
    def refine_exposures(self, exposure_threshold = 5):
        for key, exposure in self.portfolio.items():
            if (key != 'nan'):
                if exposure > exposure_threshold:
                    self.extra_exposure += (exposure - exposure_threshold)
                    self.setExposure(key, exposure_threshold)
            elif (key == 'nan'):
                break
        #print ('Extra exposure: {}'.format(self.extra_exposure))
    
        
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
                
    def addBondsToBalance(self, security_dict, bonds_alloc, recommended_bonds_alloc, exposure_threshold = 5):
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
            fit_exposure = min(exposure_threshold, (recommended_bonds_alloc - bonds_alloc))  
            # add shares to portfolio
            self.addNewSecurity(security, fit_exposure)
            # increase bond allocation
            bonds_alloc += fit_exposure 
            
    def removeBondsToBalance(self, security_dict, bonds_alloc, recommended_bonds_alloc):
        recommendations = recom.rank_etfs()  
        pop = recom.reversed_recommend_etf(recommendations) 
        while (bonds_alloc > recommended_bonds_alloc):
            security = next(pop)
            while (not self.check_security_in_portfolio(self.portfolio, security)):
                security = next(pop)
            security_exposure = self.portfolio[security]
            fit_exposure = min (security_exposure, bonds_alloc - recommended_bonds_alloc)
            if (fit_exposure == security_exposure): 
                # delete dictionary entry
                self.deteleSecurity(security)
                bonds_alloc -= fit_exposure
            elif (fit_exposure < security_exposure):
                # delete some of the shares
                
                self.setExposure(security, fit_exposure)
                bonds_alloc -= fit_exposure        
    
    def addStocksToBalance(self, security_dict, stocks_alloc, recommended_stock_alloc, exposure_threshold = 5):
        recommendations = recom.rank_stocks('Mid')  
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
            fit_exposure = min(exposure_threshold, (recommended_stock_alloc - stocks_alloc))
            # add shares to portfolio
            self.addNewSecurity(security, fit_exposure)
            # increase bond allocation
            stocks_alloc += fit_exposure
    
    def removeStocksToBalance(self, security_dict, stocks_alloc, recommended_stock_alloc):
        recommendations = recom.rank_stocks('Mid')  
        pop = recom.reverse_recommend_stock(recommendations) 
        while (stocks_alloc > recommended_stock_alloc):
            security = next(pop)
            while (not self.check_security_in_portfolio(self.portfolio, security)):
                security = next(pop)
            security_exposure = self.portfolio[security]
            fit_exposure = min (security_exposure, stocks_alloc - recommended_stock_alloc)
            if (fit_exposure == security_exposure): 
                # delete dictionary entry
                self.deteleSecurity(security)
                stocks_alloc -= fit_exposure
            elif (fit_exposure < security_exposure):
                # delete some of the shares
                self.setExposure(security, fit_exposure)
                stocks_alloc -= fit_exposure