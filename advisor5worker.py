
import recommender as recom
from pyfancy import pyfancy
import time

def advisor5(client_portfolio, allSecurities, economy):
    
    divers_sectors, divers_percent = recom.bc_sector_allocation(economy)
    # categorize existing securities by type of asset
    pyfancy.pyfancy().cyan("\n*** Portfolio analysis.... ***\n").output()
    time.sleep(1)
    stocks_held, bonds_held = client_portfolio.extract_securities_by_type(allSecurities)
    
    # categorize existing securities by sector
    pyfancy.pyfancy().cyan("\n *** Sectors you currently hold in stocks: ***").output()
    time.sleep(2)
    portfolio_sector_dict = client_portfolio.categorize_stocks_by_sector(allSecurities)
    
    # calculate recommended percentages per sector
    pyfancy.pyfancy().cyan("\n *** Sectors recommended to hold in stocks: ***").output()
    time.sleep(2)
    recomm_sector_dict = recom.recomm_sector_allocation(client_portfolio.portfolio, divers_percent, divers_sectors, sum(portfolio_sector_dict.values()))
    
    # add recommended sectors that do not exist
    pyfancy.pyfancy().cyan("\n *** Looking for sectors that should not be in your portfolio ***").output()
    time.sleep(2)
    sectors_to_del = client_portfolio.sectors_you_should_not_have(recomm_sector_dict, portfolio_sector_dict)
    if (len(sectors_to_del)==0):
        print ('No sectors to remove')
    else:
        for sector_del in sectors_to_del:
            client_portfolio.deleteSector(sector_del, allSecurities)
        
    
    # refine securities per sector
    pyfancy.pyfancy().cyan("\n *** Refining exposure for sectors you hold ***").output()
    time.sleep(2)
    for key, value in recomm_sector_dict.items():
        
        time.sleep(1)
        diff = recomm_sector_dict[key] - portfolio_sector_dict.get(key, 0) 
        
        if (diff == recomm_sector_dict[key]):
            # portfolio does not contain the recommended sector
            print ('No {} in the portfolio. You should add {} of them'.format(key, value))
            recommendations = recom.rank_stocks_without_bc(key)
            pop = recom.recommend_stock(recommendations)  
            security = next(pop)
            client_portfolio.addNewSecurity(security, value, allSecurities)
            
        elif (diff > 0):
            print ('You have {}% of {}. You should have {}% in {}.'.format(portfolio_sector_dict.get(key, 0), key, recomm_sector_dict.get(key, 0), key))
            current_holdings = client_portfolio.extract_securities_by_sector(key, allSecurities)
            print ("Currently holding {} stocks in sector {}:".format(len(current_holdings), key))
            for k, v in current_holdings.items():
                pyfancy.pyfancy().bold().white("{}       {} %".format(k,v)).output()

            recommendations = recom.rank_stocks_without_bc(key)
            pop = recom.recommend_stock(recommendations)  
            security = next(pop)
            client_portfolio.addNewSecurity(security, diff, allSecurities)
            
        elif (diff < 0):
            print ('You have {}% of {}. You should have {}% in {}.'.format(portfolio_sector_dict.get(key, 0), key, recomm_sector_dict.get(key, 0), key))
            current_holdings = client_portfolio.extract_securities_by_sector(key, allSecurities)
            print ("Currently holding {} stocks in sector {}:".format(len(current_holdings), key))
            for k, v in current_holdings.items():
                pyfancy.pyfancy().bold().white("{}       {} %".format(k,v)).output()
            current_holdings_list = sorted(current_holdings, key=current_holdings.get, reverse=True)
            diff = diff * (-1)
            for k in current_holdings_list:
                v = current_holdings[k]
                if diff == 0:
                    break
                elif (diff > 0  and v > diff):
                    client_portfolio.setExposure(k, v - diff)
                    diff = 0
                elif (diff > 0  and v <= diff):
                    client_portfolio.deteleSecurity(k, allSecurities)
                    diff -= v
    #print ('\n \n Exposure left in portfolio: {}'.format(client_portfolio.extra_exposure))
    stocks_held, bonds_held = client_portfolio.extract_securities_by_type(allSecurities)              
    return client_portfolio