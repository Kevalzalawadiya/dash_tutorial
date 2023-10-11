import dash 
import dash_bootstrap_components as dbc
import requests
from dash import html, dcc

dash.register_page(__name__, path='/registration', name='registration', external_stylesheets=['assets/registration.css'])



layout = html.Div(className="simple-form", children=[
    html.H2("Registration Form"),
    dcc.Input(placeholder="Username", type="text", className="input-field"),
    dcc.Input(placeholder="Email", type="email", className="input-field"),
    dcc.Input(placeholder="Password", type="password", className="input-field"),
    html.Button("Register", className="simple-button"),
])




