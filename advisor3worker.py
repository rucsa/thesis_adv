from pyfancy import pyfancy
import recommender as recom
import time

def getAllocations(client_portfolio, allSecurities, text = True):
    
    stocks_alloc, bonds_alloc = client_portfolio.current_allocation(allSecurities)
    if text:
        pyfancy.pyfancy().cyan("Current allocation: {} stocks and {} bonds \n".format(stocks_alloc, bonds_alloc)).output()
    
    recommended_stock_alloc, recommended_bonds_alloc = client_portfolio.recommended_allocation(client_portfolio.client['Risk_profile'])
    if text:
        pyfancy.pyfancy().cyan("Recommendad allocation: {} stocks and {} bonds \n".format(recommended_stock_alloc, recommended_bonds_alloc)).output()
    
    return stocks_alloc, bonds_alloc, recommended_stock_alloc, recommended_bonds_alloc
    
def refine_alloc_with_risk_profile (client_portfolio, allSecurities, preferences, economy):
    stocks_alloc, bonds_alloc, recommended_stock_alloc, recommended_bonds_alloc = getAllocations(client_portfolio, allSecurities, True)
    time.sleep(1)
    if (stocks_alloc == recommended_stock_alloc and bonds_alloc == recommended_bonds_alloc):
        print ("Congrats! Asset allocation is set properly.")
    else:
        pyfancy.pyfancy().cyan("Started exposure refining... \n").output()
        time.sleep(1)
        recom.balance_allocation(client_portfolio, allSecurities, bonds_alloc, stocks_alloc, recommended_bonds_alloc, recommended_stock_alloc, preferences, economy, True)
    return client_portfolio.portfolio
    
def refine_exposure_to_5 (client_portfolio, allSecurities):
    stocks_alloc, bonds_alloc, recommended_stock_alloc, recommended_bonds_alloc = getAllocations(client_portfolio, allSecurities, False)
    pyfancy.pyfancy().cyan("Started exposure refining... \n").output()
    time.sleep(1)
    client_portfolio.refine_exposures()
    return client_portfolio.portfolio