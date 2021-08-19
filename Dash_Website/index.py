from dash_bootstrap_components._components.NavLink import NavLink
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash_html_components.Div import Div
from dash_html_components.Img import Img
from dash_html_components.Nav import Nav

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import HOME, PROC, RMPM, CLEARANCE, INMKT, RMPMSS, NONMKT

sidebar = html.Div(
    [
        html.Div(
            html.Div([
                html.Img(src=app.get_asset_url('logo-kalbe.png'), className="img__logo"),
                html.Hr(),
                dbc.Nav(
                [
                    dbc.NavLink("Home", href="/apps/HOME", active="exact"),
                    dbc.NavLink("PROC", href="/apps/PROC", active="exact"),
                    dbc.NavLink("RM/PM-SS", href="/apps/RMPMSS", active="exact"),
                    dbc.NavLink("RM/PM", href="/apps/RMPM", active="exact"),
                    dbc.NavLink("CLEARANCE", href="/apps/CLEARANCE", active="exact"),
                    dbc.NavLink("INDIRECT MKT", href="/apps/INMKT", active="exact"),
                    dbc.NavLink("INDIRECT NON MKT", href="/apps/NONMKT", active="exact")
                ],
                vertical=True,
                pills=True,
                ),
            ]),
            className="sidebar__style",
        ),
        
    ],
)

content = html.Div(className="content__style", id="page-content", children=[] )

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@ app.callback(Output('page-content', 'children'),
               [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/HOME':
        return HOME.layout
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
        return HOME.layout


if __name__ == '__main__':
    app.run_server(debug=True)
