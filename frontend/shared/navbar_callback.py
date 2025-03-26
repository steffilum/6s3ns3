import dash 
from dash import html, dcc, Input, Output, State


# Callback to toggle indicator and model dropdown visibility and blur content
@dash.callback(
    Output("model-fade", "is_in"),
    Output("indicator-fade", "is_in"),
    Output("main-content", "style"),
    Input("model-fade-button", "n_clicks"),
    Input("indicator-fade-button", "n_clicks"),
    State("model-fade", "is_in"),
    State("indicator-fade", "is_in"),
    State("main-content", "style"),
    prevent_initial_call=True  # Avoid errors on page load
)
def toggle_fades(model_clicks, indicator_clicks, model_is_in, indicator_is_in, style):

    ctx = dash.callback_context

    # Default fallback if style is None
    if style is None:
        style = {"position": "absolute", "top": "150px", "left": "150px", "width": "300px", "filter": "none"}

    new_style = style.copy()

    if not ctx.triggered:
        return model_is_in, indicator_is_in, new_style

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == "model-fade-button":
        model_show = not model_is_in
        indicator_show = False
        new_style["filter"] = "blur(5px)" if model_show else "none"
        return model_show, indicator_show, new_style

    elif triggered_id == "indicator-fade-button":
        indicator_show = not indicator_is_in
        model_show = False
        new_style["filter"] = "blur(5px)" if indicator_show else "none"
        return model_show, indicator_show, new_style

    return model_is_in, indicator_is_in, new_style