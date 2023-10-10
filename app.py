import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from users import USERNAME_PASSWORD_PAIRS   

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        html.Div(
            # dcc.Link(href='/page3')
        )
    ]),
    dash.page_container
])


if __name__ == '__main__':
    app.run(debug=True)