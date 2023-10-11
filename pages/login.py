import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import requests 

external_stylesheets = [dbc.themes.BOOTSTRAP]+['assets/style.css']
dash.register_page(__name__, path="/", name="Home", external_stylesheets=external_stylesheets)


layout = html.Div(className='simple-form', children=[
    dcc.Input(id="email", type="text", placeholder="Enter Username", className='input-field'),
    dcc.Input(id="passw",type="password", placeholder="Enter Password", className='input-field',),
    html.Button("submit", id="submit", formAction='', n_clicks=0, className="simple-button",),
    html.P([ "If you don't have an account, ",
            dcc.Link("register here", id="registration", href="/registration", className="registration-link"),
        ]),  
    html.Div(id="output1"),
    dcc.Location(id='url', refresh=True),
])
           
            

@callback(
    Output("output1", "children"),
    Output('url', 'pathname'),
    Input("submit", "n_clicks"),
    State("email", "value"),
    State("passw", "value")
)
def update_output(submit, email, passw):
    if submit:
        data = {"email": email, "password": passw}
        print("DATA -------------> ", data)
        response = requests.post("http://localhost:8000/login", json=data)
        print("Response : ------------> ", response)

        if response.status_code == 200:
            return html.Div(), '/dashboard'
        else:
            return html.Div(children=[ dbc.Alert("Invalid username or password!", color="dark", className="alert-box")],
                className='static-info'
            ), '/'
    
    if email == "" or email is None or passw == "" or passw is None:
        return html.Div(children="", style={"padding-left": "550px", "padding-top": "10px"}
        ), '/'
    
    
    return html.Div(
        children=[ dbc.Alert("Invalid username or password!", color="dark", className='alert-box')], className='static-info'
    ), '/'
    
    


