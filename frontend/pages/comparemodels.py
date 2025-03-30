import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.stats import norm
from shared.default_pagelayout import get_default_layout

#link page to homepage
dash.register_page(__name__, path="/comparemodels", name="Compare Models")

# Mock Data
model1 = pd.DataFrame({"Year": [str(y) for y in range(2010, 2020)], "GDP": [15, 10, 20, 30, 35, 22, 8, 4, 23, 31]})
model2 = pd.DataFrame({"Year": [str(y) for y in range(2010, 2020)], "GDP": [20, 31, 54, 23, 43, 12, 25, 12, 4, 3]})
model3 = pd.DataFrame({"Year": [str(y) for y in range(2010, 2020)], "GDP": [12, 18, 33, 28, 39, 25, 19, 11, 6, 15]})
model4 = pd.DataFrame({"Year": [str(y) for y in range(2010, 2020)], "GDP": [33, 34, 23, 12, 39, 43, 12, 4, 6, 31]})


# Forecast values for each model
forecast_values = {
   "Model 1": 1.7,
   "Model 2": -0.5,
   "Model 3": 0,
   "Model 4": 28
}


# Evaluation Metric mock values
rmse_values = {
   "Model 1": 2.2,
   "Model 2": 1.8,
   "Model 3": 5.0,
   "Model 4": 6.7
}


mae_values = {
   "Model 1": 3.4,
   "Model 2": 1.1,
   "Model 3": 0.9,
   "Model 4": 2.5
}


da_values = {
   "Model 1": 8.7,
   "Model 2": 2.4,
   "Model 3": 0.02,
   "Model 4": 10.7
}


dmtest_values = {
   "DM Statistic": 2.34,
   "p-value": 0.02
}


# Larger Mock Data for Models (use actual model predictions here)
model1_y_true = np.array([3.1, 2.9, 3.0, 3.2, 2.8, 3.0, 3.1, 2.9, 3.2, 2.7])  # True values for Model 1
model1_y_pred = np.array([3.0, 2.8, 3.1, 3.3, 2.9, 3.0, 3.1, 2.8, 3.2, 2.7])  # Predicted values for Model 1
model2_y_true = np.array([2.8, 3.0, 3.1, 2.7, 3.0, 3.2, 3.1, 3.0, 2.9, 3.0])  # True values for Model 2
model2_y_pred = np.array([2.7, 3.1, 3.0, 2.8, 3.1, 3.2, 3.0, 3.1, 2.8, 3.0])  # Predicted values for Model 2
model3_y_true = np.array([3.5, 3.3, 3.6, 3.8, 3.7, 3.6, 3.5, 3.4, 3.6, 3.5])  # True values for Model 3
model3_y_pred = np.array([3.6, 3.5, 3.7, 3.9, 3.8, 3.7, 3.6, 3.6, 3.8, 3.7])  # Predicted values for Model 3
model4_y_true = np.array([4.1, 4.2, 4.3, 4.5, 4.6, 4.5, 4.4, 4.3, 4.5, 4.6])  # True values for Model 4
model4_y_pred = np.array([4.0, 4.1, 4.2, 4.4, 4.5, 4.4, 4.3, 4.2, 4.4, 4.5])  # Predicted values for Model 4


# Function to compute bootstrap confidence intervals for RMSE
def bootstrap_rmse(y_true, y_pred, n_iterations=1000, ci=95):
   rmse_values = []
   for _ in range(n_iterations):
       indices = np.random.choice(len(y_true), len(y_true), replace=True)
       y_true_bs = y_true[indices]
       y_pred_bs = y_pred[indices]
       rmse = np.sqrt(np.mean((y_true_bs - y_pred_bs) ** 2))
       rmse_values.append(rmse)
   lower = np.percentile(rmse_values, (100 - ci) / 2)
   upper = np.percentile(rmse_values, 100 - (100 - ci) / 2)
   return lower, upper


# Function to compute bootstrap confidence intervals for MAE
def bootstrap_mae(y_true, y_pred, n_iterations=1000, ci=95):
   mae_values = []
   for _ in range(n_iterations):
       indices = np.random.choice(len(y_true), len(y_true), replace=True)
       y_true_bs = y_true[indices]
       y_pred_bs = y_pred[indices]
       mae = np.mean(np.abs(y_true_bs - y_pred_bs))
       mae_values.append(mae)
   lower = np.percentile(mae_values, (100 - ci) / 2)
   upper = np.percentile(mae_values, 100 - (100 - ci) / 2)
   return lower, upper

# Function to compute bootstrap confidence intervals for DA
def bootstrap_da(y_true, y_pred, n_iterations=1000, ci=95):
   da_values = []
   for _ in range(n_iterations):
       indices = np.random.choice(len(y_true), len(y_true), replace=True)
       y_true_bs = y_true[indices]
       y_pred_bs = y_pred[indices]
       correct_direction = np.sum(np.sign(y_true_bs) == np.sign(y_pred_bs))
       da = correct_direction / len(y_true_bs)
       da_values.append(da)
   lower = np.percentile(da_values, (100 - ci) / 2)
   upper = np.percentile(da_values, 100 - (100 - ci) / 2)
   return lower, upper

##mock function to compute dm test, eventually provided by backend
def diebold_mariano_test(errors1, errors2):
   # Ensure that the errors are numerical
   errors1 = np.array(errors1, dtype=float)  # Convert to float
   errors2 = np.array(errors2, dtype=float)  # Convert to float


   # Calculate the loss differential (d_t = error_model1 - error_model2)
   d_t = errors1 - errors2
  
   # Mean of the loss differential
   d_bar = np.mean(d_t)
  
   # Standard deviation of the loss differential
   std_d = np.std(d_t) / np.sqrt(len(d_t))
  
   # Compute the DM statistic
   dm_statistic = d_bar / std_d
  
   # Compute the p-value using the standard normal distribution
   p_value = 2 * (1 - norm.cdf(abs(dm_statistic)))  # Two-tailed test
  
   return dm_statistic, p_value

# List of figures for each model
figures = [
   px.line(model1, x='Year', y='GDP', title='Model 1: GDP Forecast'),
   px.line(model2, x='Year', y='GDP', title='Model 2: GDP Forecast'),
   px.line(model3, x='Year', y='GDP', title='Model 3: GDP Forecast'),
   px.line(model4, x='Year', y='GDP', title='Model 4: GDP Forecast'),
]

# Helper functions for styling
def get_dropdown_style():
    return {
        "backgroundColor": "transparent",  # clear background
        "fontWeight": "bold",                # bold text inside the input
        "color": "white",                   # white text color
        "padding": "5px"
    }

def get_dropdown_menu_style():
    return {
        "backgroundColor": "transparent",  # clear background for the dropdown list
        "fontWeight": "bold",               # bold text for options
        "color": "white",                   # white text color for options
    }

# LAYOUT
comparemodels_content = html.Div(id="main-content",children=[
   html.H1("Compare NowCast Models", style={'text-align': 'center', 'color':'white'}),

   # Start and end date inputs
   html.Div([
       dcc.Input(id="start_date", type="number", placeholder="Enter Start Date"), #can use regex output later on
       dcc.Input(id="end_date", type="number", placeholder="Enter End Date"),
   ], style={'text-align': 'center', 'margin-bottom': '20px'}),

   # Dropdown and Graph for Model 1
   html.Div([
       dcc.Dropdown(
           id="model_title1",
           options=[{'label': f'Model {i}', 'value': f'Model {i}'} for i in range(1, 5)],
           placeholder="Select Model 1",
           style=get_dropdown_style()
       ),
       html.H4("GDP Forecast Next Quarter:", style={'color':'white'}),
       html.Div(id='forecast_output_1', style={"fontWeight": "bold", "fontSize": "24px"}),
       dcc.Graph(id='graph_1'),
   ], style={'display': 'inline-block', 'width': '48%'}),


   # Dropdown and Graph for Model 2
   html.Div([
       dcc.Dropdown(
           id="model_title2",
           options=[{'label': f'Model {i}', 'value': f'Model {i}'} for i in range(1, 5)],
           placeholder="Select Model 2",
           style=get_dropdown_style()
       ),
       html.H4("GDP Forecast Next Quarter:", style={'color':'white'}),
       html.Div(id='forecast_output_2', style={"fontWeight": "bold", "fontSize": "24px"}),
       dcc.Graph(id='graph_2'),
   ], style={'display': 'inline-block', 'width': '48%', 'marginLeft': '2%'}),


   # Evaluation Section
   html.H1("Evaluation", style={'color':'white'}),
   html.Div(style={'borderTop': '2px solid black', 'margin': '20px 0', 'color':'white'}),
  
   # Dropdown for Evaluation Metric
   html.Div([
       dcc.Dropdown(
           id="evaluation_metric",
           options=[
               {'label': 'Root Mean Squared Error (RMSE)', 'value': 'rmse'},
               {'label': 'Mean Absolute Error (MAE)', 'value': 'mae'},
               {'label': 'Directional Accuracy (DA)', 'value': 'da'}
           ],
           placeholder='Select Evaluation Metric',
           style=get_dropdown_style()
       )
   ], style={'width': '50%', 'marginBottom': '20px'}),
  
   # Display Evaluation Metric for Model 1
   html.Div(id="evaluation_metric1", style={'display': 'inline-block','fontSize': '20px', 'width': '48%', 'color':'white'}),
  
   # Display Evaluation Metric for Model 2
   html.Div(id="evaluation_metric2", style={'display': 'inline-block','fontSize': '20px', 'width': '48%', 'color':'white'}),

   #Display CI for Model 1
   html.Div([
       dcc.Graph(id="confidence_interval_vis1"),
       html.H4("95% Confidence Interval")],
       style={'text-align':'center', 'marginTop':'30px', 'display': 'inline-block','fontSize': '20px', 'width': '48%'}),
  
   #Display CI for Model 2
   html.Div([
       dcc.Graph(id="confidence_interval_vis2"),
       html.H4("95% Confidence Interval")],
       style={'text-align':'center', 'marginTop':'30px', 'display': 'inline-block','fontSize': '20px', 'width': '48%'}),


   #Display DM Test Values
   html.Div(id="dm_test_results", style={'display': 'inline-block','fontSize': '20px', 'text-align':'center', 'width':'100%', 'color':'white'}),
],
style={
       'height': '100vh',
       'overflowY': 'scroll',  # Enable scrolling
       'paddingTop': "100px", #Leave space on top for nav bar 
       'paddingBottom': '20px' #bottom padding
   })

# Plug that content into your default layout
layout = get_default_layout(main_content= comparemodels_content)

##CALLBACKS
# Callback for Model 1: Update graph and forecast with date filtering
@dash.callback(
   [Output('graph_1', 'figure'),
    Output('forecast_output_1', 'children')],
   [Input('model_title1', 'value'),
    Input('start_date', 'value'),
    Input('end_date', 'value')]
)
def update_graph_and_forecast_1(model_name, start_date, end_date):
   if model_name:
       model_df = {
           "Model 1": model1,
           "Model 2": model2,
           "Model 3": model3,
           "Model 4": model4
       }[model_name]
      
       # Filter by start and end date if provided
       if start_date and end_date:
           model_df = model_df[(model_df['Year'].astype(int) >= start_date) & (model_df['Year'].astype(int) <= end_date)]
      
       # Generate the figure for the selected model and filtered data
       fig = px.line(model_df, x='Year', y='GDP', title=f'{model_name}: GDP Forecast')
       forecast = forecast_values.get(model_name, 0)
       return fig, format_forecast(forecast)
  
   return {}, ""


# Callback for Model 2: Update graph and forecast with date filtering
@dash.callback(
   [Output('graph_2', 'figure'),
    Output('forecast_output_2', 'children')],
   [Input('model_title2', 'value'),
    Input('start_date', 'value'),
    Input('end_date', 'value')]
)
def update_graph_and_forecast_2(model_name, start_date, end_date):
   if model_name:
       model_df = {
           "Model 1": model1,
           "Model 2": model2,
           "Model 3": model3,
           "Model 4": model4
       }[model_name]
      
       if start_date and end_date:
           model_df = model_df[(model_df['Year'].astype(int) >= start_date) & (model_df['Year'].astype(int) <= end_date)]
      
       fig = px.line(model_df, x='Year', y='GDP', title=f'{model_name}: GDP Forecast')
       forecast = forecast_values.get(model_name, 0)
       return fig, format_forecast(forecast)
  
   return {}, ""


# Function to format forecast with color (green for positive, red for negative)
def format_forecast(forecast):
   color = "green" if forecast > 0 else "red" if forecast < 0 else "black"
   sign = "+" if forecast > 0 else "-" if forecast < 0 else ""
   return html.Span(f"{sign}{abs(forecast)}%", style={"color": color})


# Callback for evaluation metric 1
@dash.callback(
   Output('evaluation_metric1', 'children'),
   [Input('model_title1', 'value'),
    Input('evaluation_metric', 'value')]
)
def update_eval_metric(model, metric):
   if model and metric:
       # Fetch the appropriate evaluation metric value based on selection
       if metric == 'rmse':
           eval_metric = rmse_values.get(model, "Not Available")
       elif metric == 'mae':
           eval_metric = mae_values.get(model, "Not Available")
       elif metric == 'da':
           eval_metric = da_values.get(model, "Not Available")


       # Return the metric and model name on separate lines with different styles
       return html.Div([
       html.Div(f'{eval_metric}%', style={"fontSize": "36px", "fontWeight": "bold"}),
       html.Div(f'{metric.upper()} for {model}', style={"fontSize": "18px", "fontWeight": "normal"}),
       ], style={'width': '50%', 'text-align':'center', 'margin': '0 auto'}) 




   return "Select a model and metric to display the evaluation result."


# Callback for evaluation metric 2
@dash.callback(
   Output('evaluation_metric2', 'children'),
   [Input('model_title2', 'value'),
    Input('evaluation_metric', 'value')]
)
def update_eval_metric(model, metric):
   if model and metric:
       # Fetch the appropriate evaluation metric value based on selection
       if metric == 'rmse':
           eval_metric = rmse_values.get(model, "Not Available")
       elif metric == 'mae':
           eval_metric = mae_values.get(model, "Not Available")
       elif metric == 'da':
           eval_metric = da_values.get(model, "Not Available")


       # Return the metric and model name on separate lines with different styles
       return html.Div([
       html.Div(f'{eval_metric}%', style={"fontSize": "36px", "fontWeight": "bold"}),
       html.Div(f'{metric.upper()} for {model}', style={"fontSize": "18px", "fontWeight": "normal"}),
       ], style={'width': '50%', 'text-align':'center', 'margin': '0 auto'}) 


   return "Select a model and metric to display the evaluation result."


#Callback to update confidence interval visualisation 1
@dash.callback(
   Output('confidence_interval_vis1', 'figure'),
   [Input('model_title1', 'value'),
    Input('evaluation_metric', 'value')]
)


def update_confidence_interval_graph(selected_model, selected_metric):
   # Default initialization in case of an error
   y_true, y_pred = None, None
   # Choose the correct true and predicted values based on the selected model
   if selected_model == 'Model 1':
       y_true = model1_y_true
       y_pred = model1_y_pred
   elif selected_model == 'Model 2':
       y_true = model2_y_true
       y_pred = model2_y_pred
   elif selected_model == 'Model 3':
       y_true = model3_y_true
       y_pred = model3_y_pred
   elif selected_model == 'Model 4':
       y_true = model4_y_true
       y_pred = model4_y_pred


   # If no model is selected, raise an error or return a message
   if y_true is None or y_pred is None:
       return go.Figure()  # Or return some default figure, or an error message


   # Get the confidence interval based on the selected metric
   if selected_metric == 'rmse':
       lower, upper = bootstrap_rmse(y_true, y_pred, n_iterations=1000, ci=95)
       metric_name = 'RMSE'
   elif selected_metric == 'mae':
       lower, upper = bootstrap_mae(y_true, y_pred, n_iterations=1000, ci=95)
       metric_name = 'MAE'
   elif selected_metric == 'da':
       lower, upper = bootstrap_da(y_true, y_pred, n_iterations=1000, ci=95)
       metric_name = 'Directional Accuracy'
  
   # Compute the point estimate (mean of the CI)
   point_value = np.mean([lower, upper])


   # Create the Plotly figure for the confidence interval
   fig = go.Figure()


   # Add the central point (estimate)
   fig.add_trace(go.Scatter(
       x=[0], y=[point_value],
       mode='markers',
       marker=dict(size=12, color='white'),
       name=f"{metric_name} Estimate"
   ))


   # Add the horizontal error bar (Confidence Interval)
   fig.add_trace(go.Scatter(
       x=[0], y=[point_value],
       mode='lines',
       line=dict(width=3, color='white'),
       error_x=dict(type='data', symmetric=False, array=[upper - point_value], arrayminus=[point_value - lower]),
       name=f"{metric_name} CI"
   ))


   # Update layout for better visualization
   fig.update_layout(
       title=f"95% Confidence Interval for {metric_name}",
       xaxis=dict(
           showgrid=False,
           zeroline=False,
           showticklabels=False
       ),
       yaxis=dict(
           title=f"{metric_name} Value",
           showgrid=True,
           zeroline=False
       ),
       plot_bgcolor='black',  # Dark background
       showlegend=True,
       margin=dict(l=50, r=50, t=50, b=50)
   )


   return fig


#Callback to update confidence interval visualisation 2
@dash.callback(
   Output('confidence_interval_vis2', 'figure'),
   [Input('model_title2', 'value'),
    Input('evaluation_metric', 'value')]
)


def update_confidence_interval_graph(selected_model, selected_metric):
   # Default initialization in case of an error
   y_true, y_pred = None, None
   # Choose the correct true and predicted values based on the selected model
   if selected_model == 'Model 1':
       y_true = model1_y_true
       y_pred = model1_y_pred
   elif selected_model == 'Model 2':
       y_true = model2_y_true
       y_pred = model2_y_pred
   elif selected_model == 'Model 3':
       y_true = model3_y_true
       y_pred = model3_y_pred
   elif selected_model == 'Model 4':
       y_true = model4_y_true
       y_pred = model4_y_pred
  
   # If no model is selected, raise an error or return a message
   if y_true is None or y_pred is None:
       return go.Figure()  # Or return some default figure, or an error message


   # Get the confidence interval based on the selected metric
   if selected_metric == 'rmse':
       lower, upper = bootstrap_rmse(y_true, y_pred, n_iterations=1000, ci=95)
       metric_name = 'RMSE'
   elif selected_metric == 'mae':
       lower, upper = bootstrap_mae(y_true, y_pred, n_iterations=1000, ci=95)
       metric_name = 'MAE'
   elif selected_metric == 'da':
       lower, upper = bootstrap_da(y_true, y_pred, n_iterations=1000, ci=95)
       metric_name = 'Directional Accuracy'
  
   # Compute the point estimate (mean of the CI)
   point_value = np.mean([lower, upper])


   # Create the Plotly figure for the confidence interval
   fig = go.Figure()


   # Add the central point (estimate)
   fig.add_trace(go.Scatter(
       x=[0], y=[point_value],
       mode='markers',
       marker=dict(size=12, color='white'),
       name=f"{metric_name} Estimate"
   ))


   # Add the horizontal error bar (Confidence Interval)
   fig.add_trace(go.Scatter(
       x=[0], y=[point_value],
       mode='lines',
       line=dict(width=3, color='white'),
       error_x=dict(type='data', symmetric=False, array=[upper - point_value], arrayminus=[point_value - lower]),
       name=f"{metric_name} CI"
   ))


   # Update layout for better visualization
   fig.update_layout(
       title=f"95% Confidence Interval for {metric_name}",
       xaxis=dict(
           showgrid=False,
           zeroline=False,
           showticklabels=False
       ),
       yaxis=dict(
           title=f"{metric_name} Value",
           showgrid=True,
           zeroline=False
       ),
       plot_bgcolor='black',  # Dark background
       showlegend=True,
       margin=dict(l=50, r=50, t=50, b=50)
   )


   return fig


# Callback to perform the Diebold-Mariano test based on selected models
@dash.callback(
   Output('dm_test_results', 'children'),
   [Input('model_title1', 'value'),
    Input('model_title2', 'value')]
)
def compute_dm_test(model1_name, model2_name):
   if model1_name and model2_name:
       # Generate mock forecast errors for the two selected models (replace with actual errors)
       # Use actual errors from model predictions
       errors1 = np.random.normal(0, 1, 10)  # Mock forecast errors for Model 1
       errors2 = np.random.normal(0, 1, 10)  # Mock forecast errors for Model 2
      
       # Ensure the errors are numerical (float)
       errors1 = np.array(errors1, dtype=float)
       errors2 = np.array(errors2, dtype=float)
      
       # Perform the Diebold-Mariano test
       dm_statistic, p_value = diebold_mariano_test(errors1, errors2)
      
       # Create the result message
       result = f"DM Test Result: DM Statistic = {dm_statistic:.2f}, p-value = {p_value:.3f}. Conclusion: "
      
       # Conclusion based on p-value
       if p_value < 0.05:
           conclusion = "The models are significantly different in terms of forecast accuracy."
       else:
           conclusion = "No significant difference between the models."
      
       # Return the result and conclusion in the layout
       return html.Div([
           html.H2("Diebold-Mariano (DM) Test Results"),
           html.Div(f'DM Statistic: {dm_statistic:.2f}', style={'display': 'inline-block', 'fontSize': '20px', 'width': '60%', 'color':'white'}),
           html.Div(f'p-value: {p_value:.3f}', style={'display': 'inline-block', 'fontSize': '20px', 'width': '60%', 'color':'white'}),
           html.Div(f"Conclusion: {conclusion}", style={'display': 'inline-block', 'fontSize': '18px', 'width': '80%', 'color':'white'})
       ])
   return "Please select both models to compare."