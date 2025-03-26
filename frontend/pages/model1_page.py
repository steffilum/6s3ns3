import dash
from dash import html, dcc, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Register the Model 1 page
dash.register_page(__name__, path="/model1", name="Model 1")

# Sample data for the graph
years = [f"{year}Q{q}" for year in range(1950, 2026) for q in range(1, 5)]
values = [1000 * (1.03 ** (int(year.split('Q')[0]) - 1950)) for year in years]  # Simulated Real GDP growth

df = pd.DataFrame({"Year": years, "Real GDP": values})

# Layout for Model 1 page
layout = html.Div(
    children=[
        html.H1("Model 1", style={"textAlign": "center", "color": "white"}),
        html.Div([
            dcc.Graph(id='model1-graph', style={"flex": "3"}),
            html.Div([
                dcc.Input(
                    id='start-year-input',
                    type='text',
                    placeholder='Start year (e.g., 2000Q1)',
                    value='1950Q1',
                    style={"marginRight": "10px", "height": "40px", "padding": "5px", "fontSize": "16px"}
                ),
                dcc.Input(
                    id='end-year-input',
                    type='text',
                    placeholder='End year (e.g., 2025Q1)',
                    value='2025Q1',
                    style={"height": "40px", "padding": "5px", "fontSize": "16px"}
                )
            ], style={"display": "flex", "alignItems": "center", "marginLeft": "20px"})
        ], style={"display": "flex", "alignItems": "center"}),
        html.H2("Model Description", style={"textAlign": "center", "color": "white", "marginTop": "20px"}),
        html.P("This model represents a sample visualization of economic trends over time. The graph above updates dynamically based on the selected year range.",
               style={"color": "white", "textAlign": "center"})
    ]
)

# Callback to update the graph
@dash.callback(
    Output('model1-graph', 'figure'),
    Input('start-year-input', 'value'),
    Input('end-year-input', 'value')
)
def update_graph(start_year, end_year):
    if start_year not in df['Year'].values or end_year not in df['Year'].values:
        return px.line(df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    
    start_index = df[df['Year'] == start_year].index[0]
    end_index = df[df['Year'] == end_year].index[0] + 1
    filtered_df = df.iloc[start_index:end_index]
    fig = px.line(filtered_df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    return fig
