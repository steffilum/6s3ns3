import dash 
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import os
from pages.news import df_articles, generate_card_scroll
from shared.default_pagelayout import get_default_layout 
from data.fakedata1 import get_gdp_growth_rate, gdp_growth_df



# Set working directory to current file location
os.chdir(os.path.dirname(os.path.abspath(__file__)))


dash.register_page(__name__, path="/", name="Home") # Register the homepage

 # Main content for homepage
homepage_content = html.Div(
    id="main-content",
    style={
        "position": "absolute",
        "top": "120px",
        "left": "65px",
        "width": "300px",
        "height": "600px",
        "zIndex": "1"
    },
    children=[
        # Header "Top Stories this Week"
        html.H1(
            "Top Stories this Week",
            style={
                "color": "white",
                "fontWeight": "600",
                "fontSize": "22px",
                "marginBottom": "20px",
                "fontFamily": "Montserrat, sans-serif"
            }
        ),
        # Container for the articles
        html.Div(
            children=[
                generate_card_scroll(df_articles)
            ],
            style={
                "position": "absolute",
                "left": "-55px",
                "display": "block",
                "overflowY": "auto",
                "overflowX": "hidden"
            }
        ),
        html.Label(
            "Select a Quarter to Forecast GDP Growth Rate",
            style={
                "color": "white",
                "fontWeight": "600",
                "fontSize": "22px",
                "marginBottom": "20px",
                "fontFamily": "Montserrat, sans-serif", 
                "position": "absolute",
                "left": "600px"
            }
        ),
        # Range input
        dcc.Input(
            id = 'quarter-picker',
            type = 'text',
            placeholder='Enter Quarter (e.g. 1950Q1)',
            value='1950Q1',  # Default value
            style={"width": "150px", "height": "40px", "position": "absolute", "left": "800px"}
        ),
       
        # Container for Forecast label and value
        html.Div(
            children = [
                html.H1(
                    "GDP Forecast for Next Quarter:",
                    style={
                        "color": "rgba(206, 203, 203)",
                        "fontWeight": "600",
                        "fontSize": "22px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                ),
                html.H2(
                    id = 'gdp-forecast', children="",
                    style={
                        "color": "white",
                        "fontWeight": "600",
                        "fontSize": "28px",
                        "fontFamily": "Montserrat, sans-serif"
                    }
                ),

                ], style={"position": "absolute",
                        "height": "5px",
                        "width": "500px", 
                        "left": "350px",
                        "top": "-2px"}
        )
        
        
    ]
)

# Plug that content into your default layout
layout = get_default_layout(main_content=homepage_content)

# Callback to update the GDP forecast value
@dash.callback(
    Output('gdp-forecast', 'children'),
    Input('quarter-picker', 'value')
)

def update_gdp_forecast(selected_quater):
    if selected_quater not in gdp_growth_df['Quarter'].values:
        return "No data found"
    value = get_gdp_growth_rate(selected_quater)
    return f"{value:.2f}%"



