import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
from collections import Counter

import visualizations_utils as vut

def visualize(portfolio, options_list, filename):

#    portfolio = pd.read_hdf('output_data/portfolio_status.hdf5', 'Datataset1/X')
#    options_list = pd.read_hdf('output_data/option_list.hdf5', 'Datataset1/X')
    
    
    """ Portfolio
    """
    # Sector
    try:
        sector = Counter(portfolio['Sector'])
        port_sect_encoding = vut.decode_sector(sector)
    except KeyError:
        port_sect_encoding = Counter(portfolio['Sector_string']) 

    sector_labels = [*port_sect_encoding]
    sector_values = list(port_sect_encoding.values())
    
    # Region
    try:
        region = Counter(portfolio['Region'])
        port_reg_encoding = vut.dencode_region(region)
    except KeyError:
        port_reg_encoding = Counter(portfolio['Region_string'])
    
    region_labels = [*port_reg_encoding]
    region_values = list(port_reg_encoding.values())
    
    """ Output
    """
    # Sector
    try:
        sector = Counter(options_list['Sector'])
        out_sect_encoding = vut.decode_sector(sector)
    except KeyError:
        out_sect_encoding = Counter(options_list['Sector_string'])
    
    sector_labels_out = [*out_sect_encoding]
    sector_values_out = list(out_sect_encoding.values())
    
    # Region
    try:
        region = Counter(options_list['Region'])
        out_reg_encoding = vut.decode_sector(region)
    except KeyError:
        out_reg_encoding = Counter(options_list['Region_string'])

    region_labels_out = [*out_reg_encoding]
    region_values_out = list(out_reg_encoding.values())
    
    # plotting
    fig = {
        'data': [
            {
                'labels': sector_labels,
                'values': sector_values,
                'type': 'pie',
                'domain': {'x': [0, .48],
                           'y': [.51, 1]},
                'name' : 'Portfolio - Sector'
            },
            {
                'labels': region_labels,
                'values': region_values,
                'type': 'pie',
                'domain': {'x': [.52, 1],
                           'y': [.51, 1]},
                'name' : 'Portfolio - Region'
            },
            {
                'labels': sector_labels_out,
                'values': sector_values_out,
                'type': 'pie',
                'domain': {'x': [0, .48],
                           'y': [0, .49]},
                'name' : 'Output - Sector'
            },
            {
                'labels': region_labels_out,
                'values': region_values_out,
                'type': 'pie',
                'domain': {'x': [.52, 1],
                           'y': [0, .49]},
                'name' : 'Output - Region'
            }],
        'layout': {'title': 'Sector and Region Allocation',
                   'showlegend': True}
        }
    
    
    plot(fig, filename=filename, auto_open=False) # save image='jpeg')
        
        
    print ("SECTOR")
    print ("\nCurrently holding in portfolio: ")
    for k, v in port_sect_encoding.items():
        print ("{} : {}".format(k,v))
        
    print ("\nOptions sector allocation: ")
    for k, v in out_sect_encoding.items():
        print ("{} : {}".format(k,v))
            
        
        
    print ("\n\nREGION")
    print ("\nCurrently holding in portfolio: ")
    for k, v in port_reg_encoding.items():
        print ("{} : {}".format(k,v))
        
    print ("\nOptions region allocation: ")
    for k, v in out_reg_encoding.items():
        print ("{} : {}".format(k,v))
        
