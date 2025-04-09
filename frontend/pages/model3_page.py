import dash
from dash import html, dcc, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from shared.default_pagelayout import get_default_layout 
import requests
import json

# Register the Model 3 page
dash.register_page(__name__, path="/model3", name="Model 3")

# Sample data for the graph
# years = [f"{year}Q{q}" for year in range(1950, 2026) for q in range(1, 5)]
# values = [1000 * (1.03 ** (int(year.split('Q')[0]) - 1950)) for year in years]  # Simulated Real GDP growth

# df = pd.DataFrame({"Year": years, "Real GDP": values})

# Content for Model 3 page
model3_content = html.Div(
    id="main-content",
    style={
        "height": "100vh",           # Full height of the viewport    
        "overflowY": "scroll",          # Enable vertical scrolling
        "paddingTop": "25px",         # some space at the top
        "paddingBottom": "200px"        # some space at the bottom
    },     
    children=[
        # Header "Model 3"
        html.H1("Mixed Data Sampling (MIDAS) Model", style={"text-align": "center","color": "white", "marginBottom": "20px"}),

        # Graph Centered
        dcc.Graph(id='model3-graph', style={"text-align": "center", "width": "80%", "margin": "0 auto", "height": "500px"}),

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

        html.P("MIDAS models, like bridge models, are also used to address the mismatch in data frequency between economic indicators and target variables such as GDP. \
               However, our MIDAS model forecast directly incorporates the higher-frequency monthly economic indicators into the forecasting process without requiring an aggregation to a quarterly frequency. \
               This allows the model more freedom to set the relationship between monthly lags instead of taking a fixed aggregation. \
               The final regression model structure estimates the quarterly GDP by using monthly indicator values as separate regressors, in conjunction with quarterly government spending on defence and a lag of quarterly GDP. \
               Like the bridge model, OLS is also used to determine the coefficients of the regression model.",
        style={"color": "white", "width": "80%", "margin": "0 auto", "marginBottom": "10px"}
        )
    ]
)


# Plug that content into your default layout
layout = get_default_layout(main_content=model3_content)

# Callback to update the graph
@dash.callback(
    Output('model3-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_graph(year, month):
    ## DO NOT DELETE -- CODE FOR INTEGRATION
    response = requests.post("http://127.0.0.1:5000/midas_model_prediction", 
                             headers = {'Content-Type': 'application/json'}, 
                             data = json.dumps({"year": year, "month": month}))
    data = response.json()
    data = pd.DataFrame.from_dict(data)
    data = data.reset_index().rename(columns = {"index": "Quarter"})

    ## Tentative Graph Plotting Code

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

    # Create a target year from the selected year and month
    # target_year = f"{year}Q{['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(month) + 1}"
    
    # if target_year not in df['Year'].values:
    #     return px.line(df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    
    # end_index = df[df['Year'] == target_year].index[0] + 1
    # filtered_df = df.iloc[:end_index]
    # fig = px.line(filtered_df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    # return fig
