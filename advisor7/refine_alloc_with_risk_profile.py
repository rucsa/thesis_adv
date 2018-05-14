from pyfancy import pyfancy

def getAllocations(client_portfolio, allSecurities, text = True):
    
    stocks_alloc, bonds_alloc = client_portfolio.current_asset_allocation(allSecurities)
    recommended_stock_alloc, recommended_bonds_alloc = client_portfolio.recommended_asset_allocation(client_portfolio.client['Risk_profile'])
    
    if text:
        pyfancy.pyfancy().cyan("Current allocation: {} stocks and {} bonds \n".format(stocks_alloc, bonds_alloc)).output()
        pyfancy.pyfancy().cyan("Recommended allocation: {} stocks and {} bonds \n".format(recommended_stock_alloc, recommended_bonds_alloc)).output()
    
    return stocks_alloc, bonds_alloc, recommended_stock_alloc, recommended_bonds_alloc

def balance_allocation (client_portfolio, allSecurities, bonds_alloc, stocks_alloc, recommended_bonds_alloc, recommended_stock_alloc, stock_preferences, bonds_preferences, economy, exposure):
    if (bonds_alloc < recommended_bonds_alloc):
        # add more bonds
        pyfancy.pyfancy().cyan("Not enough bonds. Current bond allocation: {}%. Recommended allocation for {} profile: {}%. Need to add {}% bonds exposure... \n".format(bonds_alloc, client_portfolio.client['Risk_profile'], recommended_bonds_alloc, recommended_bonds_alloc-bonds_alloc)).output()
        client_portfolio.addBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc, bonds_preferences, exposure)
        stocks_alloc, bonds_alloc = client_portfolio.current_asset_allocation(allSecurities)   
        pyfancy.pyfancy().cyan("Modified allocation to: {}% stocks and {}% bonds \n".format(stocks_alloc, bonds_alloc)).output()

    if (bonds_alloc > recommended_bonds_alloc):
        # remove from bonds
        pyfancy.pyfancy().cyan("Too many bonds. Current bond allocation: {}%. Recommended allocation for {} profile: {}%. Need to remove {}% bonds exposure... \n".format(bonds_alloc, client_portfolio.client['Risk_profile'], recommended_bonds_alloc, bonds_alloc-recommended_bonds_alloc)).output()
        client_portfolio.removeBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc, bonds_preferences, exposure)
        stocks_alloc, bonds_alloc = client_portfolio.current_asset_allocation(allSecurities) 
        pyfancy.pyfancy().cyan("Modified allocation to: {}% stocks and {}% bonds".format(stocks_alloc, bonds_alloc)).output()

    if (stocks_alloc < recommended_stock_alloc):
        # add more stocks 
        pyfancy.pyfancy().cyan("Not enough stocks. Current stock allocation: {}%. Recommended allocation for {} profile: {}%. Need to add {}% stocks exposure... \n".format(stocks_alloc, client_portfolio.client['Risk_profile'], recommended_stock_alloc, recommended_stock_alloc-stocks_alloc)).output()
        client_portfolio.addStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc, stock_preferences, exposure)
        stocks_alloc, bonds_alloc = client_portfolio.current_asset_allocation(allSecurities)
        pyfancy.pyfancy().cyan("Modified allocation to: {}% stocks and {}% bonds".format(stocks_alloc, bonds_alloc)).output()

    if (stocks_alloc > recommended_stock_alloc):
        # remove from stocks 
        pyfancy.pyfancy().cyan("Too many stocks. Current stock allocation: {}%. Recommended allocation for {} profile: {}%. Need to remove {}% stock exposure... \n".format(stocks_alloc, client_portfolio.client['Risk_profile'], recommended_stock_alloc, stocks_alloc-recommended_stock_alloc)).output()
        client_portfolio.removeStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc, stock_preferences, exposure)
        stocks_alloc, bonds_alloc = client_portfolio.current_asset_allocation(allSecurities)
        pyfancy.pyfancy().cyan("Modified allocation to: {}% stocks and {}% bonds".format(stocks_alloc, bonds_alloc)).output()

        
def refine_alloc_with_risk_profile (client_portfolio, allSecurities, stock_preferences, bonds_preferences, economy):
    stocks_alloc, bonds_alloc, recommended_stock_alloc, recommended_bonds_alloc = getAllocations(client_portfolio, allSecurities, True)
    if (stocks_alloc == recommended_stock_alloc and bonds_alloc == recommended_bonds_alloc):
        print ("Congrats! Asset allocation is set properly.")
    else:
        pyfancy.pyfancy().cyan("Started exposure refining... \n").output()
        balance_allocation(client_portfolio, allSecurities, bonds_alloc, stocks_alloc, recommended_bonds_alloc, recommended_stock_alloc, stock_preferences, bonds_preferences, economy, True)
    return client_portfolio.portfolio