import pandas as pd
import matplotlib.pyplot as plt

'''
Purpose: 'What is the DER by league since 1978?'

Note: 'DER' stands for 'Defensive Efficiency Ratio', 
and is used as a metric to gauge team defense.
'''


from frames import games,info,events

#print (games)
plays = games.query( "type == 'play' & event !='NP'")
plays.columns = ('type', 'inning', 'team', 'player', 'count', 'pitches', 'event', 'game_id', 'year')

#print (plays['player'])

#To select all rows that do not match a consecutive row
# in the player column use the row condition:
#how does .shift( ) work I am still confused.
pa= plays.loc[ (plays['player'].shift() != plays['player']), ['year', 'game_id', 'inning', 'team','player']]
#print (pa)

pa= pa.groupby(['year', 'game_id', 'team']).size().reset_index(name= 'PA')
#print(pa)

'''we need to reshape the data by the type of event
that happened at each plate appearance.
The event types need to be the columns of our DataFrame.
The unstack() function is perfect for this.'''

# adjusting index of the events df imported from frames
events = events.set_index(['year', 'game_id', 'team', 'event_type'])
#print (events)

#After we unstack() our events DataFrame it will have multiple levels of column labels.
events= events.unstack().fillna(0).reset_index()
#print (events)

# droplevel() to remove one level.
events.columns= events.columns.droplevel()

events.columns = ['year', 'game_id', 'team', 'BB', 'E', 'H', 'HBP', 'HR', 'ROE','SO']

#remove the label of the index using rename_axis().
# Pass in a label of None and make sure it is on the columns axis.
events= events.rename_axis('None', axis='columns')

events_plus_pa= pd.merge(events, pa, how='outer',
                         left_on=['year', 'game_id','team'],right_on=['year', 'game_id','team'])
#print (events)
#print (pa)
#print (events_plus_pa)

defense= pd.merge(events_plus_pa, info)

defense.loc[:, 'DER']= 1-((defense['H'] + defense['ROE']) /
                          (defense['PA'] -defense ['BB'] - defense['SO']
                           - defense['HBP']-defense ['HR']))
defense.loc[:, 'year']=pd.to_numeric(defense.loc[:,'year'])
#print (defense['year'])

der= defense.loc[(defense['year'] >= 1978), ['year', 'defense','DER']]

der= der.pivot(index='year', columns= 'defense',values= 'DER' )
#print(der)

der.plot(x_compat= True, xticks= range(1978, 2018, 4), rot= 45)

plt.show()
