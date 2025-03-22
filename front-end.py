import dash
from dash import html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd

# App setup
app = dash.Dash(__name__)

# Mock Data
model1 = pd.DataFrame({"Year": [str(y) for y in range(2010, 2020)], "GDP": [15, 10, 20, 30, 35, 22, 8, 4, 23, 31]})
model2 = pd.DataFrame({"Year": [str(y) for y in range(2010, 2020)], "GDP": [20, 31, 54, 23, 43, 12, 25, 12, 4, 3]})
model3 = pd.DataFrame({"Year": [str(y) for y in range(2010, 2020)], "GDP": [12, 18, 33, 28, 39, 25, 19, 11, 6, 15]})

# List of figures
figures = [
    px.line(model1, x='Year', y='GDP', title='Model 1: '),
    px.line(model2, x='Year', y='GDP', title='Model 2: '),
    px.line(model3, x='Year', y='GDP', title='Model 3: ')
]

# Layout
app.layout = html.Div([
    html.H2("6SENS3 Nowcasting"),
    #html.H4(f'{forecast_value})
    dcc.Store(id='page-index', data=0),  # Keep track of current graph index

    dcc.Graph(id='graph-display'),

    html.Div([
        html.Button("Previous", id='prev-btn', n_clicks=0),
        html.Button("Next", id='next-btn', n_clicks=0)
    ], style={'marginTop': '20px'}),

    html.Div(id='page-label', style={'marginTop': '10px', 'fontWeight': 'bold'})
])

# Callback to update graph based on click-through
@app.callback(
    Output('page-index', 'data'),
    Input('prev-btn', 'n_clicks'),
    Input('next-btn', 'n_clicks'),
    State('page-index', 'data')
)
def update_page(prev_clicks, next_clicks, current_index):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_index
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'next-btn':
        return min(current_index + 1, len(figures) - 1)
    elif button_id == 'prev-btn':
        return max(current_index - 1, 0)
    return current_index

# Callback to display the current graph and label
@app.callback(
    Output('graph-display', 'figure'),
    Output('page-label', 'children'),
    Input('page-index', 'data')
)
def display_graph(index):
    return figures[index], f"Page {index + 1} of {len(figures)}"

if __name__ == '__main__':
    app.run(debug=True)


