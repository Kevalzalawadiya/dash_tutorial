from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc



app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# styling the slidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa"
}
# padding for the page content 
CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P("A simple sidebar layout with navigation links", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
                dbc.NavLink("Page 3", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),     
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id='page-content', children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar,
    content,
    ])
    


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)

def render_page_content(pathname):
    if pathname == '/':
        return [
            html.H1('Home Page'),
        ]
    elif pathname == '/page-1':
        return [
            html.H1('Page 1'),
        ]
    elif pathname == '/page-2':
        return [
            html.H1('Page 2'),
        ]
    

if __name__ == '__main__':
    app.run_server(debug=True)