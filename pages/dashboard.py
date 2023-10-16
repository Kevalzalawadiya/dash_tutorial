''' This is code made with bootstrap with resonsive pages.'''

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, callback, dcc 

''' PLOTLY_LOGO is a object from s3 bucket.'''
PLOTLY_LOGO = "https://myteamplanner.s3.eu-north-1.amazonaws.com/logo.png"

dash.register_page(__name__, path="/dashboard", name="dashboard")

''' nav_iteam can be used for mention links on header parts. '''
nav_item = dbc.NavItem(dbc.NavLink("Sign out", href="#"))
dropdown = dbc.DropdownMenu(children=[
        dbc.DropdownMenuItem("Entry 1"),
        dbc.DropdownMenuItem("Entry 2"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Entry 3"),
    ],
    nav=True,
    in_navbar=True, 
    label="Menu",
)

''' slide bar header is atteched on slidebar      '''
sidebar_header = dbc.Row(
    [
        dbc.Col(html.H2("Sidebar", className="display-4")),
        dbc.Col(
            [
                html.Button(
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            width="auto",
            align="center",
        ),
    ]
)


''' this is sidebar i try to mention in logo '''
sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P(
                    "A responsive sidebar layout with collapsible navigation "
                    "links.",
                    className="lead",
                ),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Page 1", href="/page-1", active="exact"),
                    dbc.NavLink("Page 2", href="/page-2", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)

content = html.Div(id="page-content")


''' main layout of dashboard'''
layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="https://myteamplanner.s3.eu-north-1.amazonaws.com/logo.png",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(
                        [dropdown, nav_item],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse2",
                    navbar=True,
                ),
            ],
        ),
        color="dark",
        dark=True,
        className="mb-5",
    ),
    dcc.Location(id="url"),  # Add the URL location component
    sidebar,  # Add the sidebar
    content  # Add the main content
])



''' we use a callback to toggle the collapse on small screens'''
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# the same function (toggle_navbar_collapse) is used in all three callbacks
for i in [1, 2, 3]:
    callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)


''' slide bar call back '''
@callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# to do for tommorow need to manage the slide bar and the navbar