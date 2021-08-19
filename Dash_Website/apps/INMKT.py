import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

layout = html.Div(children=[
    html.H1(children='Indirect MKT', className="layout"),
    html.Div(dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'FPP', 'value': 'FPP'},
            {'label': 'FKP', 'value': 'FKP'},
            {'label': 'SUMMARY', 'value': 'SUMMARY'}
        ],
        value='SUMMARY'), className="dropdown__menu"),
])
