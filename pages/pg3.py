import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, callback
from .ManageAccout import function


""" PLOTLY_LOGO is a object from s3 bucket."""
PLOTLY_LOGO = "https://myteamplanner.s3.eu-north-1.amazonaws.com/logo.png"

dash.register_page(
    __name__,
    path="/p3",
    name="p3",
)

layout = None