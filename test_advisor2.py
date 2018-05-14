import unittest
from utils import calculate_portfolio_value
from utils import current_allocation
from utils import check_security_in_portfolio

from ClientPortfolio import ClientPortfolio

class TestAdvisor2(unittest.TestCase):
    
    portfolio_dict = {'A': 3, 'B':9, 'C':10, 'D':7}
    security_dict = {'A': {'1YReturn': -1.58, 'Asset': 'Bond', 'Price': 27.36, 'Symbol': 'a'},
                      'B': {'1YReturn': 2.33, 'Asset': 'Equity', 'Price': 4.31, 'Symbol': 'b'},
                      'C': {'1YReturn': 4.58, 'Asset': 'Bond', 'Price': 15.6, 'Symbol': 'c'},
                      'D': {'1YReturn': 3.13, 'Asset': 'Equity', 'Price': 4.5, 'Symbol': 'b'}}
    capital = 308.37
    
    def test_calculate_portfolio_value(self):
        self.assertEqual(calculate_portfolio_value(self.portfolio_dict, self.security_dict), self.capital)
        
    def test_current_allocation(self):
        self.assertEqual(current_allocation(self.security_dict, self.portfolio_dict, self.capital), (22.794046113435158, 77.20595388656484))
        self.assertNotEqual(current_allocation(self.security_dict, self.portfolio_dict, self.capital), (50, 50))
        
    def test_check_security_in_portfolio(self):
        self.assertTrue(check_security_in_portfolio(self.portfolio_dict, 'A'))
        self.assertFalse(check_security_in_portfolio(self.portfolio_dict, 'V'))

if __name__ == '__main__':
    unittest.main()