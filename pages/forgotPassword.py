import dash
from dash import dcc, html, callback, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import requests


dash.register_page(__name__, path="/forgotPassword", name="forgotPassword")

layout = html.Div(className='simple-form', children=[
    dcc.Input(id="email", type="email", placeholder="Enter Email", className='input-field'),
    html.Button("submit", id="submit", n_clicks=0, disabled=True, className=""),
    html.Div(id="output-data"),
    
])



@callback(
    Output('submit', 'disabled'),
    Output('output-data', 'children'),
    Input('email', 'value'),
    Input('submit', 'n_clicks'),
)
def show_data(email, submit):
    if email:
        if submit > 0:
            data = {"email": email}
            print("DATA -------------> ", data)
            return no_update, html.Div(children=[dbc.Alert("Email Sent", className="custom-fade-in")])
        return False, no_update
    

    return True, no_update

