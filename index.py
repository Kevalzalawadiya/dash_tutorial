import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

import base64
import datetime
import io

import pandas as pd
import dash

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# styling the slidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "15rem",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}
# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P("A simple sidebar layout with navigation links", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


upload_data = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        html.Div(id="output-data-upload"),
    ]
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        "Python Multipage App with Dash",
                        style={"fontSize": 50, "textAlign": "center"},
                    )
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([sidebar], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
                dbc.Col([dash.page_container], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10),
            ]
        ),
    ],
    fluid=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)
