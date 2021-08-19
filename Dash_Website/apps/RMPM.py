import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

from apps.chartRMPM import FPP


layout = html.Div(children=[

    html.H1(children='RMPM', className="layout"),

    html.Div(dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'FPP', 'value': 'a'},
            {'label': 'FKP', 'value': 'FKP'},
        ],
        value=''), className="dropdown__menu"),

    html.Div(id='chart-content', children=[])
])


@ app.callback(Output('chart-content', 'children'),
               [Input('dropdown', 'value')])
def display_page(label):
    # if label == 'FKP':
    #     return FKP.layout
    if label == 'a':
        return FPP.layout
    else:
        return "404 Page Error! Please choose a link"
