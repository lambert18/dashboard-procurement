import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import PROC, RMPM, CLEARANCE, INMKT, RMPMSS, NONMKT

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Ini Logo", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("PROC", href="/apps/PROC", active="exact"),
                dbc.NavLink("RM/PM-SS", href="/apps/RMPMSS", active="exact"),
                dbc.NavLink("RM/PM", href="/apps/RMPM", active="exact"),
                dbc.NavLink("CLEARANCE", href="/apps/CLEARANCE", active="exact"),
                dbc.NavLink("INDIRECT MKT", href="/apps/INMKT", active="exact"),
                dbc.NavLink("INDIRECT NON MKT", href="/apps/NONMKT", active="exact"),
            ],
            vertical=True,
            pills=True,
            
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])




# app.layout = html.Div(children=[
#     html.H1(children='Welcome To Procurement', style={
#         "color": "red",
#         "text-align": "center",
#         "background-color": "lightblue",
#         "height": "200px"
#     }),
#     html.Div([
#         dcc.Location(id='url', refresh=False),
#         html.Div([
#             dcc.Link('PROC', href='/apps/PROC', className="link"), 
#             dcc.Link('RM/PM-SS', href='/apps/RMPMSS', className="link"),
#             dcc.Link('RM/PM', href='/apps/RMPM', className="link"),
#             dcc.Link('CLEARANCE', href='/apps/CLEARANCE', className="link"),
#             dcc.Link('INDIRECT MKT', href='/apps/INMKT', className="link"),
#             dcc.Link('INDIRECT NON MKT', href='/apps/NONMKT', className="link"),
#         ], className="menu"),
#         html.Div(id='page-content', children=[]),
#     ])])


@ app.callback(Output('page-content', 'children'),
               [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/RMPM':
        return RMPM.layout
    if pathname == '/apps/PROC':
        return PROC.layout
    if pathname == '/apps/CLEARANCE':
        return CLEARANCE.layout
    if pathname == '/apps/INMKT':
        return INMKT.layout
    if pathname == '/apps/RMPMSS':
        return RMPMSS.layout
    if pathname == '/apps/NONMKT':
        return NONMKT.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)
