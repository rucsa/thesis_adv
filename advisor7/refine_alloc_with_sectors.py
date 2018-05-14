
import recommender as recom
from pyfancy import pyfancy

def refine_alloc_with_sectors(client_portfolio, allSecurities, economy, stock_preferences, bonds_preferences, all_preferences):

    # recommended sector allocation
    divers_sectors, divers_percent = recom.bc_sector_allocation(economy)
    recomm_sector_dict = {}
    for i in range (0, len(divers_sectors)):
        recomm_sector_dict[divers_sectors[i]] = divers_percent[i]
    
    # check if we have enough stocks to fill sector alloc, add more if not
    while len(client_portfolio.portfolio) < len(recomm_sector_dict):
        sorted_exposures = client_portfolio.extract_item_with_most_exposure(client_portfolio.portfolio)
        pop = recom.recommend_stock(sorted_exposures)
        security = next(pop)
        security_exposure = client_portfolio.portfolio[security]
        exposure_to_remove = security_exposure/2
        exposure_to_add = security_exposure - exposure_to_remove
        client_portfolio.setExposure(security, exposure_to_remove)
        if (client_portfolio.getAssetType(security, allSecurities) == 'Equity'):
            client_portfolio.add_one_item(stock_preferences, exposure_to_add, allSecurities)
        elif (client_portfolio.getAssetType(security, allSecurities) == 'Bond'):
            client_portfolio.add_one_item(bonds_preferences, exposure_to_add, allSecurities)
    
    # current sector allocation
    portfolio_sector_dict = {}
    for sector in divers_sectors:
        sector_dict = client_portfolio.extract_securities_by_criterion(sector, allSecurities, 'Sector')
        portfolio_sector_dict[sector] = sum(sector_dict.values())
    
    
    # cut regions with too much exposure to get some cash
    for key, value in recomm_sector_dict.items():
        diff = portfolio_sector_dict.get(key, 0) - recomm_sector_dict[key]
        if diff > 0:
            client_portfolio.cutExposureOnCriterion(recomm_sector_dict[key], key, all_preferences, allSecurities, 'Sector')
            print ("Cut {} from region {}".format(diff, key))
            
    # cut exposure above recommended alloc    
    stocks_alloc, bonds_alloc = client_portfolio.current_asset_allocation(allSecurities)
    recommended_stock_alloc, recommended_bonds_alloc = client_portfolio.recommended_asset_allocation(client_portfolio.client['Risk_profile'])    
    print("You have {} stocks and {} bonds. Recommended {} stocks and {} bonds".format(stocks_alloc, bonds_alloc, recommended_stock_alloc, recommended_bonds_alloc))
    if (stocks_alloc > recommended_stock_alloc):
        client_portfolio.removeStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc, stock_preferences, True)
    if (bonds_alloc > recommended_bonds_alloc):
        client_portfolio.removeBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc, bonds_preferences, True)
    
    # check current allocation again         
    portfolio_sector_dict = {}
    for sector in divers_sectors:
        sector_dict = client_portfolio.extract_securities_by_criterion(sector, allSecurities, 'Sector')
        portfolio_sector_dict[sector] = sum(sector_dict.values())
    
    #now deal with adding more exposure to sectors that don't have enough
    for key, value in recomm_sector_dict.items():
        diff = recomm_sector_dict[key] - portfolio_sector_dict.get(key, 0)
        print ("adding {} in sector {}".format(diff, key))
        while diff > 0:
            #decide wheather to add a stock or a bond
            which_type = recom.recommend_asset_type(client_portfolio, allSecurities)
            for i in range(0, len(which_type), 2):
                if (which_type[i] == 'Equity' and diff > 0):
                    client_portfolio.add_security_with_criterion(min(diff, 5, which_type[i+1]), key, stock_preferences, allSecurities, 'Sector')
                    diff = diff - min(diff, 5, which_type[i+1])
                elif (which_type[i] == 'Bond' and diff > 0):
                    client_portfolio.add_security_with_criterion(min(diff, 5, which_type[i+1]), key, bonds_preferences, allSecurities, 'Sector')
                    diff = diff - min(diff, 5, which_type[i+1])
    print("finished sector alloc")
    return True