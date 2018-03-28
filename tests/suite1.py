from __future__ import print_function
from __future__ import division

import unittest


def f(x):
    return 1


#make a class with tests
class _generic_test_stuff(unittest.TestCase):
    """
    Class containing unittests
    """

    #tests should begin with test_
    def test_f(self):
        """
        Convert isin to Morningstar security id, scrapge morningstar page and test for same isin
        """
        self.assertEqual(f(3),1)


if __name__ == "__main__":
    _run_unit_tests=True
    _test_only = list() # if list is empty then test all
    #test_only.append('test_transform_shape')
    if _run_unit_tests:
        if len(_test_only) > 0:
            _suite = unittest.TestSuite()
            for ut in _test_only:
                _suite.addTest(_generic_test_stuff(ut))
            unittest.TextTestRunner().run(_suite)
        else:
            #unittest.main()
            _suite = unittest.TestLoader().loadTestsFromTestCase(_generic_test_stuff)
            unittest.TextTestRunner(verbosity=2).run(_suite)
    else:
        #do something else
        pass