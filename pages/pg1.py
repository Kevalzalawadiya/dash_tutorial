import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", name="Home")  # '/' is home page

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6(
                            "Change the value in the text box to see callbacks in action!"
                        ),
                        html.Div(
                            [
                                "Input: ",
                                dcc.Input(
                                    id="my-input", value="initial value", type="text"
                                ),
                            ]
                        ),
                        html.Br(),
                        html.Div(id="my-output"),
                    ],
                    xs=10,
                    sm=10,
                    md=8,
                    lg=4,
                    xl=4,
                    xxl=4,
                )
            ]
        ),
    ]
)

@callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'