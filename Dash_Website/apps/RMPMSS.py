import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

from apps.chartRMPMSS import summary, spending, PIRMPM


layout = html.Div(children=[
    html.H1('RMPM-SS', style={
        "text-align": "center"
    }),

    html.Div(dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Purchase by Supplier & Category', 'value': 'a'},
            {'label': 'Price Index', 'value': 'b'},
            {'label': 'Contract Coverage per Supplier Category', 'value': 'c'},
            {'label': 'Spending by Category', 'value': 'd'}
        ],
        value='a'), style={
            "display": "inline-block",
            "width": "20%"
    }),



    html.Div(id='chart-content1', children=[])
])


@ app.callback(Output('chart-content1', 'children'),
               [Input('dropdown', 'value')])
def display_page(label):
    # if label == 'FKP':
    #     return FKP.layout
    if label == 'a':
        return summary.layout
    if label == 'b':
        return PIRMPM.layout
    if label == 'd':
        return spending.layout
    else:
        return "404 Page Error! Please choose a link"
