from pyfancy import pyfancy
import recommender as recom

def getAllocations(client_portfolio, allSecurities, text = True):
    
    stocks_alloc, bonds_alloc = client_portfolio.current_asset_allocation(allSecurities)
    recommended_stock_alloc, recommended_bonds_alloc = client_portfolio.recommended_asset_allocation(client_portfolio.client['Risk_profile'])
    
    if text:
        pyfancy.pyfancy().cyan("Current allocation: {} stocks and {} bonds \n".format(stocks_alloc, bonds_alloc)).output()
        pyfancy.pyfancy().cyan("Recommended allocation: {} stocks and {} bonds \n".format(recommended_stock_alloc, recommended_bonds_alloc)).output()
    
    return stocks_alloc, bonds_alloc, recommended_stock_alloc, recommended_bonds_alloc
    
    
def refine_exposure_to_5 (client_portfolio, allSecurities, preferences):
    stocks_alloc, bonds_alloc, recommended_stock_alloc, recommended_bonds_alloc = getAllocations(client_portfolio, allSecurities, False)
    pyfancy.pyfancy().cyan("Started exposure refining... \n").output()
    for key, exposure in client_portfolio.portfolio.items():
        if (key != 'nan'):
            if exposure > 5:
                client_portfolio.setExposure(key, 5)
        elif (key == 'nan'):
            break
    return client_portfolio.portfolio