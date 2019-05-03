import os
import glob
import pandas as pd

game_files = glob.glob(os.path.join(os.getcwd(),'games','*.EVE'))
game_files.sort()

#how do i know game_file is a single file in game_files?
game_frames=[]
for game_file in game_files:
    game_frame = pd.read_csv(game_file, names = ['type','multi2','multi3','multi4','multi5','multi6','event'])
    game_frames.append(game_frame)


games= pd.concat(game_frames)
#print (games)
#.loc?
games.loc[games['multi5']== '??', 'multi5'] = ''

#what on earth does the .extract (???) mean? is it extracting from 'multi2'?
identifiers =games['multi2'].str.extract(r'(.LS(\d{4})\d{5})')
identifiers = identifiers.fillna(method= 'ffill')
#At this point, identifiers is a two column array. First column is xLSxxxxyyyyy, second is xxxx
#do i just give them names or what?
identifiers.columns = ['game_id','year']

#what am I doing here?
games = pd.concat([games, identifiers], axis=1, sort= False)
games = games.fillna(' ')
games.loc[:,'type'] = pd.Categorical(games.loc[:,'type'])
print (games.head())
