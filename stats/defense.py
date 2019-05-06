import pandas as pd
import matplotlib.pyplot as plt

from data import games

plays = games[games['type']=='play']

plays.columns= ['type','inning','team', 'player', 'count','pitches','event', 'game_id', 'year']
#print (plays)
hits = plays.loc[plays['event'].str.contains('^(?:S(?!B)|D|T|HR)'), ['inning','event']]
#print(hits)

#plays.columns = ['inning', 'event']

#attendance.loc[:, 'attendance']= pd.to_numeric(attendance.loc[:, 'attendance'])
hits.loc[:, 'inning']= pd.to_numeric(hits.loc[:, 'inning'])

print (hits)

replacements= {r'^S(.*)': 'single', r'^D(.*)': 'double', r'^T(.*)': 'triple', r'^HR(.*)': 'hr'}

#this is just an array, with now converted 'event' called hit_type
hit_type= hits['event'].replace(replacements, regex=True)
#print(hit_type)

#add hit_type into hits matrix,
#now we have ['inning', 'event','hit_type']
hits= hits.assign(hit_type=hit_type)
#print (hits)

'''
In one line of code, group the hits DataFrame by inning and hit_type,
 call size() to count the number of hits per inning, 
 and then reset the index of the resulting DataFrame.
'''

hits = hits.groupby(['inning','hit_type']).size()

#how does it know the reset_index is the size()?
hits = hits.reset_index(name= 'count')

#print (hits)

hits['hit_type']= pd.Categorical(hits['hit_type'], ['single', 'double', 'triple', 'hr'])

#sort_values need parameter 'by=[column1, column2, ...]'
hits= hits.sort_values(by=['inning','hit_type'])
#print (hits)

hits= hits.pivot(index='inning', columns='hit_type',values='count')
#print (hits)

hits.plot.bar(stacked= True)

plt.show()
