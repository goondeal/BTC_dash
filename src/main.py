import numpy as np
import datetime as dt
import pandas as pd

from dash import Dash, html, dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
        )


app.layout = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/assets/logo.png', height="30px")),
                        dbc.Col(dbc.NavbarBrand("BTC I", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
        ]
    ),
)


if __name__ == '__main__':
    # print(app.config)
    app.run_server(debug=True)
