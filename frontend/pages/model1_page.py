import dash
from dash import html, dcc, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from shared.default_pagelayout import get_default_layout 
import requests
import json

# Register the Model 1 page
dash.register_page(__name__, path="/model1", name="Model 1")

# Sample data for the graph
years = [f"{year}Q{q}" for year in range(1950, 2026) for q in range(1, 5)]
values = [1000 * (1.03 ** (int(year.split('Q')[0]) - 1950)) for year in years]  # Simulated Real GDP growth

df = pd.DataFrame({"Year": years, "Real GDP": values})

# Content for Model 1 page
model1_content = html.Div(
    id="main-content",
    children=[
        html.Br(), 
        # Header "Model 1"
        html.H1("Model 1", style={"margin-left": "75px", "color": "white", "marginBottom": "20px"}),

        # Container for the graph and input fields
        html.Div([
            # Graph on the left
            dcc.Graph(id='model1-graph', style={"margin-left": "50px", "flex": "3", "height": "500px"}),

            # Input fields on the right
            html.Div([
                html.Label("End year:", style={"margin-right": "25px", "text-align": "left", "color": "white", "fontSize": "16px", "marginBottom": "5px"}),
                dcc.Input(
                    id='end-year-input',
                    type='text',
                    placeholder='End year (e.g., 2025Q1)',
                    value='2025Q1',
                    style={"margin-right": "25px", "width": "150px", "height": "40px", "padding": "5px", "fontSize": "16px"}
                )
            ], style={"display": "flex", "flexDirection": "column", "alignItems": "center", "marginLeft": "20px"})
        ], style={"margin-left": "75px", "display": "flex", "alignItems": "center", "justifyContent": "center"}),

        # Header "Model Description"
        html.H2("Model Description", style={"margin-left": "75px", "color": "white", "marginTop": "30px"}),

        # Description text
        html.P("This model represents a sample visualization of economic trends over time. The graph above updates dynamically based on the selected year range.",
               style={"margin-left": "75px", "color": "white", "textAlign": "left", "width": "100%"}
        )
    ]
)

# Plug that content into your default layout
layout = get_default_layout(main_content=model1_content)

# Callback to update the graph
@dash.callback(
    Output('model1-graph', 'figure'),
    Input('end-year-input', 'value')
)
def update_graph(end_year):

    headers = {'Content-Type': 'application/json'}
    response = requests.post("http://127.0.0.1:5000/mean_model_user_input", headers = headers, data = json.dumps({"date": end_year}))
    data = response.json()

    fig = px.line(pd.DataFrame.from_dict(data), x = "quarters", y = "pct_chg", color = "Indicator", title = "Real GDP Percentage Change Over Time")
    return fig

    # if end_year not in df['Year'].values:
    #     return px.line(df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    
    # end_index = df[df['Year'] == end_year].index[0] + 1
    # filtered_df = df.iloc[:end_index]
    # fig = px.line(filtered_df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    # return fig

