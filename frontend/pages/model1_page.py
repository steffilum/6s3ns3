import dash
from dash import html, dcc, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from shared.default_pagelayout import get_default_layout 
import requests
import json
import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()

# Register the Model 1 page
dash.register_page(__name__, path="/model1", name="Model 1")

# Sample data for the graph
# years = [f"{year}Q{q}" for year in range(1950, 2026) for q in range(1, 5)]
# values = [1000 * (1.03 ** (int(year.split('Q')[0]) - 1950)) for year in years]  # Simulated Real GDP growth

# df = pd.DataFrame({"Year": years, "Real GDP": values})

# Content for Model 1 page
model1_content = html.Div(
    id="main-content",
    style={
        "height": "100vh",           # Full height of the viewport    
        "overflowY": "scroll",          # Enable vertical scrolling
        "paddingTop": "25px",         # some space at the top
        "paddingBottom": "200px"        # some space at the bottom
    },     
    children=[
        # Header "Model 1"
        html.H1("Prevailing Mean Benchmark Model", style={"text-align": "center","color": "white", "marginBottom": "20px"}),

        # Graph Centered
        dcc.Graph(id='model1-graph', style={"text-align": "center", "width": "80%", "margin": "0 auto", "height": "500px"}),

        html.Br(), 

        # Dropdowns for year and month
        html.Div([
            # Year dropdown
            html.Div([
                html.Label("Select Year:", style={"color": "white", "fontSize": "16px", "marginBottom": "5px"}),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': str(year)} for year in range(2000, 2026)],
                    value='2025',
                    style={"color":"black", "width": "150px", "fontSize": "16px"}
                ),
            ], style={"margin": "10px"}),

            # Month dropdown
            html.Div([
                html.Label("Select Month:", style={"color": "white", "fontSize": "16px", "marginBottom": "5px"}),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': month, 'value': month} for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']],
                    value='Dec',
                    style={"color": "black", "width": "150px", "fontSize": "16px"}
                ),
            ], style={"margin": "10px"})
        ], style={"display": "flex", "justifyContent": "center", "alignItems": "center"}),

        html.Br(),

        # Model Description
        html.H2("Model Description", style={"text-align": "center", "color": "white", "marginTop": "30px"}),

        html.P("This model takes the prevailing arithmetic mean of GDP for all past quarters and that would be the prediction for GDP in the next quarter. \
               We can see that the predictions tend to fall above the real values in evaluation test data, likely due to the fact GDP growth figures are greater \
               in periods of growth during the industrial revolution as compared to more steady growth in the 2000s. One main con of this model would be the inability to predict recessions as they are few and far between.",
        style={"color": "white", "width": "80%", "margin": "0 auto"}
        )
    ]
)

# Plug that content into your default layout
layout = get_default_layout(main_content=model1_content)

# Callback to update the graph
@dash.callback(
    Output('model1-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_graph(year, month):
    ## DO NOT DELETE -- CODE FOR INTEGRATION
    response = requests.post("http://127.0.0.1:5000/mean_model_prediction", 
                             headers = {'Content-Type': 'application/json'}, 
                             data = json.dumps({"year": year, "month": month}))
    data = response.json()
    data = pd.DataFrame.from_dict(data)
    data = data.reset_index().rename(columns = {"index": "Quarter"})

    fig = px.line(data, 
                  x = "Quarter", 
                  y = ["Actual GDP", "Predicted GDP"], 
                  color_discrete_sequence = ["black", "red"])
    
    # customisation
    fig.update_layout(
        legend_title_text = "Legend",
        xaxis_title_text = "Year and Quarter",
        yaxis_title= "GDP Growth"
    )
    
    return fig

    # ## Tentative Graph Plotting Code

    # fig = px.line(pd.DataFrame.from_dict(data), x = "quarters", y = "pct_chg", color = "Indicator", title = "Real GDP Percentage Change Over Time")
    # return fig
 
    # # Create a target year from the selected year and month
    # target_year = f"{year}Q{['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(month) + 1}"
    
    # if target_year not in df['Year'].values:
    #     return px.line(df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    
    # end_index = df[df['Year'] == target_year].index[0] + 1
    # filtered_df = df.iloc[:end_index]
    # fig = px.line(filtered_df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    # return fig
