import dash 
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import os
from pages.news import df_articles, generate_card_scroll
from shared.default_pagelayout import get_default_layout 
from integration.model1 import get_forecast, get_forecast_graph, monthyear, get_quarter
from datetime import datetime
import calendar




# Set working directory to current file location
os.chdir(os.path.dirname(os.path.abspath(__file__)))


dash.register_page(__name__, path="/", name="Home") # Register the homepage

 # Main content for homepage
homepage_content = html.Div(
    id="main-content",
    style={
        "position": "absolute",
        "top": "60px",
        "left": "65px",
        "width": "300px",
        "height": "600px",
        "zIndex": "1", 
        "paddingBottom": "100px"
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
            "Select a Month and Year to forecast next Quarter GDP Growth Rate",
            style={
                "color": "rgba(206, 203, 203)",
                "fontWeight": "600",
                "fontSize": "20px",
                "marginBottom": "20px",
                "fontFamily": "Montserrat, sans-serif", 
                "position": "absolute",
                "left": "350px", 
                "top": "400px",
                "width": "900px"
            }
        ),
       
       
        # Container for Forecast label and value
        html.Div(
            children = [
                html.H1(
                    id = 'gdp-forecast-title',
                    children = ["GDP Forecast for: "],
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
                        "left": "360px",
                        "top": "-2px"}
        ), 
        # Container for displaying forecast graph
        html.Div( 
            children =[
            dcc.Graph(
                id = 'gdp-forecast-graph',
                figure = get_forecast_graph(),
                config = {"displayModeBar": False},
                style={
                    "position": "absolute",
                    "left": "316px",
                    "top": "70px",
                    "width": "900px",
                    "height": "620px",
                    "backgroundColor": 'transparent'
                }
            )
            ]

        ), 
        html.Div(
                id="myear-display",
                style={
                    "color": "grey",
                    "fontSize": "16px",
                    "marginBottom": "10px",
                    "fontFamily": "Montserrat, sans-serif",
                    "textAlign": "center", 
                    "position": "absolute",
                    "left": "189px",
                    "top": "430px",
                    "width": "500px"
        }
),
         # Dropdown for selecting the month/year
        html.Div(
            style={
                "position": "absolute",
                "left": "347px",
                "top": "470px",   
                "display": "flex",
                "flexDirection": "row",
                "gap": "10px",   
                "alignItems": "center"
        },
            children=[
                
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': m, 'value': m} for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                                                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']],
                    value= calendar.month_abbr[datetime.now().month],
                    className="myear-dropdown"
                ),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': str(year)} for year in range(datetime.now().year, 1999, -1)],
                    value=str(datetime.now().year),
                    className="myear-dropdown"
                ),
    ]
)

    
    ]
)
# Wrap the entire page content in a loading indicator
loading_content = html.Div(
    dcc.Loading(
        id="page-loading",
        type="circle",  
        children=homepage_content, 
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "height": "100vh" 
        }

    )
)


# Plug that content into your default layout
layout = get_default_layout(main_content=loading_content)


@dash.callback(
    Output('myear-display', 'children'),
    Output('gdp-forecast', 'children'),
    Output('gdp-forecast', 'style'),
    Output('gdp-forecast-graph', 'figure'),
    Output('gdp-forecast-title', 'children'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value')
)
def update_all(selected_year, selected_month):
    # Combine selected month and year into a single date string.
    selected_date = f"{selected_month} {selected_year}"
    
    # Build display text.
    display_text = html.Span([
        html.Span("Selected Time: ", style={"color": "grey"}),
        html.Span(selected_date, style={"color": "white", "fontWeight": "700"})
    ])
    
    # Base style for the forecast text.
    base_style = {
        "color": "grey",
        "fontWeight": "600",
        "fontSize": "28px",
        "fontFamily": "Montserrat, sans-serif"
    }
    
    # Get forecast value using the combined date string.
    value = get_forecast(selected_date)
    if value < 0:
        forecast_value = f"{value:.3f}%"
        forecast_style = {**base_style, "color": "red"}
    elif value > 0:
        forecast_value = f"{value:.3f}%"
        forecast_style = {**base_style, "color": "rgb(0, 200, 83)"}
    else:
        forecast_value = f"{value:.3f}%"
        forecast_style = {**base_style, "color": "white"}
    
    # Update the forecast graph.
    figure = get_forecast_graph(selected_date)
    
    # Update the title.
    forecast_title = f"GDP Forecast for {get_quarter(selected_date)}:"
    
    return display_text, forecast_value, forecast_style, figure, forecast_title