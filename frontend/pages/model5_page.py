import dash
from dash import html, dcc, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from shared.default_pagelayout import get_default_layout 
import requests
import json

# Register the Model 5 page
dash.register_page(__name__, path="/model5", name="Model 5")

# Sample data for the graph
years = [f"{year}Q{q}" for year in range(1950, 2026) for q in range(1, 5)]
values = [1000 * (1.03 ** (int(year.split('Q')[0]) - 1950)) for year in years]  # Simulated Real GDP growth

df = pd.DataFrame({"Year": years, "Real GDP": values})

# Content for Model 5 page
model5_content = html.Div(
    id="main-content",
    children=[
        html.Br(), 
        # Header "Model 5"
        html.H1("Model 5", style={"margin-left": "75px", "color": "white", "marginBottom": "20px"}),

        # Container for the graph and input fields
        html.Div([
            # Graph on the left
            dcc.Graph(id='model5-graph', style={"margin-left": "50px", "flex": "3", "height": "500px"}),

            # Input fields on the right
            html.Div([
                # year dropdown
                html.Label("Select year:", style={"margin-right": "25px", "text-align": "left", "color": "white", "fontSize": "16px", "marginBottom": "5px"}),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label' : str(year), 'value': str(year)} for year in range(2000,2026)],
                    value='2025', # default value
                    style={ "width": "150px", "height": "40px", "fontSize": "16px"}
                ),
                # month dropdown
                html.Label("Select Month:", style={"margin-right": "25px", "text-align": "left", "color": "white", "fontSize": "16px", "marginBottom": "5px"}),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label' : str(month), 'value': str(month)} for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']],
                    value='Dec', #default value
                    style={ "width": "150px", "height": "40px", "fontSize": "16px"}
                ),
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
layout = get_default_layout(main_content=model5_content)

# Callback to update the graph
@dash.callback(
    Output('model5-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_graph(year, month):
    # ## DO NOT DELETE -- CODE FOR INTEGRATION
    # response = requests.post("http://127.0.0.1:5000/mean_model_user_input", 
    #                          headers = {'Content-Type': 'application/json'}, 
    #                          data = json.dumps({"year": year, "month": month}))
    # data = response.json()

    # ## Tentative Graph Plotting Code

    # fig = px.line(pd.DataFrame.from_dict(data), x = "quarters", y = "pct_chg", color = "Indicator", title = "Real GDP Percentage Change Over Time")
    # return fig
    # Create a target year from the selected year and month
    target_year = f"{year}Q{['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(month) + 1}"
    
    if target_year not in df['Year'].values:
        return px.line(df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    
    end_index = df[df['Year'] == target_year].index[0] + 1
    filtered_df = df.iloc[:end_index]
    fig = px.line(filtered_df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    return fig
