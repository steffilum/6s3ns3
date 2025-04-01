import dash
from dash import html, dcc, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from shared.default_pagelayout import get_default_layout 

# Register the Model 2 page
dash.register_page(__name__, path="/model2", name="Model 2")

# Sample data for the graph
years = [f"{year}Q{q}" for year in range(1950, 2026) for q in range(1, 5)]
values = [1000 * (1.03 ** (int(year.split('Q')[0]) - 1950)) for year in years]  # Simulated Real GDP growth

df = pd.DataFrame({"Year": years, "Real GDP": values})

# Content for Model 2 page
model2_content = html.Div(
    id="main-content",
    children=[
        html.Br(), 
        # Header "Model 2"
        html.H1("Model 2", style={"margin-left": "75px", "color": "white", "marginBottom": "20px"}),

        # Container for the graph and input fields
        html.Div([
            # Graph on the left
            dcc.Graph(id='model2-graph', style={"margin-left": "50px", "flex": "3", "height": "500px"}),

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
layout = get_default_layout(main_content=model2_content)

# Callback to update the graph
@dash.callback(
    Output('model2-graph', 'figure'),
    Input('end-year-input', 'value')
)
def update_graph(end_year):
    if end_year not in df['Year'].values:
        return px.line(df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    
    end_index = df[df['Year'] == end_year].index[0] + 1
    filtered_df = df.iloc[:end_index]
    fig = px.line(filtered_df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    return fig

