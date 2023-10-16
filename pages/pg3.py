import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, callback


""" PLOTLY_LOGO is a object from s3 bucket."""
PLOTLY_LOGO = "https://myteamplanner.s3.eu-north-1.amazonaws.com/logo.png"

dash.register_page(
    __name__,
    path="/p3",
    name="p3",
)

""" nav_iteam can be used for mention links on header parts. """
nav_item = dbc.NavItem(dbc.NavLink("Sign out", href="#"))
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Entry 1"),
        dbc.DropdownMenuItem("Entry 2"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Entry 3"),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
)

""" main layout of dashboard"""
navbar = html.Div(
    [
        dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            ],
                            # align="center",
                            # className="g-0",
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
            # className="mb-5",
        ),
        dcc.Location(id="url"),  # Add the URL location component
    ],
)

layout = html.Div(
    children=[
        html.Div(children=[navbar], className="child",),
        html.Div(
            children=[
                html.Div("slidbar", className="child"),
                html.Div("content", className="child content"),
            ],
            className="main",
        ),
        html.Div("footer", className="child"),
    ],
    className="parent",
)
