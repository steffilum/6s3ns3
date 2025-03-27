import dash 
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import os
from pages.news import df_articles, generate_card_scroll
from shared.default_pagelayout import get_default_layout 

dash.register_page(__name__, path="/", name="Home") # Register the homepage

# Homepage layout
homepage_content = html.Div(
    # Main content (blurs when dropdown is open)
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
        html.H3(
            "Top Stories this Week",
            style={
                "color": "white",
                "fontWeight": "600",
                "fontSize": "22px",
                "marginBottom": "20px",
                "fontFamily": "Montserrat, sans-serif"
            }
        ),
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
        )
    ]  
)


# Plug that content into your default layout
layout = get_default_layout(main_content=homepage_content)



