from constraint import *
import pandas as pd
import numpy as np
import time

allSecurities = pd.read_hdf('stocks&etfs.hdf5', 'Datataset1/X') #.T.to_dict()

names = allSecurities[['Name','Price']].set_index('Name').T.to_dict()
print (names)

problem = Problem()
problem.addVariables('security', names)
problem.addConstraint(lambda k, v: v > 0, 'security')

tic = time.clock()
solutions = problem.getSolutions()
print (solutions)
toc = time.clock()
print (toc - tic)

