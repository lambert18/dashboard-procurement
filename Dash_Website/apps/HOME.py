from os import link
from dash_bootstrap_components._components.NavLink import NavLink
import dash_html_components as html
import dash_core_components as dcc
from app import app


layout = html.Div(children=[
    html.H1(children='WELCOME TO PROCUREMENT'),
    html.Div([
        html.Div([
            NavLink(
                html.Img(src=app.get_asset_url('raw-material-logo.png'), className="img__style"), 
                href="/apps/PROC", active="exact"
            ),
            NavLink("PROC", href="/apps/PROC", active="exact")
        ], className="display__img"),
        html.Div([
            NavLink(
                html.Img(src=app.get_asset_url('connect.jpg'), className="img__style"), 
                href="/apps/RMPMSS", active="exact"
            ),
            NavLink("RM/PM-SS", href="/apps/RMPMSS", active="exact")
        ], className="display__img"),
        html.Div([
            NavLink(
                html.Img(src=app.get_asset_url('connect.jpg'), className="img__style"), 
                href="/apps/RMPM", active="exact"
            ),
            NavLink("RM/PM", href="/apps/RMPM", active="exact")
        ], className="display__img"),
        html.Div([
            NavLink(
                html.Img(src=app.get_asset_url('connect.jpg'), className="img__style"), 
                href="/apps/CLEARANCE", active="exact"
            ),
            NavLink("CLEARANCE", href="/apps/CLEARANCE", active="exact")
        ], className="display__img"),
        html.Div([
            NavLink(
                html.Img(src=app.get_asset_url('connect.jpg'), className="img__style"), 
                href="/apps/INMKT", active="exact"
            ),
            NavLink("INDIRECT MKT", href="/apps/INMKT", active="exact")
        ], className="display__img"),
        html.Div([
            NavLink(
                html.Img(src=app.get_asset_url('connect.jpg'), className="img__style"), 
                href="/apps/NONMKT", active="exact"
            ),
            NavLink("INDIRECT", href="/apps/NONMKT", active="exact")
        ], className="display__img")
    ], className="display__container")
], className="layout")

app.layout = html.Div([
    dcc.Location(id="url"),
    layout
])