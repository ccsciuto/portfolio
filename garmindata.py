from garminconnect import Garmin
import datetime
import json
from calendar import month_name as mn
import plotly.express as px
import plotly.graph_objects as go
import base64
import numpy as np
import pandas as pd


# update with your own credentials
username = "ceceliasciuto@gmail.com"
password = "Kodak505!"

# connect to the API
garmin_client = Garmin(username, password)
garmin_client.login()

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
df_file = activities_df.copy()
df_file['date'] = pd.to_datetime(df_file['startTimeLocal']).dt.strftime('%Y-%m-%d')
activities_df['date'] = pd.to_datetime(activities_df['startTimeLocal'])
activities_df.drop('startTimeLocal', axis=1)
df_file.drop('startTimeLocal', axis=1, inplace=True)
activities_df['month'] = pd.DatetimeIndex(activities_df['date']).month
activities_df['year'] = pd.DatetimeIndex(activities_df['date']).year


# Assuming `activities_df` is your clean DataFrame
activities_df['date'] = pd.to_datetime(activities_df['date'])
activities_df['month'] = activities_df['date'].dt.month
activities_df['year'] = activities_df['date'].dt.year

# Group by Year + Month
monthly_df = activities_df.groupby(['year', 'month']).agg({
    'distance': 'sum',
    'averageHR': 'mean',       # Include avg HR
    'pace': 'mean'             # Optional: Include pace too
}).reset_index()

# Convert month number to name
monthly_df['month_name'] = pd.to_datetime(monthly_df['month'], format='%m').dt.strftime('%b')
monthly_df['month_num'] = monthly_df['month']
monthly_df = monthly_df.sort_values(by=['month_num'])

# Sort by month number so plot goes Jan–Dec
monthly_df['month_num'] = monthly_df['month']
monthly_df = monthly_df.sort_values(by=['month_num'])


# Plot using Plotly
pink_shades = ['#ff99cc', '#ff66b2', '#ff3399', '#ff1a8c', '#e60073']
fig_distance = px.line(
    monthly_df,
    x='month_name',
    y='distance',
    color='year',
    color_discrete_sequence=pink_shades,
    markers=True,
    labels={
        'distance': 'Total Distance (mi)',
        'month_name': 'Month',
        'year': 'Year'
    },
    title="Monthly Running Distance (YoY)"
)

# Improve layout
fig_distance.update_layout(
    plot_bgcolor='#2e2e2e',  # inner plot area
    paper_bgcolor='#1e1e1e',  # outer paper area
    font=dict(color='white'),  # axis & title labels,
    title_font_size=20,
    legend_title_text='Year',
    xaxis=dict(categoryorder='array', categoryarray=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], gridcolor='rgba(255, 255, 255, 0.1)'),
    yaxis_title="Miles",
    xaxis_title="Month"
)
fig_distance.write_html("static/charts/running_distance_chart.html")

# Plot using Plotly
fig_hr= px.line(
    monthly_df,
    x='month_name',
    y='averageHR',
    color='year',
    color_discrete_sequence=pink_shades,
    markers=True,
    labels={
        'averageHR': 'Avg Heart Rate (BPM)',
        'month_name': 'Month',
        'year': 'Year'
    },
    title="Monthly Average Heart Rate (BPM)"
)

# Improve layout
fig_hr.update_layout(
    plot_bgcolor='#2e2e2e',  # inner plot area
    paper_bgcolor='#1e1e1e',  # outer paper area
    font=dict(color='white'),  # axis & title labels,
    title_font_size=20,
    legend_title_text='Year',
    xaxis=dict(categoryorder='array', categoryarray=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], gridcolor='rgba(255, 255, 255, 0.1)'),
    yaxis_title="BPM",
    xaxis_title="Month"
)

fig_hr.write_html("static/charts/running_avg_hr_chart.html")

# Plot using Plotly
fig_pace= px.line(
    monthly_df,
    x='month_name',
    y='pace',
    color='year',
    color_discrete_sequence=pink_shades,
    markers=True,
    labels={
        'pace': 'Avg Pace (Min/Mile)',
        'month_name': 'Month',
        'year': 'Year'
    },
    title="Monthly Average Pace (Min/Mile)"
)

# Improve layout
fig_pace.update_layout(
    plot_bgcolor='#2e2e2e',  # inner plot area
    paper_bgcolor='#1e1e1e',  # outer paper area
    font=dict(color='white'),  # axis & title labels,
    title_font_size=20,
    legend_title_text='Year',
    xaxis=dict(categoryorder='array', categoryarray=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], gridcolor='rgba(255, 255, 255, 0.1)'),
    yaxis_title="Min/Mile",
    xaxis_title="Month"
)

fig_pace.write_html("static/charts/running_avg_pace_chart.html")

