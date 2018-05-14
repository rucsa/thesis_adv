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
        if (new_exposure > self.portfolio[security]):
            self.extra_exposure = self.extra_exposure - new_exposure + self.portfolio[security]
            print ('Extra exposure: taken {}. Currently set to {}'.format(new_exposure - self.portfolio[security], self.extra_exposure))
        elif (new_exposure < self.portfolio[security]):
            self.extra_exposure += self.portfolio[security] - new_exposure
            print ('Extra exposure: added {}. Currently set to {}'.format(self.portfolio[security] - new_exposure, self.extra_exposure))
        self.portfolio[security] = new_exposure
         
    def setExtraExposure(self, new_exposure):
        self.extra_exposure = new_exposure
        
    def addNewSecurity(self, security, shares):
        self.portfolio[security] = shares
        print ('Added to portfolio security {} with {} exposure'.format(security, shares))
        self.extra_exposure -= shares
        print ('Extra exposure: borrowed {}. Currently set to {}'.format(shares, self.extra_exposure))
        
    def deteleSecurity(self, security):
        exposure = self.portfolio.pop(security, None)
        print('Deleted security {} that had {} exposure'.format(security, exposure))
        self.extra_exposure = self.extra_exposure + exposure
        print ('Extra exposure: deleted {}. Currently set to {}'.format(exposure, self.extra_exposure))
        
    def deleteSector(self, sector, security_dict):
        print ('Scanning portfolio to delete securities from sector {}'.format(sector))
        securities_to_del = []
        for key, value in self.portfolio.items():
            current_security = security_dict[key]
            if current_security['Sector'] == sector:
                securities_to_del.append(key)
        for key in securities_to_del:
            self.deteleSecurity(key)
        print ('Deleted sector {}'.format(sector))
                
        
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
            print("{}      {} %".format(k, v))
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
    
    