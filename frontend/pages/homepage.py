import dash 
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import os
from pages.news import df_articles, generate_card_scroll
from shared.default_pagelayout import get_default_layout 
from integration.model1 import get_forecast, get_forecast_graph, monthyear, get_quarter
from datetime import datetime




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
            "Select a Month to forecast next Quarter GDP Growth Rate",
            style={
                "color": "rgba(206, 203, 203)",
                "fontWeight": "600",
                "fontSize": "20px",
                "marginBottom": "20px",
                "fontFamily": "Montserrat, sans-serif", 
                "position": "absolute",
                "left": "350px", 
                "top": "400px",
                "width": "700px"
            }
        ),
        # label for start
        # html.Label(
            # "Start Quarter",
               # style={
                # "color": "white",
                # "fontWeight": "400",
                # "fontSize": "18px",
                # "marginBottom": "20px",
                # "fontFamily": "Montserrat, sans-serif", 
                # "position": "absolute",
                # "left": "350px", 
                # "top": "550px", 
                # "width": "200px"
            # }
        # ),
        # Range input
        # dcc.Input(
            # id = 'start-quarter-picker',
            # type = 'text',
            # placeholder='Enter Quarter (e.g. 1950Q1)',
            # value='1950Q1',  # Default value
            # style={"width": "150px", "height": "40px", "position": "absolute", "left": "350px", 'top': '500px'}
        # ),
        # dcc.Input(
            # id = 'end-quarter-picker',
            # type = 'text',
            # placeholder='Enter Quarter (e.g. 2025Q1)',
            # value = '2023Q4',
            # style={"width": "150px", "height": "40px", "position": "absolute", "left": "1050px", 'top': '500'}
        # ),
       
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
        # Range Slider for selecting the quarter
        html.Div( 
             style = {
                    "position": "absolute",
                    "left": "330px",
                    "top": "490px",
                    "width": "800px"}, 
            children = [
                dcc.Slider(
                    id = 'myear-slider',
                    min = 0, 
                    max = len(monthyear()) -1, 
                    step = 1, 
                    value = len(monthyear()) - 1,
                    marks={
                        i: {'label': month, 'style': {'color': 'grey', 'fontSize': '12px'}}
                        for i, month in enumerate(monthyear())
                        if i % 24 == 0
                    },
                    tooltip={"always_visible": False, "placement": "bottom"}
                    )
            ]
        ), 
            # Container for displaying selected month year
            html.Div(
                id="myear-display",
                style={
                    "color": "grey",
                    "fontSize": "16px",
                    "marginBottom": "10px",
                    "fontFamily": "Montserrat, sans-serif",
                    "textAlign": "center", 
                    "position": "absolute",
                    "left": "188px",
                    "top": "430px",
                    "width": "500px"
        }
),

    
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


# Callback to update the GDP forecast value
# @dash.callback(
    # Output('gdp-forecast', 'children'),
    # Output('gdp-forecast', 'style'),
    # Input('end-quarter-picker', 'value'),
    # Input('start-quarter-picker', 'value')
# )

# def update_gdp_forecast(selected_quater):
    # base_style = {
        # "color": "grey",
        # "fontWeight": "600",
        # "fontSize": "28px",
        # "fontFamily": "Montserrat, sans-serif"
    # # }
    # if selected_quater not in gdp_growth_df['Quarter'].values:
    #     return "No data found", base_style
    
    # value = get_gdp_growth_rate(selected_quater)
    # if value < 0:
    #     return f"{value:.2f}%", {**base_style, "color": "red"}
    # if value > 0:
    #     return f"{value:.2f}%", {**base_style, "color": "rgb(0, 200, 83)"}
    # else: 
    #     return f"{value:.2f}%", {**base_style, "color": "white"}



# @dash.callback(
#     Output('gdp-forecast-graph', 'figure'),
#     Input('start-quarter-picker', 'value'), 
#     Input('end-quarter-picker', 'value')
# )

# def update_gdp_forecast_graph(selected_start, selected_end):
#     if selected_start not in gdp_growth_df['Quarter'].values or selected_end not in gdp_growth_df['Quarter'].values:
#         return get_forecast_graph("1950Q1", "2023Q4")
#     else: 
#         return get_forecast_graph(selected_start, selected_end)


#            @dash.callback(
 #               Output('gdp-forecast-graph', 'figure'),
 #               Input('quarter-range-slider', 'value')
 #           )

 #           def update_range(selected_range):
  #              start_idx, end_idx = selected_range
  #              start_quarter = quarters[start_idx]
   #             end_quarter = quarters[end_idx]
   #             return get_forecast_graph(start_quarter, end_quarter)

@dash.callback(
    Output('myear-display', 'children'),
    Output('gdp-forecast', 'children'),
    Output('gdp-forecast', 'style'),
    Output('gdp-forecast-graph', 'figure'),
    Output('gdp-forecast-title', 'children'),
    Input('myear-slider', 'value')
)
def update_all(selected_index):
    
    selected_date = monthyear()[selected_index]


    # Build display text
    display_text = html.Span([
        html.Span("Selected Time: ", style={"color": "grey"}),
        html.Span(selected_date, style={"color": "white", "fontWeight": "700"})
    ])
    
    # Define a base style for forecast text
    base_style = {
        "color": "grey",
        "fontWeight": "600",
        "fontSize": "28px",
        "fontFamily": "Montserrat, sans-serif"
    }
    
    

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
    
    # Update the title
    forecast_title = f"GDP Forecast for {get_quarter(selected_date)}:"


    return display_text, forecast_value, forecast_style, figure, forecast_title
