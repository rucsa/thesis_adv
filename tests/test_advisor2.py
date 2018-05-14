import unittest
from utils import calculate_portfolio_value

class TestAdvisor2(unittest.TestCase):
    
    def setUpClass(cls):
        cls.security_dict = {'A': 3, 'B':9, 'C':10}
        cls.portfolio_dict = {'A': {'1YReturn': -1.58, 'Asset': 'Bond', 'Price': 27.36, 'Symbol': 'a'},
                      'B': {'1YReturn': 2.33, 'Asset': 'Equity', 'Price': 4.31, 'Symbol': 'b'},
                      'C': {'1YReturn': 4.58, 'Asset': 'Bond', 'Price': 15.6, 'Symbol': 'c'}}
    
    def test_calculate_portfolio_value(self):
        self.assertEqual(calculate_portfolio_value(self.portfolio_dict, self.security_dict), 276.87)

if __name__ == '__main__':
    unittest.main()