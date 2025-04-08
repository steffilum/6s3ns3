import dash
from dash import html, dcc, Input, Output, State, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from shared.default_pagelayout import get_default_layout 
import requests
import json
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()


# Register the Model 4 page
dash.register_page(__name__, path="/model4", name="Model 4")

# Sample data for the graph
# years = [f"{year}Q{q}" for year in range(1950, 2026) for q in range(1, 5)]
# values = [1000 * (1.03 ** (int(year.split('Q')[0]) - 1950)) for year in years]  # Simulated Real GDP growth

# df = pd.DataFrame({"Year": years, "Real GDP": values})

# Content for Model 4 page
model4_content = html.Div(
    id="main-content",
    style={
        "height": "100vh",           # Full height of the viewport    
        "overflowY": "scroll",          # Enable vertical scrolling
        "paddingTop": "25px",         # some space at the top
        "paddingBottom": "200px"        # some space at the bottom
    },     
    children=[
        # Header "Model 4"
        html.H1("Bridge Model", style={"text-align": "center","color": "white", "marginBottom": "20px"}),

        # Graph Centered
        dcc.Graph(id='model4-graph', style={"text-align": "center", "width": "80%", "margin": "0 auto", "height": "500px"}),

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

        html.P("Bridge Models are used to address the mismatch in data frequency between economic indicators and target variables like GDP. ",
        style={"color": "white", "width": "80%", "margin": "0 auto", "marginBottom": "10px"}
        ),

        html.P("Our bridge model forecast is constructed by aggregating the 11 economic indicators that were selected as proxies for each subcomponent of GDP. \
               Since most of these indicators are monthly data, we make one- to three- step-ahead predictions depending on the input month within the quarter. \
               For example, if the input month is the first of the quarter, we will forecast 3 months ahead; for the second month, 2 months ahead; and for the last month; only one month ahead. \
               We aggregate each of the monthly actuals and/or forecasts to produce a quarterly value. These are calculated in each of the economic indicators code files. \
               The resulting quarterly data, along with the addition of a lag of quarterly GDP, are then used as regressors in our bridge model. \
               The bridge model itself is a linear regression that estimates the quarter GDP using ordinary least squares (OLS)...",
        style={"color": "white", "width": "80%", "margin": "0 auto", "marginBottom": "10px"}
        ),

        html.P("Our first constructed model would attempt to follow the GDPNow model as mentioned in the GDPNow working paper where they used a bridge model for the nowcasting of GDP. \
               Firstly, we identify the main components in GDP, mainly C, I, G, X and M as well as other indicators like Sahm’s rule. \
               Then we would aggregate them up to quarterly percentage changes and subsequently use a larger OLS as our bridge models. \
               For each of our components, we would transform our data based on the recommendation on FRED if available, we would then test for stationarity with a constant. \
               If stationary, we would assume an ARMA model and plot the ACF and PACF in order to try to find a range of optimal parameters. Next, we would do a grid search to find the optimal values of p and q in the model. \
               Subsequently, we would predict the required data until the end of the quarter to be forecasted subsequently we would aggregate the data into the quarters to link in our larger model. ",
        style={"color": "white", "width": "80%", "margin": "0 auto", "marginBottom": "10px"}
        ),

         html.P("In the larger model we simply use OLS of all the predictors including a lag of GDP to account for the effect of GDP last quarter to today.",
        style={"color": "white", "width": "80%", "margin": "0 auto"}
        )
    ]
)


# Plug that content into your default layout
layout = get_default_layout(main_content=model4_content)

# Callback to update the graph
@dash.callback(
    Output('model4-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_graph(year, month):
    ## DO NOT DELETE -- CODE FOR INTEGRATION
    response = requests.post("http://127.0.0.1:5000/bridge_model_prediction", 
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

    # Create a target year from the selected year and month
    # target_year = f"{year}Q{['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(month) + 1}"
    
    # if target_year not in df['Year'].values:
    #     return px.line(df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    
    # end_index = df[df['Year'] == target_year].index[0] + 1
    # filtered_df = df.iloc[:end_index]
    # fig = px.line(filtered_df, x='Year', y='Real GDP', title="Real GDP Growth Over Time")
    # return fig
