import gspread
from oauth2client.client import GoogleCredentials
from google.auth import default
from decimal import Decimal
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import datetime as dt
import matplotlib.dates as mdates
import seaborn as sns
from garminconnect import Garmin
import datetime
from calendar import month_name as mn

# update with your own credentials
"""username = "ceceliasciuto@gmail.com"
password = "Kodak505!"

# connect to the API
garmin_client = Garmin(username, password)
garmin_client.login()

#get activities
activities = garmin_client.get_activities_by_date("2021-08-15", datetime.date.today(), "running")

# Process activities
activity_df = pd.DataFrame(activities)

# select required columns
activities_df = activity_df[[
  'startTimeLocal','activityName','activityType','distance','duration','averageHR','averageSpeed'
]]
# update activityType column to only contain activity type name
activities_df.loc[:, 'activityType'] = activities_df['activityType'].apply(lambda x: x['typeKey'])
activities_df['duration'] = activities_df['duration'].apply(lambda x: x/60)
activities_df['distance'] = activities_df['distance'].apply(lambda x: x/1609.34)
activities_df['pace'] = activities_df['duration']/activities_df['distance']
activities_df = activities_df[activities_df['pace'] < 15]
activities_df['date'] = pd.to_datetime(activities_df['startTimeLocal'])
activities_df.drop('startTimeLocal', axis=1)
activities_df['month'] = pd.DatetimeIndex(activities_df['date']).month
activities_df['year'] = pd.DatetimeIndex(activities_df['date']).year
activities_df_monthly=activities_df.resample(rule='M',on='date').agg({'date':'last','distance':'sum','averageHR':'mean','pace':'mean'})
activities_df.to_csv("runnningdata.csv")
"""
df = pd.read_csv("runnningdata.csv")
df = df.groupby(['month','year'], as_index=False).agg({'distance':'sum','averageHR':'mean','pace':'mean'})
print(df.to_html())

"""
#Plotting total distance run
p = sns.relplot(kind='line', data=df, x=df['month'], y=df['distance'], hue=df['year'], aspect=4, marker='o')
p.set(xticks=df['month'])
plt.title("Monthly Distance YoY (Miles)",fontdict={'fontsize': 16, 'fontweight': 'bold', 'color': 'black'})
plt.xlabel("Months",fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'black'})
plt.ylabel("Miles",fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'black'})
plt.legend(title="Year")
# Remove initial space
plt.xlim(df['month'].min(), df['month'].max())
plt.show()

#Plotting avg pace
p = sns.relplot(kind='line', data=df, x=df['month'], y=df['pace'], hue=df['year'], aspect=2, marker='o')
p.set(xticks=df['month'])
plt.title("Aervage Pace YoY (Min/Mile)",fontdict={'fontsize': 16, 'fontweight': 'bold', 'color': 'black'})
plt.xlabel("Min/Miles",fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'black'})
plt.ylabel("Miles",fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'black'})
plt.legend(title="Year")
# Remove initial space
plt.xlim(df['month'].min(), df['month'].max())
plt.show()


#Plotting avg hr
p = sns.relplot(kind='line', data=df, x=df['month'], y=df['averageHR'], hue=df['year'], aspect=2.5, marker='o')
p.set(xticks=df['month'])
plt.title("Aervage Heart Rate YoY (BPM)",fontdict={'fontsize': 16, 'fontweight': 'bold', 'color': 'black'})
plt.xlabel("BPM",fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'black'})
plt.ylabel("Miles",fontdict={'fontsize': 10, 'fontweight': 'bold', 'color': 'black'})
plt.legend(title="Year")
# Remove initial space
plt.xlim(df['month'].min(), df['month'].max())
plt.show()

"""
