import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import requests 

external_stylesheets = [dbc.themes.BOOTSTRAP]+['assets/style.css']
dash.register_page(__name__, path="/dashboard", name="dashboard", external_stylesheets=external_stylesheets)

layout = html.Div(className='simple-form', children=[
    html.Button("Registration", id="registration", formAction='', n_clicks=0, className="simple-button",),
    html.Div(id="output1"),
    dcc.Location(id='url', refresh=True),
])

