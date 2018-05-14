import recommender as recom

def yield_item (list_):
    yield from list_
    
def recom_alloc_per_region (regions, regions_alloc):
    recom_regions_dict = {}
    for i in range(0, len(regions)):
        recom_regions_dict[regions[i]] = regions_alloc[i]
    return recom_regions_dict

def refine_alloc_with_regions (client_portfolio, allSecurities, stock_preferences, bonds_preferences, all_preferences):
    regions = ['USA', 'Europe ex UK', 'Emerging Markets', 'Japan', 'UK', 'Canada', 'Other', 'Asia ex Japan']
    regions_alloc = [52, 15, 12, 8, 6, 3, 2, 2]
    
    
    
    # if client has less securities than the number of regions in MSCI, 
    # sort desc exposure of held securities and cut in half the exposure of top first
    # with the remaining half exposure add one security of the same type as the removed one
    # repeat until portfolio has as many securities as regions in MSCI
    while len(client_portfolio.portfolio) < len(regions):
        sorted_exposures = client_portfolio.extract_item_with_most_exposure(client_portfolio.portfolio)
        pop = yield_item(sorted_exposures)
        security = next(pop)
        security_exposure = client_portfolio.portfolio[security]
        exposure_to_remove = security_exposure/2
        exposure_to_add = security_exposure - exposure_to_remove
        client_portfolio.setExposure(security, exposure_to_remove)
        if (client_portfolio.getAssetType(security, allSecurities) == 'Equity'):
            client_portfolio.add_one_item(stock_preferences, exposure_to_add, allSecurities)
        elif (client_portfolio.getAssetType(security, allSecurities) == 'Bond'):
            client_portfolio.add_one_item(bonds_preferences, exposure_to_add, allSecurities)
    
    # allocations per regions in portfolio
    port_regions_dict = {}
    for region in regions:
        security_dict_per_region = client_portfolio.extract_securities_by_criterion(region, allSecurities, 'Region')
        port_regions_dict[region] = sum(security_dict_per_region.values())
    print ("Current region allocation:")
    print (port_regions_dict)
        
    # recommended allocations per region
    recom_regions_dict = recom_alloc_per_region(regions, regions_alloc)
    print ("Recommended region allocation:")
    print (recom_regions_dict)      
    
      
    # refine remaining alloc
    # cut regions with too much exposure to get some cash
    for key, value in recom_regions_dict.items():
        diff = port_regions_dict.get(key, 0) - recom_regions_dict[key]
        if diff > 0:
            client_portfolio.cutExposureOnCriterion(recom_regions_dict[key], key, all_preferences, allSecurities, 'Region')
            print ("Cut {} from region {}".format(diff, key))
     
    # cut exposure above recommended alloc    
    stocks_alloc, bonds_alloc = client_portfolio.current_asset_allocation(allSecurities)
    recommended_stock_alloc, recommended_bonds_alloc = client_portfolio.recommended_asset_allocation(client_portfolio.client['Risk_profile'])    
    print("You have {} stocks and {} bonds. Recommended {} stocks and {} bonds".format(stocks_alloc, bonds_alloc, recommended_stock_alloc, recommended_bonds_alloc))
    if (stocks_alloc > recommended_stock_alloc):
        client_portfolio.removeStocksToBalance(allSecurities, stocks_alloc, recommended_stock_alloc, stock_preferences, True)
    if (bonds_alloc > recommended_bonds_alloc):
        client_portfolio.removeBondsToBalance(allSecurities, bonds_alloc, recommended_bonds_alloc, bonds_preferences, True)
        
    # Just to be sure       
    # allocations per regions in portfolio
    port_regions_dict = {}
    for region in regions:
        security_dict_per_region = client_portfolio.extract_securities_by_criterion(region, allSecurities, 'Region')
        port_regions_dict[region] = sum(security_dict_per_region.values())
    print ("Current region allocation:")
    print (port_regions_dict)
            
    #now deal with adding more exposure to regions that don't have enough
    for key, value in recom_regions_dict.items():
        diff = recom_regions_dict[key] - port_regions_dict.get(key, 0)
        print ("adding {} in region {}".format(diff, key))
        while diff > 0:
            #decide wheather to add a stock or a bond
            which_type = recom.recommend_asset_type(client_portfolio, allSecurities)
            for i in range(0, len(which_type), 2):
                if (which_type[i] == 'Equity' and diff > 0):
                    client_portfolio.add_security_with_criterion(min(diff, 5, which_type[i+1]), key, stock_preferences, allSecurities, 'Region')
                    diff = diff - min(diff, 5, which_type[i+1])
                elif (which_type[i] == 'Bond' and diff > 0):
                    client_portfolio.add_security_with_criterion(min(diff, 5, which_type[i+1]), key, bonds_preferences, allSecurities, 'Region')
                    diff = diff - min(diff, 5, which_type[i+1])
    print("finished regions alloc")
    return True        
     
    





    