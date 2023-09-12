#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns

data= pd.read_csv('matches - matches.csv')
delivery= pd.read_csv('deliveries.csv')
data
delivery

data.head() 
data.shape
data.info()

data.describe() #only works on numerical columns

data['winner'] #fetching column
                #it is a series(because its a single column)

data[['team1','team2','winner']].shape

data['winner'].shape #its a tuple

data.iloc[0] #fetching rows

data.iloc[1:3] #fetching multiple rows

data.iloc[1:11:2]

data.iloc[:,[4,5,10]] #fetching multiple columns

# filtering dataframe based on a given conditon
#masking
mask= data['city']=='Hyderabad'
mask
mask=data['city']=='Hyderabad'
data[mask]

#function to count the no. of matches happen in a particular city
def get_city_match_count(city):
    mask=data['city']==city
    return data[mask].shape[0]

mask1=data['city']=='Hyderabad'
mask2=data['date']>"2010-01-01"
data[mask1 & mask2].shape[0]

# The Pandas plot()
import matplotlib.pyplot as plt

#bar chart is used to represent categorical data
data["winner"].value_counts().plot(kind='bar')

data["winner"].value_counts().head().plot(kind='barh')
data['toss_decision'].value_counts()
data['toss_decision'].value_counts().plot(kind='pie')

#histogram is used to represent numerical data
data['win_by_runs'].plot(kind='hist')

#series operations
myseries=data['winner'].value_counts()
myseries    #left side = index, right side= value
myseries['Royal Challengers Bangalore']


#value_counts()... it works on categorical data/series
data['winner'].value_counts()

data['team1'].value_counts()+data['team2'].value_counts()
data['team1'].value_counts()-data['team2'].value_counts()
data['team1'].value_counts()*data['team2'].value_counts()
data['team1'].value_counts()/data['team2'].value_counts()

#sort_values() method
(data['team1'].value_counts()+data['team2'].value_counts()).sort_values()
(data['team1'].value_counts()+data['team2'].value_counts()).sort_values(ascending=False)
data.sort_values(['city','date'])
data.sort_values(['city','date'],ascending=[True,False])

# drop_duplicates() Method
data.sort_values('id', ascending=True, inplace=True)
data
data.drop_duplicates(subset=['city'])
data.drop_duplicates(subset=['city','season'])
data.drop_duplicates('season', keep='last')[['season','winner']]

data.drop_duplicates('season', keep='last')[['season','winner']].sort_values('season')

#group_by() function
sectors=data.groupby('season')
sectors.size().sort_values(ascending=False)
sectors.last()
sectors.groups
sectors.sum()
sectors['win_by_runs'].mean().sort_values(ascending=False)

#Using Deliveries dataset
total_runs=delivery.groupby('batsman')
total_runs.get_group('V Kohli')
total_runs['batsman_runs'].sum()
total_runs['batsman_runs'].sum().sort_values(ascending=False)

#top 5 batsman with the most '4'
mask=delivery['batsman_runs']==4  
new_delivery=delivery[mask]
new_delivery.groupby('batsman')['batsman_runs'].count().sort_values(ascending=False)

# VK scores most runs against which 3 teams?
vk= delivery[delivery['batsman']=='V Kohli']
vk.groupby('bowling_team')['batsman_runs'].sum().sort_values(ascending=False).head(3)

# Most runs scored by the batsman against a particular team
def run_scored(batsman_name):
    runs= delivery[delivery['batsman']== batsman_name]
    return runs.groupby('bowling_team')['batsman_runs'].sum().sort_values(ascending=False).index[0]

# To calculate the strike rate in a match
death_over=delivery[delivery['over']>15]
all_batsman=death_over.groupby('batsman')['batsman_runs'].count()
x=all_batsman>200
batsman_list=all_batsman[x].index.tolist() 
final=delivery[delivery['batsman'].isin(batsman_list)]
total_runs=final.groupby('batsman')['batsman_runs'].sum()
total_balls=final.groupby('batsman')['ball'].count()
strike_rate=(total_runs/total_balls)*100
strike_rate

# Using Merge Function to create a new dataframe by two different dataframes 
new=delivery.merge(data,left_on='match_id',right_on='id')
new.groupby(['season','batsman'])['batsman_runs'].sum().sort_values(ascending=False).reset_index().drop_duplicates(subset='season',keep='first')

# Applying Pivot Table to the dataframe
mask=delivery['batsman_runs']==6
six=delivery[mask]
pt=six.pivot_table(index='over',columns='batting_team',values='batsman_runs',aggfunc='count')

sns.heatmap(pt) # creating a heatmap 

# Corr Function -> to find the relation b/w two numerical quantities
new.corr()
sns.heatmap(new.corr()) # creating a heatmap

