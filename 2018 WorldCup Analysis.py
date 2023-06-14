

# In[1]:



import pandas as pd
import numpy as np
from pandas.io.json import json_normalize #special package in pandas
import json
from lxml import etree
import sqlite3


# # Part A: Reading json

# In[2]:


# Run this cell to import the following JSON strings
players = '[{"name":"Gazinsky","team":"Russia"},{"name":"Dzyuba","team":"Russia"},{"name":"Lukaku","team":"Belgium"}]'
stadium_data = '{"stadiums":[{"name": "Ekaterinburg Arena","city": "Ekaterinburg"},{"name": "Luzhniki Stadium","city": "Moscow"},{"name": "Nizhny Novgorod Stadium","city": "Nizhny Novgorod"}]}'


# In[3]:



players_json = json.loads(players)
# dictionary containing information about Romelu Lukaku
print(players_json[2])


# In[4]:


# loading stadium_data as a json object
stadium_data_json = json.loads(stadium_data)
# printing the city of Luzhniki Stadium 
for stadium in stadium_data_json['stadiums']:
    if stadium['name'] == 'Luzhniki Stadium':
        print(stadium['city'])


# In[5]:


# reading world cup match data from the worldcup.json file into a json object
with open('worldcup.json', encoding='utf-8') as f:
    worldcup_json = json.load(f)
# printing the date of the first match
print(worldcup_json['rounds'][0]['matches'][0]['date'])


# In[6]:


# reading world cup team data from the worldcup.teams.json file into json object
with open('worldcup.teams.json', encoding='utf-8') as f:
    worldcup_teams_json = json.load(f)
# print the name of the first team in the team data
print(worldcup_teams_json['teams'][0]['name'])


# In[7]:


# creating a list of dictionaries with the soccer associations and continents as the keys & values
 
soccer_associations = [
    {"continent": "Europe", "association": "Union of European Football Associations"},
    {"continent": "Asia", "association": "Asian Football Confederation"},
    {"continent": "Africa", "association": "Confédération Africaine de Football"}
]
# Europe - Union of European Football Associations 
# Asia - Asian Football Confederation
# Africa - Confederation Africaine de Football 


# # Part B: Flattening json

# In[8]:


# flattening the players json object created in Part A into a data frame with one row per player
players_df = pd.json_normalize(players_json)
print(players_df.head())


# In[9]:


# flattening the stadium data json object created in Part A into a data frame with one row per stadium
stadiums_df = pd.json_normalize(stadium_data_json, ['stadiums'])
print(stadiums_df.head())


# In[10]:


# flatten the world cup match json object created in Part A (fourth cell)  into a data frame with one row per match
matches_df = pd.json_normalize(worldcup_json, record_path=['rounds', 'matches'])
print(matches_df.shape)
print(matches_df.head())


# In[11]:


# flattening the team data json object created in Part A (fifth cell) into a data frame with one row per team
teams_df = pd.json_normalize(worldcup_teams_json, ['teams'])

print(teams_df.shape)
print(teams_df.head())


# In[12]:


# flattening the soccer association list of dictionaries created in Part A (sixth cell) into a data frame with one row per association
associations_df = pd.DataFrame(soccer_associations)
print(associations_df.shape)
print(associations_df.head())


# # Part C: SQL

# In[13]:


# creating a database and sql connection 
conn = sqlite3.connect('soccer_db.sqlite')


# In[14]:


# saving the players data set created in part B as a sql table in the database
players_df.to_sql('players', conn, if_exists='replace', index=False)


# In[15]:


# saving the stadiums data set created in part B as a sql table in the database
stadiums_df.to_sql('stadiums', conn, if_exists='replace', index=False)


# In[16]:


# saving the world cup match data set created in part B as a sql table in the database
matches_df.drop(columns=['goals1', 'goals2']).to_sql('matches', conn, if_exists='replace', index=False)


# In[17]:


# saving the teams data set created in part B as a sql table in the database
teams_df[['code','continent', 'name']].to_sql('teams', conn, if_exists='replace', index=False)


# In[18]:


3 using SQL syntax to select only those rows where Mexico played as team1 (team1.name) OR team2 (team2.name) from the database, and save these rows as a data frame

mexico_games_df = pd.read_sql('SELECT * FROM matches WHERE "team1.name"="Mexico" OR "team2.name"="Mexico"', conn)

# counting the number of rows in the data frame
print(len(mexico_games_df))

print(mexico_games_df.head())


# In[19]:


#SelectING only those rows that were tied games from the database and save these rows as a data frame

tie_games_df = pd.read_sql('SELECT * FROM matches WHERE score1=score2', conn)
print(len(tie_games_df))
print(tie_games_df.head())


# # Part D: Visualization
# 

# In[21]:


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
sns.countplot(x='continent', data=teams_df)
plt.title('Number of Teams per Continent')
plt.show()


# In[23]:


match_city = matches_df['city'].value_counts()

plt.figure(figsize=(10,6))
plt.pie(match_city, labels = match_city.index, autopct='%1.1f%%')
plt.title('Number of Matches Played in Each City')
plt.show()


# In[29]:


# First, we need to calculate the total number of goals for each team
matches_df['total_goals'] = matches_df['score1'] + matches_df['score2']

# Then, we group by team and sum up the total goals
team_goals = matches_df.groupby('team1.name')['total_goals'].sum().sort_values(ascending=False)

# We then select the top 5 teams with the most goals
top5_teams = team_goals[:5]

# Create a bar plot
plt.figure(figsize=(10,6))
plt.barh(top5_teams.index, top5_teams, color='skyblue')
plt.xlabel('Number of Goals')
plt.title('Top 5 teams with most goals')
plt.gca().invert_yaxis() # To display the team with most goals on top
plt.show()


# In[34]:


# We first need to convert the date to datetime format
matches_df['date'] = pd.to_datetime(matches_df['date'])

# We then group by date and sum the total goals
goals_over_time = matches_df.groupby('date')['total_goals'].sum()

# Create a line plot
plt.figure(figsize=(12,6))
plt.plot(goals_over_time)
plt.xlabel('Date')
plt.ylabel('Number of Goals')
plt.title('Goals scored over time')
plt.show()


# In[37]:





# In[ ]:




