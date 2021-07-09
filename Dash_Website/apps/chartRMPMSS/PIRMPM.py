import dash
import dash_core_components as dcc
import dash_html_components as html
from matplotlib.pyplot import title

import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import base64
import io
from app import app

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='filename-PI'),
    html.Div(dcc.Graph(
        id='PIGraph1',
    ), style={
        "display": "block",
        "width": "100%"
    }),
    html.Div(dcc.Graph(
        id='PIGraph2',
    ), style={
        "display": "block",
        "width": "100%"
    }),
])


def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded),
                               sheet_name='Sheet1')
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


@app.callback(Output('filename-PI', 'children'),
              [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
]
)
def update_output2(contents, filename):
    string_prefix = 'You have selected: '
    table = html.Div()
    if contents:
        contents = contents[0]
        filename = filename[0]
        string_prefix = string_prefix + filename
    if len(string_prefix) == len('You have selected: '):
        return 'Select a file to see it displayed here'
    else:
        return string_prefix


@app.callback(Output('PIGraph1', 'figure'),
              [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_graph1(contents, filename):
    fig1 = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }

    if contents:
        contents = contents[0]
        filename = filename[0]
        Rekap_PI = parse_data(contents, filename)
        df = pd.DataFrame(data=Rekap_PI)
        fig1 = go.Figure(data=[
            go.Scatter(name='RMPM',
                       x=df['MTD'], y=df['RMPM']),
            go.Scatter(name='Target', x=df['MTD'], y=df['Target']),
            go.Bar(name='RM', x=df['MTD'], y=df['RM']),
            go.Bar(name='PM', x=df['MTD'], y=df['PM'])
        ])
    return fig1


@ app.callback(Output('PIGraph2', 'figure'),
               [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_graph2(contents, filename):
    fig = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"],
            barmode='group')
    }

    if contents:
        contents = contents[0]
        filename = filename[0]
        Rekap_PI = parse_data(contents, filename)
        df = pd.DataFrame(data=Rekap_PI)
        fig = go.Figure(data=[
            go.Scatter(name='RMPM.1',
                       x=df['YTD'], y=df['RMPM.1']),
            go.Scatter(name='Target.1', x=df['YTD'], y=df['Target.1']),
            go.Bar(name='RM.1', x=df['YTD'], y=df['RM.1']),
            go.Bar(name='PM.1', x=df['YTD'], y=df['PM.1'])
        ])

    return fig
