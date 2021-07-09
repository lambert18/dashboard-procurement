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
    html.Div(id='filename-spending'),
    html.Div(dcc.Graph(
        id='SpendingGraph1',
    ), style={
        "display": "block",
        "width": "100%"
    }),
    html.Div(dcc.Graph(
        id='SpendingGraph2',
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
                               sheet_name='summary-value-normal')
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


@app.callback(Output('filename-spending', 'children'),
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


@app.callback(Output('SpendingGraph1', 'figure'),
              [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_graph1(contents, filename):
    fig = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }

    if contents:
        contents = contents[0]
        filename = filename[0]
        Data_spending_category = parse_data(contents, filename)
        fig = go.Figure([go.Scatter(
            x=Data_spending_category['Kategory'], y=Data_spending_category['Polyroll'])])

    return fig


@app.callback(Output('SpendingGraph2', 'figure'),
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
        Data_spending_category = parse_data(contents, filename)
        df = pd.DataFrame(data=Data_spending_category)
        fig = go.Figure(data=[
            go.Bar(name='offset duplex',
                   x=df['Kategory'], y=df['offset duplex']),
            go.Bar(name='Polyroll', x=df['Kategory'], y=df['Polyroll']),
            go.Bar(name='corr. Box', x=df['Kategory'], y=df['corr. Box']),
            go.Bar(name='can', x=df['Kategory'], y=df['can']),
            go.Bar(name='spoon', x=df['Kategory'], y=df['spoon']),
            go.Bar(name='shrink label',
                   x=df['Kategory'], y=df['shrink label']),
            go.Bar(name='plastic banded',
                   x=df['Kategory'], y=df['plastic banded']),
            go.Bar(name='Lid cap can', x=df['Kategory'], y=df['Lid cap can']),
            go.Bar(name='alu lid cap', x=df['Kategory'], y=df['alu lid cap']),
            go.Bar(name='paper banded',
                   x=df['Kategory'], y=df['paper banded']),
            go.Bar(name='Total MTD Value',
                   x=df['Kategory'], y=df['Total MTD Value'])
        ])

    return fig
