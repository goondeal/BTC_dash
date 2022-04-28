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

# upper triangle \u25B2 
# lower triangle \u25BC
def build_card(title, subtitle, borderColor="red"):

    p1 = max(title, subtitle)
    p2 = min(title, subtitle)
    _return_ = (p1-p2)/p1 * 100
    _tri_ = "\u25B2" if title > subtitle else "\u25BC"
    _color_ = "green" if title > subtitle else "red"
    return dbc.Card( 
        dbc.CardBody([html.H4(f"{round(title,2)} $", className="card-title"),
                      html.P(
                                f"{round(_return_,5)}%  {_tri_}",
                                className="card-text",
                                style={"color": _color_}
                             ), 
                     ], 
                     style={"margin": "auto"}),
        style={'height': '100px', 'wigth': '100px',
               "border-bottom": f"4px solid {borderColor}"},
        # className= "border-top-dark border-top-3"
    )


def build_row_cards():
    return dbc.Row(
        [
            dbc.Col(build_card(38170.72, 30000, "black")),
            dbc.Col(build_card(38170.72, 34680.05)),
            dbc.Col(build_card(38170.72, 50000, "green")),
            dbc.Col(build_card(38170.72, 38112.65, "blue")),
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
            dcc.Dropdown(
                ['SMA', 'MACD', 'BF'],
                ['SMA', 'MACD', 'BF'],
                multi=True,
                id="drop-down-id",
                style = {"margin-top":"48px"}
            ),
            dbc.Container(id="lol"),
            # dbc.Row(
            #     [
            #         dbc.Col(
            #             dcc.Graph(figure=fig, config={
            #             'displayModeBar': False, 'autosizable': True, 'displaylogo': False},)
            #             , width=8,),
            #         dbc.Col([
            #             html.H6(f'{k}: {v}') for k, v in data_provider.get_strategy_summary().items()
            #             # dbc.Button("Go somewhere", color="primary",
            #             #            className='my-2', style={'width': '100%'}),
            #             # dbc.Button("Go somewhere", color="danger",
            #             #            className='my-2', style={'width': '100%'}),
            #             # dbc.Button("Go somewhere", color="warning",
            #             #            className='my-2', style={'width': '100%'}),
            #             # dbc.Button("Go somewhere", color="success",
            #             #            className='my-2', style={'width': '100%'}),
            #         ],
            #             className='m-auto ',
            #             width=4,
            #         ),
            #     ]
            # )
        ]
)
]
)


@app.callback(
    Output("lol", 'children'),
    Output('drop-down-id', 'value'),
    Input('drop-down-id', 'value')
)
def test_drop_down(value):
    # print(len(value))
    value2 = value
    lst = []
    colors = {"SMA":"rgba(255,0,0,0.1)", "MACD":"rgba(0,255,0,0.1)", "BF":"rgba(0,0,255,0.1)"}
    for i in value:
        lst.append(dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=fig, config={
                        'displayModeBar': False, 'autosizable': True, 'displaylogo': False},), width=9,),
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
                        width=3,
                        ),
            ], 
            style = {"background-color":colors[i], "margin":"16px", "padding":"16px"}
        ))
    if len(value) == 0:
        value2 = ["SMA"]
        lst.append("SMA")

    return lst, value2


if __name__ == '__main__':
    # print(app.config)
    app.run_server(debug=True)
