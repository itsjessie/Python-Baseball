import pandas as pd
import matplotlib.pyplot as plt
from data import games

#print (games)
#games.set_index("type", inplace = True)
#games.loc['info']

attendance= games.loc[ (games['type'] == 'info') & (games['multi2'] == 'attendance'), ['year','multi3']]
attendance.columns=['year', 'attendance']

# print (attendance)

attendance.loc[:, 'attendance']= pd.to_numeric(attendance.loc[:, 'attendance'])

attendance.plot( x='year',y='attendance',figsize= (15,7), kind='bar')
plt.xlabel('Year')
plt.ylabel('Attendance')

plt.axhline( label= 'Mean', y = attendance['attendance'].mean(), color= 'green', linestyle= 'dashed')

plt.show()
