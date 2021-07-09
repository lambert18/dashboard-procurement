import dash
import dash_core_components as dcc
import dash_html_components as html
from matplotlib.pyplot import title
import datetime as dt
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import base64
import io
from app import app
import dash_core_components as dcc
from datetime import date

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
    html.Div(id='output-container-upload'),
    html.Div('Tanggal'),
    'Bulan',
    dcc.Input(
        id="bulan",
        value=0.0,
        type="number"
    ),

    html.Div(dcc.Graph(
        id='FPPGRAPH',
    ), style={
        "display": "block",
        "width": "100%"
    }),

    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=dt.date.today(),
        initial_visible_month=dt.date.today(),
        start_date=dt.date.today(),
        end_date=dt.date.today()
    ),
    html.Div(id='output-container-date-picker-range'),
    html.Div(dcc.Graph(
        id='FPPGRAPH1',
    ), style={
        "display": "block",
        "width": "100%"
    }),
])


def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        # if filename is not 'FPPFKP.xlsx':
        #     raise Exception('spam', 'eggs')
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded),
                               sheet_name='FPP', skiprows=4, usecols="B,D,O")
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


@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


@app.callback(Output('output-container-upload', 'children'),
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


@app.callback(Output('FPPGRAPH', 'figure'),
              Input('upload-data', 'contents'),
              Input('upload-data', 'filename'),
              Input("bulan", "value")
              )
def update_graph1(contents, filename, bulan):
    fig = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"],
            title='Trend Category Per Bulan', barmode='stack')
    }

    if contents:

        contents = contents[0]
        filename = filename[0]
        print(filename)

        df = parse_data(contents, filename)

        # ADMINISTRASI = df.loc[df['tier1'] == 'ADMINISTRASI'].count()[0]
        # NaN = df['tier1'].isnull().values.any().sum()
        mask = df['TGL'].map(lambda x: x.month) == bulan
        df_with_good_dates = df.loc[mask]
        month_list = [i.strftime("%b-%y")
                      for i in df_with_good_dates['TGL']]
        labels = sorted(set(month_list))
        planning = df_with_good_dates[df_with_good_dates.tier1 == 'planning'].groupby(
            [df_with_good_dates.TGL.dt.year, df_with_good_dates.TGL.dt.month]).agg({"tier1": "count"}).values
        var = [i[0] for i in planning]
        ADMINISTRASI = df_with_good_dates[df_with_good_dates.tier1 == 'ADMINISTRASI'].groupby(
            [df_with_good_dates.TGL.dt.year, df_with_good_dates.TGL.dt.month]).agg({"tier1": "count"}).values
        var1 = [i[0] for i in ADMINISTRASI]

        notnulindex = df_with_good_dates.dropna().index
        varA = df_with_good_dates.loc[~df_with_good_dates.index.isin(
            notnulindex)]

        NaN = varA.groupby(
            [df_with_good_dates.TGL.dt.year, df_with_good_dates.TGL.dt.month]).agg({"NO. PO": "count"}).values
        var2 = [i[0] for i in NaN]

        layout = go.Layout(title='Trend Category Per Bulan', barmode='stack')
        fig = go.Figure(data=[
            go.Bar(name='Planning', x=labels, y=var),
            go.Bar(name='ADMINISTRASI', x=labels, y=var1),
            go.Bar(name='NaN', x=labels, y=var2)
        ])

    return fig


@app.callback(Output('FPPGRAPH1', 'figure'),
              Input('upload-data', 'contents'),
              Input('upload-data', 'filename'),
              [Input("my-date-picker-range", "start_date"),
              Input("my-date-picker-range", "end_date")]
              )
def update_graph2(contents, filename, start_date, end_date):
    fig1 = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"],
            title='Trend Category Per Bulan', barmode='stack')
    }

    if contents:

        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        # ADMINISTRASI = df.loc[df['tier1'] == 'ADMINISTRASI'].count()[0]
        # NaN = df['tier1'].isnull().values.any().sum()
        mask = (df['TGL'] >= start_date) & (
            df['TGL'] <= end_date)
        df_with_good_dates = df.loc[mask]
        planning = df_with_good_dates.loc[df_with_good_dates['tier1'] == 'planning'].count()[
            0]
        ADMINISTRASI = df_with_good_dates.loc[df_with_good_dates['tier1'] == 'ADMINISTRASI'].count()[
            0]
        NaN = df_with_good_dates.tier1.isnull().sum()

        print(NaN)
        labels = ['planning', 'ADMINISTRASI', 'NaN']
        values = [planning, ADMINISTRASI, NaN]

        layout = go.Layout(title='Trend Category Per Bulan', barmode='stack')

        fig1 = go.Figure([go.Bar(x=labels, y=values)])

    return fig1
