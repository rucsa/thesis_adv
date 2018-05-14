import unittest
import numpy as np
import pandas as pd
from ClientPortfolio7 import ClientPortfolio
from random import randint

class TestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.allSecurities = pd.read_hdf('../hdfs/stocks&etfs.hdf5', 'Datataset1/X').set_index('Name').T.to_dict()
        cls.investors = pd.read_hdf('../hdfs/clients.hdf5', 'DatatasetCli').set_index('Id')
        cls.portfolios = pd.read_hdf('../hdfs/portfolios.hdf5', 'DatatasetPort')

#        cls.client_id = randint(1, 99)
#        cls.client = cls.investors.iloc[cls.client_id]
#        cls.client_portfolio = ClientPortfolio(cls.portfolios.iloc[cls.client['Portfolio_Id']].tolist(), 
#                                   cls.client)
        cls.client = pd.Series({'Age': 27, 'Capital': 17300, 'Goal': 20100, 'Name': 'Michael', 
                  'Portfolio_Id': 15, 'Retirement': 61, 
                  'Risk_profile': 'Moderate Offensive', 'Timeline': 34}) #64
        cls.portfolio = ['BioTelemetry', 10, 'Eaton Corporation', 7, 
                      'Ingredion Inc', 12, 'NetApp', 6, 'NetScout Systems', 44, 
                      'On Assignment, Inc', 6, 'Perrigo', 13, 'Tetra Technologies', 2]
        cls.client_portfolio = ClientPortfolio(cls.portfolio, cls.client)
        
        cls.portfolio_dict = {'BioTelemetry': 10, 'Eaton Corporation': 7, 
                      'Ingredion Inc': 12, 'NetApp': 6, 'NetScout Systems': 44, 
                      'On Assignment, Inc': 6, 'Perrigo': 13, 'Tetra Technologies': 2}
        cls.portfolio_security_added = {'BioTelemetry': 10, 'Eaton Corporation': 7, 
                      'Ingredion Inc': 12, 'NetApp': 6, 'NetScout Systems': 44, 
                      'On Assignment, Inc': 6, 'Perrigo': 13, 'Tetra Technologies': 2,
                      'ANI Pharmaceuticals': 5}
        cls.exposure = 5
        

    def test_getAssetType (self):
        np.random.seed(100)
        self.assertEqual(self.client_portfolio.getAssetType('ANI Pharmaceuticals', self.allSecurities), 'Equity')
        self.assertEqual(self.client_portfolio.getAssetType('iShares MBS ETF', self.allSecurities), 'Bond')
        
    def test_addNewSecurity (self):
        self.assertEqual(self.client_portfolio.addNewSecurity('ANI Pharmaceuticals', self.exposure, self.allSecurities), self.portfolio_security_added)
        self.assertEqual(self.client_portfolio.cash, 0-self.exposure)
    
    def test_deleteSecurity (self):
        self.assertEqual(self.client_portfolio.deleteSecurity('ANI Pharmaceuticals', self.allSecurities), self.portfolio_dict)
        self.assertEqual(self.client_portfolio.cash, 0)
    
    def test_setExposure (self):
        self.client_portfolio.setExposure('Perrigo', 10)
        self.assertEqual(self.client_portfolio.cash, 3)
        self.assertEqual(self.client_portfolio.portfolio['Perrigo'], 10)
    
    def test_current_asset_allocation (self):
        pass
    
    def test_recommended_asset_allocation (self):
        pass
    
    def test_security_exists_in_portfolio (self):
        pass
    
    def test_addBondsToBalance (self):
        pass
    
    def test_removeBondsToBalance (self):
        pass
    
    def test_addStocksToBalance (self):
        pass
    
    def test_removeStocksToBalance (self):
        pass
    
    def test_extract_securities_by_criterion (self):
        self.assertEqual(self.client_portfolio.extract_securities_by_criterion('Consumer, Non-cyclical', self.allSecurities, 'Sector'), \
                         {'BioTelemetry': 10, 'Ingredion Inc': 12, 'On Assignment, Inc': 6, 'Perrigo': 13})
        self.assertEqual(self.client_portfolio.extract_securities_by_criterion('Industrial', self.allSecurities, 'Sector'), \
                          {'Eaton Corporation': 7})
        self.assertEqual(self.client_portfolio.extract_securities_by_criterion('Energy', self.allSecurities, 'Sector'), \
                          {'Tetra Technologies': 2})
        self.assertEqual(self.client_portfolio.extract_securities_by_criterion('Technology', self.allSecurities, 'Sector'), \
                          {'NetApp': 6, 'NetScout Systems': 44})
        self.assertEqual(self.client_portfolio.extract_securities_by_criterion('Financial', self.allSecurities, 'Sector'), {})
        self.assertEqual(self.client_portfolio.extract_securities_by_criterion('Basic Materials', self.allSecurities, 'Sector'), {})
        self.assertEqual(self.client_portfolio.extract_securities_by_criterion('Communications', self.allSecurities, 'Sector'), {})
        self.assertEqual(self.client_portfolio.extract_securities_by_criterion('Consumer, Cyclical', self.allSecurities, 'Sector'), {})
        self.assertEqual(self.client_portfolio.extract_securities_by_criterion('Utilities', self.allSecurities, 'Sector'), {})
       
    
    def test_filter_list_by_criterion (self):
        pass
    
    def test_add_security_with_criterion (self):
        pass
    
    def test_cutExposureOnCriterion (self):
        pass
    
    def test_deleteCriterion (self):
        pass
    
    def test_extract_item_with_most_exposure (self):
        pass
    
    def test_remove_one_item (self):
        pass

    def test_add_one_item (self):
        pass
        
    
if __name__ == '__main__':
    unittest.main()