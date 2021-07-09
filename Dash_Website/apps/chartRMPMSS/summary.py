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
    html.Div(id='filename-summary'),
    html.Div(dcc.Graph(
        id='Mygraph1',
    ), style={
        "display": "inline-block",
        "width": "30%"
    }),
    html.Div(dcc.Graph(
        id='Mygraph2',
    ), style={
        "display": "inline-block",
        "width": "30%"
    }),
    html.Div(dcc.Graph(
        id='Mygraph3',
    ), style={
        "display": "inline-block",
        "width": "30%"
    }),
    html.Div(dcc.Graph(
        id='Mygraph4',
    ), style={
        "display": "inline-block",
        "width": "50%"
    }),
    html.Div(dcc.Graph(
        id='Mygraph5',
    ), style={
        "display": "inline-block",
        "width": "50%"
    }),
    html.Div(dcc.Graph(
        id='Mygraph6',
    ), style={
        "display": "block",
        "width": "50%"
    })
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
                               sheet_name='SHP___Receiving_Transaction_Su_')
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    print(df)
    return df


@app.callback(Output('filename-summary', 'children'),
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


@app.callback(Output('Mygraph1', 'figure'),
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
        Data_RTS = parse_data(contents, filename)
        Data_RTS['Unnamed: 5'] = Data_RTS['Unnamed: 5'].str.strip().str.upper()
        # CHART1
        BOTTLE = Data_RTS[Data_RTS['Unnamed: 5'] == 'BOTTLE']
        jumlah_BOTTLE = BOTTLE['Unnamed: 10'].sum()

        CAN = Data_RTS[Data_RTS['Unnamed: 5'] == 'CAN']
        jumlah_CAN = CAN['Unnamed: 10'].sum()

        POLYROLL = Data_RTS[Data_RTS['Unnamed: 5'] == 'POLYROLL']
        jumlah_POLYROLL = POLYROLL['Unnamed: 10'].sum()

        SPOON = Data_RTS[Data_RTS['Unnamed: 5'] == 'SPOON']
        jumlah_SPOON = SPOON['Unnamed: 10'].sum()

        STRAW = Data_RTS[Data_RTS['Unnamed: 5'] == 'STRAW']
        jumlah_STRAW = STRAW['Unnamed: 10'].sum()

        alu_lid_cap = Data_RTS[Data_RTS['Unnamed: 5'] == 'ALU LID CAP']
        jumlah_alu_lid_cap = alu_lid_cap['Unnamed: 10'].sum()

        corr_Box = Data_RTS[Data_RTS['Unnamed: 5'] == 'CORR. BOX']
        jumlah_corr_Box = corr_Box['Unnamed: 10'].sum()

        offset_duplex = Data_RTS[Data_RTS['Unnamed: 5'] == 'OFFSET DUPLEX']
        jumlah_offset_duplex = offset_duplex['Unnamed: 10'].sum()

        others_PM = Data_RTS[Data_RTS['Unnamed: 5'] == 'OTHERS PM']
        jumlah_others_PM = others_PM['Unnamed: 10'].sum()

        paper_banded = Data_RTS[Data_RTS['Unnamed: 5'] == 'PAPER BANDED']
        jumlah_paper_banded = paper_banded['Unnamed: 10'].sum()

        plastic_banded = Data_RTS[Data_RTS['Unnamed: 5'] == 'PLASTIC BANDED']
        jumlah_plastic_banded = plastic_banded['Unnamed: 10'].sum()

        shrink_label = Data_RTS[Data_RTS['Unnamed: 5'] == 'SHRINK LABEL']
        jumlah_shrink_label = shrink_label['Unnamed: 10'].sum()

        lid_cap_can = Data_RTS[Data_RTS['Unnamed: 5'] == 'LID CAP CAN']
        jumlah_lid_cap_can = lid_cap_can['Unnamed: 10'].sum()

        labels1 = ['ALU LID CAP', 'BOTTLE', 'CAN', 'CORR. BOX', 'LID CAP CAN', 'OFFSET DUPLEX',
                   'OTHERS PM', 'PAPER BANDED', 'PLASTIC BANDED', 'POLYROLL', 'SHRINK LABEL', 'SPOON', 'STRAW']
        values1 = [jumlah_alu_lid_cap, jumlah_BOTTLE, jumlah_CAN, jumlah_corr_Box, jumlah_lid_cap_can, jumlah_offset_duplex,
                   jumlah_others_PM, jumlah_paper_banded, jumlah_plastic_banded, jumlah_POLYROLL, jumlah_shrink_label, jumlah_SPOON, jumlah_STRAW]

        layout = go.Layout(title='SPENDING SUMMARY (MTD Qty)')
        fig = go.Figure(
            data=[go.Pie(labels=labels1, values=values1)], layout=layout)
    return fig


@app.callback(Output('Mygraph2', 'figure'),
              [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_graph2(contents, filename):
    fig2 = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }

    if contents:
        contents = contents[0]
        filename = filename[0]
        Data_RTS = parse_data(contents, filename)
        Data_RTS['Unnamed: 5'] = Data_RTS['Unnamed: 5'].str.strip().str.upper()
        # CHART1
        BOTTLE = Data_RTS[Data_RTS['Unnamed: 5'] == 'BOTTLE']
        jumlah_BOTTLE1 = BOTTLE['Unnamed: 11'].sum()

        CAN = Data_RTS[Data_RTS['Unnamed: 5'] == 'CAN']
        jumlah_CAN1 = CAN['Unnamed: 11'].sum()

        POLYROLL = Data_RTS[Data_RTS['Unnamed: 5'] == 'POLYROLL']
        jumlah_POLYROLL1 = POLYROLL['Unnamed: 11'].sum()

        SPOON = Data_RTS[Data_RTS['Unnamed: 5'] == 'SPOON']
        jumlah_SPOON1 = SPOON['Unnamed: 11'].sum()

        STRAW = Data_RTS[Data_RTS['Unnamed: 5'] == 'STRAW']
        jumlah_STRAW1 = STRAW['Unnamed: 11'].sum()

        alu_lid_cap = Data_RTS[Data_RTS['Unnamed: 5'] == 'ALU LID CAP']
        jumlah_alu_lid_cap1 = alu_lid_cap['Unnamed: 11'].sum()

        corr_Box = Data_RTS[Data_RTS['Unnamed: 5'] == 'CORR. BOX']
        jumlah_corr_Box1 = corr_Box['Unnamed: 11'].sum()

        offset_duplex = Data_RTS[Data_RTS['Unnamed: 5'] == 'OFFSET DUPLEX']
        jumlah_offset_duplex1 = offset_duplex['Unnamed: 11'].sum()

        others_PM = Data_RTS[Data_RTS['Unnamed: 5'] == 'OTHERS PM']
        jumlah_others_PM1 = others_PM['Unnamed: 11'].sum()

        paper_banded = Data_RTS[Data_RTS['Unnamed: 5'] == 'PAPER BANDED']
        jumlah_paper_banded1 = paper_banded['Unnamed: 11'].sum()

        lid_cap_can = Data_RTS[Data_RTS['Unnamed: 5'] == 'LID CAP CAN']
        jumlah_lid_cap_can1 = lid_cap_can['Unnamed: 11'].sum()

        plastic_banded = Data_RTS[Data_RTS['Unnamed: 5'] == 'PLASTIC BANDED']
        jumlah_plastic_banded1 = plastic_banded['Unnamed: 11'].sum()

        shrink_label = Data_RTS[Data_RTS['Unnamed: 5'] == 'SHRINK LABEL']
        jumlah_shrink_label1 = shrink_label['Unnamed: 11'].sum()

        lid_cap_can = Data_RTS[Data_RTS['Unnamed: 5'] == 'LID CAP CAN']
        jumlah_lid_cap_can1 = lid_cap_can['Unnamed: 11'].sum()

        labels2 = ['ALU LID CAP', 'BOTTLE', 'CAN', 'CORR. BOX', 'LID CAP CAN', 'OFFSET DUPLEX',
                   'OTHERS PM', 'PAPER BANDED', 'PLASTIC BANDED', 'POLYROLL', 'SHRINK LABEL', 'SPOON', 'STRAW']
        values2 = [jumlah_alu_lid_cap1, jumlah_BOTTLE1, jumlah_CAN1, jumlah_corr_Box1, jumlah_lid_cap_can1, jumlah_offset_duplex1,
                   jumlah_others_PM1, jumlah_paper_banded1, jumlah_plastic_banded1, jumlah_POLYROLL1, jumlah_shrink_label1, jumlah_SPOON1, jumlah_STRAW1]

        layout2 = go.Layout(title='SPENDING SUMMARY (YTD Qty)',
                            hovermode='closest')
        fig2 = go.Figure(
            data=[go.Pie(labels=labels2, values=values2)], layout=layout2)

    return fig2


@app.callback(Output('Mygraph3', 'figure'),
              [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_graph2(contents, filename):
    fig3 = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }

    if contents:
        contents = contents[0]
        filename = filename[0]
        Data_RTS = parse_data(contents, filename)
        Data_RTS['Unnamed: 5'] = Data_RTS['Unnamed: 5'].str.strip().str.upper()
        # CHART1
        BOTTLE = Data_RTS[Data_RTS['Unnamed: 5'] == 'BOTTLE']
        jumlah_BOTTLE2 = BOTTLE['Unnamed: 12'].sum()

        CAN = Data_RTS[Data_RTS['Unnamed: 5'] == 'CAN']
        jumlah_CAN2 = CAN['Unnamed: 12'].sum()

        POLYROLL = Data_RTS[Data_RTS['Unnamed: 5'] == 'POLYROLL']
        jumlah_POLYROLL2 = POLYROLL['Unnamed: 12'].sum()

        SPOON = Data_RTS[Data_RTS['Unnamed: 5'] == 'SPOON']
        jumlah_SPOON2 = SPOON['Unnamed: 12'].sum()

        STRAW = Data_RTS[Data_RTS['Unnamed: 5'] == 'STRAW']
        jumlah_STRAW2 = STRAW['Unnamed: 12'].sum()

        alu_lid_cap = Data_RTS[Data_RTS['Unnamed: 5'] == 'ALU LID CAP']
        jumlah_alu_lid_cap2 = alu_lid_cap['Unnamed: 12'].sum()

        corr_Box = Data_RTS[Data_RTS['Unnamed: 5'] == 'CORR. BOX']
        jumlah_corr_Box2 = corr_Box['Unnamed: 12'].sum()

        offset_duplex = Data_RTS[Data_RTS['Unnamed: 5'] == 'OFFSET DUPLEX']
        jumlah_offset_duplex2 = offset_duplex['Unnamed: 12'].sum()

        others_PM = Data_RTS[Data_RTS['Unnamed: 5'] == 'OTHERS PM']
        jumlah_others_PM2 = others_PM['Unnamed: 12'].sum()

        paper_banded = Data_RTS[Data_RTS['Unnamed: 5'] == 'PAPER BANDED']
        jumlah_paper_banded2 = paper_banded['Unnamed: 12'].sum()

        lid_cap_can = Data_RTS[Data_RTS['Unnamed: 5'] == 'LID CAP CAN']
        jumlah_lid_cap_can2 = lid_cap_can['Unnamed: 12'].sum()

        plastic_banded = Data_RTS[Data_RTS['Unnamed: 5'] == 'PLASTIC BANDED']
        jumlah_plastic_banded2 = plastic_banded['Unnamed: 12'].sum()

        shrink_label = Data_RTS[Data_RTS['Unnamed: 5'] == 'SHRINK LABEL']
        jumlah_shrink_label2 = shrink_label['Unnamed: 12'].sum()

        lid_cap_can = Data_RTS[Data_RTS['Unnamed: 5'] == 'LID CAP CAN']
        jumlah_lid_cap_can2 = lid_cap_can['Unnamed: 12'].sum()

        labels3 = ['ALU LID CAP', 'BOTTLE', 'CAN', 'CORR. BOX', 'LID CAP CAN', 'OFFSET DUPLEX',
                   'OTHERS PM', 'PAPER BANDED', 'PLASTIC BANDED', 'POLYROLL', 'SHRINK LABEL', 'SPOON', 'STRAW']
        values3 = [jumlah_alu_lid_cap2, jumlah_BOTTLE2, jumlah_CAN2, jumlah_corr_Box2, jumlah_lid_cap_can2, jumlah_offset_duplex2,
                   jumlah_others_PM2, jumlah_paper_banded2, jumlah_plastic_banded2, jumlah_POLYROLL2, jumlah_shrink_label2, jumlah_SPOON2, jumlah_STRAW2]

        layout3 = go.Layout(title='SPENDING SUMMARY (MTD Value)',
                            hovermode='closest')
        fig3 = go.Figure(
            data=[go.Pie(labels=labels3, values=values3)], layout=layout3)

    return fig3


@app.callback(Output('Mygraph4', 'figure'),
              [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_graph4(contents, filename):
    fig4 = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }

    if contents:
        contents = contents[0]
        filename = filename[0]
        Data_RTS = parse_data(contents, filename)
        Data_RTS['Unnamed: 5'] = Data_RTS['Unnamed: 5'].str.strip().str.upper()
        # CHART4
        DAYACIPTA_KEMASINDO_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                          == 'DAYACIPTA KEMASINDO, PT']
        jumlah_DAYACIPTA_KEMASINDO_PT = DAYACIPTA_KEMASINDO_PT['Unnamed: 10'].sum(
        )

        DUA_KELINCI_PT = Data_RTS[Data_RTS['Unnamed: 1'] == 'DUA KELINCI, PT']
        jumlah_DUA_KELINCI_PT = DUA_KELINCI_PT['Unnamed: 10'].sum()

        KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                                                      == 'KEDAWUNG SETIA CORRUGATED CARTON BOX INDUSTRIAL, PT']
        jumlah_KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT = KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT['Unnamed: 10'].sum(
        )

        MULTIBOX_INDAH_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                     == 'MULTIBOX INDAH, PT']
        jumlah_MULTIBOX_INDAH_PT = MULTIBOX_INDAH_PT['Unnamed: 10'].sum()

        PARAMITRA_GUNAKARYA_CEMERLANG_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                                    == 'PARAMITRA GUNAKARYA CEMERLANG, PT']
        jumlah_PARAMITRA_GUNAKARYA_CEMERLANG_PT = PARAMITRA_GUNAKARYA_CEMERLANG_PT['Unnamed: 10'].sum(
        )

        PURINUSA_EKAPERSADA_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                          == 'PURINUSA EKAPERSADA, PT']
        jumlah_PURINUSA_EKAPERSADA_PT = PURINUSA_EKAPERSADA_PT['Unnamed: 10'].sum(
        )

        SUPRACOR_SEJAHTERA_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                         == 'SUPRACOR SEJAHTERA, PT']
        jumlah_SUPRACOR_SEJAHTERA_PT = SUPRACOR_SEJAHTERA_PT['Unnamed: 10'].sum(
        )

        SURYA_RENGO_CONTAINERS_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                             == 'SURYA RENGO CONTAINERS, PT']
        jumlah_SURYA_RENGO_CONTAINERS_PT = SURYA_RENGO_CONTAINERS_PT['Unnamed: 10'].sum(
        )

        TRISTAR_MAKMUR_KARTONINDO_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                                == 'TRISTAR MAKMUR KARTONINDO, PT']
        jumlah_TRISTAR_MAKMUR_KARTONINDO_PT = TRISTAR_MAKMUR_KARTONINDO_PT['Unnamed: 10'].sum(
        )

        labels4 = ['DAYACIPTA KEMASINDO, PT', 'DUA KELINCI, PT', 'KEDAWUNG SETIA CORRUGATED CARTON BOX INDUSTRIAL, PT', 'MULTIBOX INDAH, PT',
                   'PARAMITRA GUNAKARYA CEMERLANG, PT', 'PURINUSA EKAPERSADA, PT', 'SURYA RENGO CONTAINERS, PT', 'SUPRACOR SEJAHTERA, PT', 'TRISTAR MAKMUR KARTONINDO, PT']
        values4 = [jumlah_DAYACIPTA_KEMASINDO_PT, jumlah_DUA_KELINCI_PT, jumlah_KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT, jumlah_MULTIBOX_INDAH_PT,
                   jumlah_PARAMITRA_GUNAKARYA_CEMERLANG_PT, jumlah_PURINUSA_EKAPERSADA_PT, jumlah_SUPRACOR_SEJAHTERA_PT, jumlah_SURYA_RENGO_CONTAINERS_PT, jumlah_TRISTAR_MAKMUR_KARTONINDO_PT]

        layout4 = go.Layout(title='SPENDING SUMMARY SUPPLIER(MTD Qty)')
        fig4 = go.Figure(
            data=[go.Pie(labels=labels4, values=values4)], layout=layout4)

    return fig4


@app.callback(Output('Mygraph5', 'figure'),
              [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_graph5(contents, filename):
    fig5 = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }

    if contents:
        contents = contents[0]
        filename = filename[0]
        Data_RTS = parse_data(contents, filename)
        Data_RTS['Unnamed: 5'] = Data_RTS['Unnamed: 5'].str.strip().str.upper()
        # CHART5
        DAYACIPTA_KEMASINDO_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                          == 'DAYACIPTA KEMASINDO, PT']
        jumlah_DAYACIPTA_KEMASINDO_PT1 = DAYACIPTA_KEMASINDO_PT['Unnamed: 11'].sum(
        )

        DUA_KELINCI_PT = Data_RTS[Data_RTS['Unnamed: 1'] == 'DUA KELINCI, PT']
        jumlah_DUA_KELINCI_PT1 = DUA_KELINCI_PT['Unnamed: 11'].sum()

        KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                                                      == 'KEDAWUNG SETIA CORRUGATED CARTON BOX INDUSTRIAL, PT']
        jumlah_KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT1 = KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT['Unnamed: 11'].sum(
        )

        MULTIBOX_INDAH_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                     == 'MULTIBOX INDAH, PT']
        jumlah_MULTIBOX_INDAH_PT1 = MULTIBOX_INDAH_PT['Unnamed: 11'].sum()

        PARAMITRA_GUNAKARYA_CEMERLANG_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                                    == 'PARAMITRA GUNAKARYA CEMERLANG, PT']
        jumlah_PARAMITRA_GUNAKARYA_CEMERLANG_PT1 = PARAMITRA_GUNAKARYA_CEMERLANG_PT['Unnamed: 11'].sum(
        )

        PURINUSA_EKAPERSADA_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                          == 'PURINUSA EKAPERSADA, PT']
        jumlah_PURINUSA_EKAPERSADA_PT1 = PURINUSA_EKAPERSADA_PT['Unnamed: 11'].sum(
        )

        SUPRACOR_SEJAHTERA_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                         == 'SUPRACOR SEJAHTERA, PT']
        jumlah_SUPRACOR_SEJAHTERA_PT1 = SUPRACOR_SEJAHTERA_PT['Unnamed: 11'].sum(
        )

        SURYA_RENGO_CONTAINERS_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                             == 'SURYA RENGO CONTAINERS, PT']
        jumlah_SURYA_RENGO_CONTAINERS_PT1 = SURYA_RENGO_CONTAINERS_PT['Unnamed: 11'].sum(
        )

        TRISTAR_MAKMUR_KARTONINDO_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                                == 'TRISTAR MAKMUR KARTONINDO, PT']
        jumlah_TRISTAR_MAKMUR_KARTONINDO_PT1 = TRISTAR_MAKMUR_KARTONINDO_PT['Unnamed: 11'].sum(
        )

        labels5 = ['DAYACIPTA KEMASINDO, PT', 'DUA KELINCI, PT', 'KEDAWUNG SETIA CORRUGATED CARTON BOX INDUSTRIAL, PT', 'MULTIBOX INDAH, PT',
                   'PARAMITRA GUNAKARYA CEMERLANG, PT', 'PURINUSA EKAPERSADA, PT', 'SURYA RENGO CONTAINERS, PT', 'SUPRACOR SEJAHTERA, PT', 'TRISTAR MAKMUR KARTONINDO, PT']
        values5 = [jumlah_DAYACIPTA_KEMASINDO_PT1, jumlah_DUA_KELINCI_PT1, jumlah_KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT1, jumlah_MULTIBOX_INDAH_PT1,
                   jumlah_PARAMITRA_GUNAKARYA_CEMERLANG_PT1, jumlah_PURINUSA_EKAPERSADA_PT1, jumlah_SUPRACOR_SEJAHTERA_PT1, jumlah_SURYA_RENGO_CONTAINERS_PT1, jumlah_TRISTAR_MAKMUR_KARTONINDO_PT1]

        layout5 = go.Layout(title='SPENDING SUMMARY SUPPLIER(YTD Qty)',
                            hovermode='closest')
        fig5 = go.Figure(
            data=[go.Pie(labels=labels5, values=values5)], layout=layout5)

    return fig5


@app.callback(Output('Mygraph6', 'figure'),
              [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_graph6(contents, filename):
    fig6 = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }

    if contents:
        contents = contents[0]
        filename = filename[0]
        Data_RTS = parse_data(contents, filename)
        Data_RTS['Unnamed: 5'] = Data_RTS['Unnamed: 5'].str.strip().str.upper()
        # CHART6
        DAYACIPTA_KEMASINDO_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                          == 'DAYACIPTA KEMASINDO, PT']
        jumlah_DAYACIPTA_KEMASINDO_PT2 = DAYACIPTA_KEMASINDO_PT['Unnamed: 12'].sum(
        )

        DUA_KELINCI_PT = Data_RTS[Data_RTS['Unnamed: 1'] == 'DUA KELINCI, PT']
        jumlah_DUA_KELINCI_PT2 = DUA_KELINCI_PT['Unnamed: 12'].sum()

        KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                                                      == 'KEDAWUNG SETIA CORRUGATED CARTON BOX INDUSTRIAL, PT']
        jumlah_KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT2 = KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT['Unnamed: 12'].sum(
        )

        MULTIBOX_INDAH_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                     == 'MULTIBOX INDAH, PT']
        jumlah_MULTIBOX_INDAH_PT2 = MULTIBOX_INDAH_PT['Unnamed: 12'].sum()

        PARAMITRA_GUNAKARYA_CEMERLANG_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                                    == 'PARAMITRA GUNAKARYA CEMERLANG, PT']
        jumlah_PARAMITRA_GUNAKARYA_CEMERLANG_PT2 = PARAMITRA_GUNAKARYA_CEMERLANG_PT['Unnamed: 12'].sum(
        )

        PURINUSA_EKAPERSADA_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                          == 'PURINUSA EKAPERSADA, PT']
        jumlah_PURINUSA_EKAPERSADA_PT2 = PURINUSA_EKAPERSADA_PT['Unnamed: 12'].sum(
        )

        SUPRACOR_SEJAHTERA_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                         == 'SUPRACOR SEJAHTERA, PT']
        jumlah_SUPRACOR_SEJAHTERA_PT2 = SUPRACOR_SEJAHTERA_PT['Unnamed: 12'].sum(
        )

        SURYA_RENGO_CONTAINERS_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                             == 'SURYA RENGO CONTAINERS, PT']
        jumlah_SURYA_RENGO_CONTAINERS_PT2 = SURYA_RENGO_CONTAINERS_PT['Unnamed: 12'].sum(
        )

        TRISTAR_MAKMUR_KARTONINDO_PT = Data_RTS[Data_RTS['Unnamed: 1']
                                                == 'TRISTAR MAKMUR KARTONINDO, PT']
        jumlah_TRISTAR_MAKMUR_KARTONINDO_PT2 = TRISTAR_MAKMUR_KARTONINDO_PT['Unnamed: 12'].sum(
        )

        labels6 = ['DAYACIPTA KEMASINDO, PT', 'DUA KELINCI, PT', 'KEDAWUNG SETIA CORRUGATED CARTON BOX INDUSTRIAL, PT', 'MULTIBOX INDAH, PT',
                   'PARAMITRA GUNAKARYA CEMERLANG, PT', 'PURINUSA EKAPERSADA, PT', 'SURYA RENGO CONTAINERS, PT', 'SUPRACOR SEJAHTERA, PT', 'TRISTAR MAKMUR KARTONINDO, PT']
        values6 = [jumlah_DAYACIPTA_KEMASINDO_PT2, jumlah_DUA_KELINCI_PT2, jumlah_KEDAWUNG_SETIA_CORRUGATED_CARTON_BOX_INDUSTRIAL_PT2, jumlah_MULTIBOX_INDAH_PT2,
                   jumlah_PARAMITRA_GUNAKARYA_CEMERLANG_PT2, jumlah_PURINUSA_EKAPERSADA_PT2, jumlah_SUPRACOR_SEJAHTERA_PT2, jumlah_SURYA_RENGO_CONTAINERS_PT2, jumlah_TRISTAR_MAKMUR_KARTONINDO_PT2]

        layout6 = go.Layout(title='SPENDING SUMMARY SUPPLIER(MTD Value)',
                            hovermode='closest')
        fig6 = go.Figure(
            data=[go.Pie(labels=labels6, values=values6)], layout=layout6)

    return fig6
