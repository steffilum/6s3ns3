import dash 
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import os
from pages.news import df_articles, generate_card_scroll



# Set working directory to current file location
os.chdir(os.path.dirname(os.path.abspath(__file__)))


dash.register_page(__name__, path="/", name="Home") # Register the homepage

# Homepage layout
layout = html.Div(
    style={
        "height": "100vh",
        "background": "radial-gradient(circle at top left, #3e1f47 0%, #000000 25%)",
        "boxShadow": "0 0 100px #ff6a00",
        "margin": "0px",
        "padding": "0px",
        "position": "relative",
        "overflow": "hidden"
    },
    children=[
        html.Nav(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "padding": "20px 40px",
                "color": "rgba(206, 203, 203, 0.8)",
                "fontFamily": "Montserrat, sans-serif",
                "fontWeight": "400",
                "fontSize": "22px"
            },
            children=[
                # Logo that clicks to return to homepage
                dcc.Link("6SENS3", href='/', style={                     
                    "fontWeight": "800",
                    "fontSize": "32px", 
                    "position": "absolute",
                    "left": "75px",
                    "top": "35px",
                    "textDecoration": "none"},
                    className="logo-clickable"
                ),

                html.Div([
                    # About button as a link
                    dcc.Link("About", href="/about", style={
                        "position": "absolute",
                        "left": "482px",
                        "top": "42px",
                        "backgroundColor": "transparent",
                        "border": "none",
                        "fontFamily": "Montserrat, sans-serif",
                        "fontSize": "22px",
                        "cursor": "pointer",
                        "textDecoration": "none" 
                    }, className="fade-button-dropdown"),

                    html.Button("Models", id="model-fade-button", className= 'fade-button-dropdown', n_clicks=0, style={
                        "cursor": "pointer", 
                        "position": "absolute", 
                        "left": "669px", 
                        "top": "42px",
                        "backgroundColor": "transparent",
                        "border": "none",
                        
                        "fontFamily": "Montserrat, sans-serif",
                        "fontSize": "22px"
                    }),

                    html.Button("Indicators", id="indicator-fade-button", className= 'fade-button-dropdown', n_clicks=0, style={
                        "position": "absolute",
                        "left": "856px",
                        "top": "42px",
                        "backgroundColor": "transparent",
                        "border": "none",
                        
                        "fontFamily": "Montserrat, sans-serif",
                        "fontSize": "22px",
                        "cursor": "pointer"
                    })
                ])
            ]
        ),
        
        # Fade Dropdown for models
        dbc.Fade(
            id="model-fade",
            is_in=False,
            appear=True,
            children=html.Div(
                className="mega-dropdown",
                children=[
                    html.Div("Explore Models", className="dropdown-item-normal"),
                    dcc.Link("Model 1", href="/model1", className="dropdown-item-bold"),  # Link to model1 page
                    dcc.Link("Model 2", href="/model2", className="dropdown-item-bold"),  # Link to model2 page
                    dcc.Link("Model 3", href="/model3", className="dropdown-item-bold"),  # Link to model3 page
                    dcc.Link("Model 4", href="/model4", className="dropdown-item-bold"),  # Link to model4 page
                    dcc.Link("Compare Models", href="/comparemodels", className="dropdown-item-comparemodels") # Link to comparemodels page
                ]
            )
        ),
        # Fade Dropdown for indicators
        dbc.Fade(
            id="indicator-fade",
            is_in=False,
            appear=True,
            children=html.Div(
                className="mega-dropdown",
                children=[
                    html.Div("Explore Indicators", className="dropdown-item-normal"),
                    dcc.Link("CPI", href="/cpi", className="dropdown-item-bold"),
                    dcc.Link("Housing Starts", href="/cpi", className="dropdown-item-bold"),
                    dcc.Link("PMI", href="/cpi", className="dropdown-item-bold")
                
                ]
            )
        ),

        # Main content (blurs when dropdown is open)
        html.Div(
            id="main-content",
            style={
                "position": "absolute",
                "top": "120px",
                "left": "65px",
                "width": "300px",
                "height": "600px",
                "zindex": "1"
    },
            children=[
                html.H3("Top Stories this Week", style={
                    "color": "white",
                    "fontWeight": "600",
                    "fontSize": "22px",
                    "marginBottom": "20px",
                    "fontFamily": "Montserrat, sans-serif"}),
                html.Div(
                    children=[
                        generate_card_scroll(df_articles)],
                        style={
                            "position": "absolute",
                            "left": "-55px",
                            "display": "block",
                            "overflowY": "auto",
                            "overflowX": "hidden",
                            
                        }
                )]
                
        )
    ]
)




