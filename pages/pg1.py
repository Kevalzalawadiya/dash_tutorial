import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import requests 

dash.register_page(
    __name__, path="/", name="Home", external_stylesheets=[dbc.themes.BOOTSTRAP]
)
layout = html.Div(
    [
        html.Div(
            children=[
                dcc.Input(
                    id="email",
                    type="text",
                    placeholder="Enter Username",
                    style={
                        "margin-left": "35%",
                        "width": "450px",
                        "height": "45px",
                        "padding": "10px",
                        "margin-top": "60px",
                        "font-size": "16px",
                        "border-width": "3px",
                        "border-color": "#a0a3a2",
                    },
                ),
            ]
        ),
        html.Div(
            dcc.Input(
                id="passw",
                type="password",  # Use type="password" for password input
                placeholder="Enter Password",
                style={
                    "margin-left": "35%",
                    "width": "450px",
                    "height": "45px",
                    "padding": "10px",
                    "margin-top": "10px",
                    "font-size": "16px",
                    "border-width": "3px",
                    "border-color": "#a0a3a2",
                },
            ),
        ),
        html.Div(
            children=[
                html.Button(
                    "Verify",
                    id="verify",
                    formAction='',
                    n_clicks=0,
                    className="btn btn-primary",  # Bootstrap class for button
                    style={"border-width": "3px", "font-size": "14px"},
                ),
                # to do registration 
                # html.Button(
                #     "Registration",
                #     id="registration",
                #     formAction='',
                #     n_clicks=0,
                #     className="btn btn-primary",  # Bootstrap class for button
                #     style={"border-width": "3px", "font-size": "14px"},
                # ),
            ],
            
            style={"margin-left": "45%", "padding-top": "30px"},
        ),
        html.Div(id="output1"),
        dcc.Location(id='url', refresh=True)
    ]
)


 
@callback(
    Output("output1", "children"),
    Output('url', 'pathname'),
    Input("verify", "n_clicks"),
    State("email", "value"),
    State("passw", "value")
)

def update_output(n_clicks, email, passw):
    if n_clicks:
        data = {"email": email, "password": passw}
        print("DATA -------------> ", data)
        response = requests.post("http://localhost:8000/login", json=data)
        print("Response : ------------> ", response)

        if response.status_code == 200:
            return html.Div(), '/page3'
        else:
            return html.Div(
                children=[ 
                    dbc.Alert("Invalid username or password!",
                        id="alert", 
                        color="dark", 
                        style={
                            "margin-left": "35%",
                            "width": "450px",
                            "height": "45px",
                            "padding": "10px",
                            "margin-top": "10px",
                            "font-size": "16px",
                            "border-width": "3px",
                            "border-color": "#a0a3a2",
                        },
                    ),
                ],
                style={"padding-left": "550px", "padding-top": "40px", "font-size": "16px"},
            ), '/'
    
    if email == "" or email is None or passw == "" or passw is None:
        return html.Div(
            children="",
            style={"padding-left": "550px", "padding-top": "10px"}
        ), '/'
    
    return html.Div(
        children=[
            dbc.Alert("Invalid username or password!",
                id="alert", 
                color="dark", 
                style={
                    "margin-left": "35%",
                    "width": "450px",
                    "height": "45px",
                    "padding": "10px",
                    "margin-top": "10px",
                    "font-size": "16px",
                    "border-width": "3px",
                    "border-color": "#a0a3a2",
                },
            ),
        ],
        style={"padding-left": "550px", "padding-top": "40px", "font-size": "16px"},
    ), '/'
