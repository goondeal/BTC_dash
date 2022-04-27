import numpy as np
import datetime as dt
import pandas as pd

from dash import Dash, html, dcc
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from controller import DataProvider


data_provider = DataProvider()

# TODO: set graph & axis titles
fig = data_provider.get_strategy_graph()
# go.Figure(
#     data=[
#         go.Candlestick(x=df.index,
#                        open=df['open'],
#                        high=df['high'],
#                        low=df['low'],
#                        close=df['close'])
#     ],
# )

# fig.show()

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           )


def build_card():
    return dbc.Card(
        dbc.CardBody("This is some text within a card body"),
        style={'height': '100px', 'wigth': '100px'},
    )


def build_row_cards():
    return dbc.Row(
        [
            dbc.Col(build_card()),
            dbc.Col(build_card()),
            dbc.Col(build_card()),
            dbc.Col(build_card()),
        ],
        align="center",
        className="my-2 p-0 justify-content-between",
    )


app.layout = html.Div(children=[dbc.Navbar(
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
),
    dbc.Container(
        [
            build_row_cards(),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(figure=fig, config={
                        'displayModeBar': False, 'autosizable': True, 'displaylogo': False},)
                        , width=8,),
                    dbc.Col([
                        html.H6(f'{k}: {v}') for k, v in data_provider.get_strategy_summary().items()     
                        # dbc.Button("Go somewhere", color="primary",
                        #            className='my-2', style={'width': '100%'}),
                        # dbc.Button("Go somewhere", color="danger",
                        #            className='my-2', style={'width': '100%'}),
                        # dbc.Button("Go somewhere", color="warning",
                        #            className='my-2', style={'width': '100%'}),
                        # dbc.Button("Go somewhere", color="success",
                        #            className='my-2', style={'width': '100%'}),
                    ],
                        className='m-auto ',
                        width=4,
                    ),
                ]
            )]
)
]
)


if __name__ == '__main__':
    # print(app.config)
    app.run_server(debug=True)
