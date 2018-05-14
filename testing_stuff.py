

def normalize_value(value, minimum, maximum, x = 1, y = 100):
    return ((value-minimum) / (maximum-minimum)) * (y - x) + x


x = [18.1, 16.8, 11.76, 12.26, 11.62, 9.04, 6.32, 5.25, 3.11, 2.97, 2.77]

for i in range(1, len(x)):
    part_list = []
    percent_list = []
    for j in range(0, i):
        part_list.append(x[j]) 

    total_part = sum(part_list)
    for j in range(0, len(part_list)):
        percent_list.append(part_list[j]*100/total_part)
        
        
#if (bonds_held > 0):
#    # normalize exposure of sectors in portfolio
#    norm_portfolio_sector_dict = {}
#    sum_sectors_exposure = sum(portfolio_sector_dict.values())
#    for key, value in portfolio_sector_dict.items():
#        norm_portfolio_sector_dict[key] = 100 * value / sum_sectors_exposure
        
        
#        recommendations = recom.rank_stocks_without_bc(key)
#        pop = recom.recommend_stock(recommendations)  
#        while (value > 0):
#            try:
#                security = next(pop)
#            except StopIteration:
#                print ('Out of stocks for sector {} to recommend'.format(key))
#                security = 'undefined'
#            while ut.check_security_in_portfolio(client_portfolio.portfolio, security) and security != 'undefined':
#                try:
#                    security = next(pop)
#                except StopIteration:
#                    print ('Out of stocks for sector {} to recommend'.format(key))
#            client_portfolio.addNewSecurity(security, value)
#            value = 0
        
#        if (diff < 0):
#            diff = diff * (-1)
#            for key1, value1 in current_holdings.items():
#                while (diff > 0):
#                    if (value1 > diff + 5):
#                        client_portfolio.setExposure(key1, value1 - diff)
#                        diff = 0
#                    elif (value1 < diff):
#                        client_portfolio.setExposure(key1, diff - value1)
#                        client_portfolio.deteleSecurity(key1)
#                        diff = diff - value1
#                    print ('diff is {}'.format(diff))
#        elif (diff > 0):
#            for key2, value2 in current_holdings.items():
#                if (value2 < 5):
#                    to_add = 5 - value
#                    diff -= to_add
#                    client_portfolio.setExposure(key2, value + to_add)
#            while (diff > 0):
#                recommendations = recom.rank_stocks_without_bc(key)
#                pop = recom.recommend_stock(recommendations)  
#                security = next(pop)
#                while ut.check_security_in_portfolio(client_portfolio.portfolio, security):
#                    security = next(pop)
#                client_portfolio.addNewSecurity(security, min(5, diff))
#                diff = diff - min(5, diff)
        
#    # delete regions that are in current allocation, but not in recommended allocation
#    regions_you_should_not_have = client_portfolio.sectors_you_should_not_have(recom_regions_dict, port_regions_dict)
#    if (len(regions_you_should_not_have)==0):
#        print ('No regions to remove')
#    else:
#        for region_del in regions_you_should_not_have:
#            client_portfolio.deleteRegion(region_del, allSecurities)
                    