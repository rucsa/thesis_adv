
"""
# takes input named series with numbered sectors 
# encodes back sectors as strings
# returns 2 arrays, labels and value for pie chart
"""
def decode_sector (sector_dict):
    encoding = {}
    for key, value in sector_dict.items():
        if (key == 1):
            encoding['Technology'] = value
        if (key == 2):
            encoding['Industrial'] = value
        if (key == 3):
            encoding['Communications'] = value
        if (key == 4):
            encoding['Financial'] = value
        if (key == 5):
            encoding['Basic Materials'] = value
        if (key == 6):
            encoding['Consumer, Non-cyclical'] = value
        if (key == 7):
            encoding['Consumer, Cyclical'] = value
        if (key == 8):
            encoding['Utilities'] = value
        if (key == 9):
            encoding['Energy'] = value
    return encoding

"""
# takes input named series with numbered regions 
# encodes back regions as string
# returns 2 arrays, labels and value for pie chart
"""
def dencode_region (region_dict):
    encoding = {}
    for key, value in region_dict.items():
        if (key == 1):
            encoding['Asia ex Japan'] = value
        if (key == 2):
            encoding['Canada'] = value
        if (key == 3):
            encoding['Emerging Markets'] = value
        if (key == 4):
            encoding['Europe ex UK'] = value
        if (key == 5):
            encoding['Japan'] = value
        if (key == 6):
            encoding['Other'] = value
        if (key == 7):
            encoding['UK'] = value
        if (key == 8):
            encoding['USA'] = value
    return encoding