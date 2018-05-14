import pandas as pd
import utils as ut

def rank_by_preferences(u_in, data, economy, show = True):
    
    score = {}
    criterions = []
    criterions.append('Name')
    desc_df = pd.DataFrame()
    
    ### score anr
    if (1 in u_in):
        score = ut.score_feature(data, score, 'ANR')
        criterions.append('ANR')
        
    if (2 in u_in):
        score = ut.score_feature(data, score, 'Dividents')
        criterions.append('Dividents')
    
    ### score P/E
    if (3 in u_in):
        score = ut.score_feature(data, score, 'PE')
        criterions.append('PE')
    
    ### score returns last 3 months
    if (4 in u_in):
        score = ut.score_feature(data, score, 'Returns_3_months')
        criterions.append('Returns_3_months')
        
    if (5 in u_in):
        score = ut.score_feature(data, score, 'Ethics')
        criterions.append('Ethics')
    
    if (6 in u_in):
        score = ut.score_feature(data, score, 'Bribery')
        criterions.append('Bribery')
     
    ### score sectors from BC   
    if (7 in u_in):
        sectors = ut.check_bc(economy)
        score = ut.score_sectors(data, sectors, score)
        criterions.append('Sector')
            
    ### determine ranking
    rank = ut.rank_scores(score)
    
    ### make df
    reasoning = pd.DataFrame(list(rank.items()), columns=['Company', 'Score'])
    reasoning = reasoning.set_index('Company')
    desc_df = data[criterions]
    desc_df = desc_df.set_index('Name')
    
    ranking = pd.concat([reasoning, desc_df], axis=1)
    ranking = ranking.sort_values(by='Score', axis=0, ascending=False)
    
    criterions.remove('Name')
    if show:
        print(ranking.head(25))
        
    return ranking

def select_preferences():
    print ('Select the preferences you want to enable. Unspecified preferences will be disabled.')
    print ("1 - High analyst rating for the previous year")
    print ("2 - Company pays dividents")
    print ("3 - High P/E ratio over the previous year")
    print ("4 - High returns for the past 3 months")
    print ("5 - Company implements ethics policy")
    print ("6 - Company implements bribery policy")
    print ("7 - Include business cycle")
    print ("0 - Exit preferences settings withou saving")
    u_in = [int(y) for y in input('Enable preferences.. ').split()]
    for val in u_in:
        if (val < 1 & val > 7):
            print ('Inserted value unknown.. Try again.. ')
            u_in = [int(y) for y in input('Enable preferences.. ').split()]
    return u_in