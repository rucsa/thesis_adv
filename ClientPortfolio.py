from random import randint
import recommender as recom
import utils as ut

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
    
    def setShares(self, security, new_shares):
        print ('Modified number of shares for security {} from {} shares to {} shares \n'.format(security, self.portfolio[security], new_shares))
        self.portfolio[security] = new_shares
        
    def setExtraExposure(self, new_exposure):
        self.extra_exposure = new_exposure
        
    def addNewSecurity(self, security, shares):
        self.portfolio[security] = shares
        print ('Added to portfolio security {} with {} shares'.format(security, shares))
        
    def deteleSecurity(self, security):
        shares = self.portfolio.pop(security, None)
        print('Deleted {} shares from security {}'.format(shares, security))
        
    def deleteSharesFromSecurity(self, shares_to_delete, security):
        self.portfolio[security] = self.portfolio[security] - shares_to_delete
        print('Deleted {} shares from security {}. Remaining {} shares '.format(shares_to_delete, security, self.portfolio[security]))
            
    def refine_exposure(self, security_dict, exposure_threshold = 0.05):
        for key, shares in self.portfolio.items():
            if (key != 'nan'):
                current_security = security_dict[key]
                price = current_security['Price']
                exposure = shares * price /  self.getCapital()
                if exposure > exposure_threshold:
                    self.extra_exposure += (exposure - exposure_threshold)
                    new_shares = exposure_threshold * self.getCapital() / price        
                    print ('Security {} has too much exposure: {}'.format(key, exposure))
                    print ('Extra exposure {}'.format(exposure - exposure_threshold))
                    self.setShares(key, new_shares)
            elif (key == 'nan'):
                break
        print ('Total extra exposure in the portfolio {}'.format(self.extra_exposure))
            
    def complete_exposure(self, security_dict, exposure_threshold = 0.05):
        recommendations = recom.rank_stocks('Mid')  
        pop = recom.recommend_stock(recommendations)  
        
        while (self.extra_exposure > 0):
            security = next(pop)
            # check if the recommended security is in the portfolio already and get the second best if it is
            while ut.check_security_in_portfolio(self.portfolio, security):
                security = next(pop)
            
            if self.extra_exposure >= exposure_threshold:
                exp = exposure_threshold
                self.setExtraExposure(self.extra_exposure - exposure_threshold)
            else:
                exp = self.extra_exposure
                self.setExtraExposure(0)
            current_security = security_dict[security]
            price = current_security['Price']
            sha = exp * self.getCapital() / price
            self.addNewSecurity(security, sha)
            print ('Added security {} with {} shares and {} exposure'.format(security, sha, exp))
            
    def addBondsToBalance(self, security_dict, bonds_alloc, recommended_bonds_alloc, exposure_threshold = 0.05):
        recommendations = recom.rank_etfs()  
        pop = recom.recommend_etf(recommendations)  
        while (bonds_alloc < recommended_bonds_alloc):
            # get a recommendation
            security = next(pop)
            print ('Checking if bond {} exists in portfolio'.format(security))
            # check if the recommended security is in the portfolio already and get the second best if it is
            while ut.check_security_in_portfolio(self.portfolio, security):
                print ('Bond {} exists in portfolio'.format(security))
                security = next(pop)
                print ('Checking if bond {} exists in portfolio'.format(security))
            # desired exposure
            fit_exposure = min(exposure_threshold, (recommended_bonds_alloc - bonds_alloc) / 100)  
            # calculated desired shares to fit 0.05 exposure
            shares = fit_exposure * self.client['Capital'] / security_dict[security]['Price']
            current_exposure = shares * security_dict[security]['Price'] / self.client['Capital']
            # add shares to portfolio
            self.addNewSecurity(security, shares)
            # increase bond allocation
            bonds_alloc += current_exposure * 100
            
    def removeBondsToBalance(self, security_dict, bonds_alloc, recommended_bonds_alloc):
        recommendations = recom.rank_etfs('Mid')  
        pop = recom.reversed_recommend_etf(recommendations) 
        while (bonds_alloc > recommended_bonds_alloc):
            security = next(pop)
            while (not ut.check_security_in_portfolio(self.portfolio, security)):
                security = next(pop)
            security_exposure = self.portfolio[security] * security_dict[security]['Price'] / self.client['Capital'] * 100
            fit_exposure = min (security_exposure, bonds_alloc - recommended_bonds_alloc)
            if (fit_exposure == security_exposure): 
                # delete dictionary entry
                self.deteleSecurity(security)
                bonds_alloc -= fit_exposure
            elif (fit_exposure < security_exposure):
                # delete some of the shares
                shares_to_delete = fit_exposure / 100 * self.client['Capital'] / security_dict[security]['Price']
                self.deleteSharesFromSecurity(shares_to_delete, security)
                bonds_alloc -= fit_exposure        
    
    def addStocksToBalance(self, security_dict, stocks_alloc, recommended_stock_alloc, exposure_threshold = 0.05):
        recommendations = recom.rank_stocks('Mid')  
        pop = recom.recommend_stock(recommendations)      
        while (stocks_alloc < recommended_stock_alloc):
            # get a recommendation
            security = next(pop)
            print ('Checking if stock {} exists in portfolio'.format(security))
            # check if the recommended security is in the portfolio already and get the second best if it is
            while ut.check_security_in_portfolio(self.portfolio, security):
                print ('Stock {} exists in portfolio'.format(security))
                security = next(pop)
                print ('Checking if stock {} exists in portfolio'.format(security))
            # desired exposure
            fit_exposure = min(exposure_threshold, (recommended_stock_alloc - stocks_alloc) / 100)
            # calculated desired shares to fit 0.05 exposure
            shares = fit_exposure * self.client['Capital'] / security_dict[security]['Price']
            current_exposure = shares * security_dict[security]['Price'] / self.client['Capital']
            # add shares to portfolio
            self.addNewSecurity(security, shares)
            # increase bond allocation
            stocks_alloc += current_exposure * 100
    
    def removeStocksToBalance(self, security_dict, stocks_alloc, recommended_stock_alloc):
        recommendations = recom.rank_stocks('Mid')  
        pop = recom.reverse_recommend_stock(recommendations) 
        while (stocks_alloc > recommended_stock_alloc):
            security = next(pop)
            while (not ut.check_security_in_portfolio(self.portfolio, security)):
                security = next(pop)
            security_exposure = self.portfolio[security] * security_dict[security]['Price'] / self.client['Capital'] * 100
            fit_exposure = min (security_exposure, stocks_alloc - recommended_stock_alloc)
            if (fit_exposure == security_exposure): 
                # delete dictionary entry
                self.deteleSecurity(security)
                stocks_alloc -= fit_exposure
            elif (fit_exposure < security_exposure):
                # delete some of the shares
                shares_to_delete = fit_exposure / 100 * self.client['Capital'] / security_dict[security]['Price']
                self.deleteSharesFromSecurity(shares_to_delete, security)
                stocks_alloc -= fit_exposure