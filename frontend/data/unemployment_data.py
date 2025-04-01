from fredapi import Fred
import pandas as pd
import os
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc


fred = Fred(api_key='aca56acb87a4241e0e9684e37849de17')

##############################################
# Data for Unemployment Rate
##############################################

unemployment = fred.get_series('UNRATE')

# convert to DataFrame
unemployment = unemployment.reset_index()
unemployment.columns = ['Date', 'unemployment']
unemployment['MonthYear'] = unemployment['Date'].dt.strftime('%b %Y')

# start data from 1993
unemployment = unemployment[unemployment['Date'] >= pd.Timestamp('1993-01-01')]

# Calculate year over year change in Unemployment Rate
unemployment['YOY Change'] = unemployment['unemployment'].pct_change(periods=12) * 100

# Calculate monthly over monthly change in Unemployment Rate
unemployment['MoM Change'] = unemployment['unemployment'].pct_change() * 100

# print(unemployment.tail())

def get_unemployment_graph(period=60):
    # get trailing 60 months of data
    unemployment_filtered = unemployment.iloc[-period:]
    fig = px.line(unemployment_filtered, x='MonthYear', y='MoM Change', title='Unemployment Rate, Seasonally Adjusted',
                  labels={"MonthYear": "", "MoM Change": "MoM Change (%)"}, template='plotly_dark')
    
    # Remove grid lines
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent plotting area
        margin=dict(l=0, r=0, t=50, b=50),
        title={
            "font": {
                "color": "grey",
                "family": "Montserrat, sans-serif"
            }
        },
        height=200
    )
    return fig

def get_latest_unemployment_change():
    # Latest Percent Change in unemployment round off to 2 dp
    latest_unployment = unemployment['MoM Change'].iloc[-1]
    return round(latest_unployment,2)

def get_latest_month():
    latest_month = unemployment['MonthYear'].iloc[-1]
    return latest_month

def get_next_month():
    latest_date = unemployment['Date'].iloc[-1]
    next_date = latest_date + pd.DateOffset(months=1)
    return f"{next_date:%B} {next_date:%Y}"

def get_next_release_date():
    latest_date = unemployment['Date'].iloc[-1]
    next_date = latest_date + pd.DateOffset(months=2)
    return f"{next_date:%B} {next_date:%Y}"

##############################################
# Data for Jobs Opening
##############################################

openings = fred.get_series('JTSJOL')

# convert to DataFrame
openings = openings.reset_index()
openings.columns = ['Date', 'openings']
openings['MonthYear'] = openings['Date'].dt.strftime('%b %Y')

# start data from 2000
openings = openings[openings['Date'] >= pd.Timestamp('2000-01-01')]

# Calculate year over year change in Jobs Openings
openings['YOY Change'] = openings['openings'].pct_change(periods=12) * 100

# Calculate monthly over monthly change in Jobs Openings
openings['MoM Change'] = openings['openings'].pct_change() * 100

# print(openings.head())

def get_openings_graph(period=60):
    # get trailing 60 months of data
    openings_filtered = openings.iloc[-period:]
    fig = px.line(openings_filtered, x='MonthYear', y='MoM Change', title='Total Nonfarm Job Openings, Seasonally Adjusted',
                  labels={"MonthYear": "", "MoM Change": "MoM Change (%)"}, template='plotly_dark')
    
    # Remove grid lines
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outer background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent plotting area
        margin=dict(l=0, r=0, t=50, b=50),
        title={
            "font": {
                "color": "grey",
                "family": "Montserrat, sans-serif"
            }
        },
        height=200
    )
    return fig

def get_latest_openings_change():
    # Latest Percent Change in openings round off to 2 dp
    latest_openings = openings['MoM Change'].iloc[-1]
    return round(latest_openings,2)

def get_latest_openingsfigure():
    latest_openings = openings['openings'].iloc[-1]
    value = round(latest_openings, 2) * 1000
    return f"{value:,.0f}"

def get_latest_month_openings():
    latest_month = openings['MonthYear'].iloc[-1]
    return latest_month

def get_next_month_openings():
    latest_date = openings['Date'].iloc[-1]
    next_date = latest_date + pd.DateOffset(months=1)
    return f"{next_date:%B} {next_date:%Y}"

def get_next_release_date_openings():
    latest_date = openings['Date'].iloc[-1]
    next_date = latest_date + pd.DateOffset(months=2)
    return f"{next_date:%B} {next_date:%Y}"





