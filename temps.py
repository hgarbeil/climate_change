import pandas as pd
import numpy as np
import plotly.express as px
from dash import dash, dcc, html, Output, Input, dash_table
import dash_bootstrap_components as dbc
from process_co2 import *


## Define the app and hook in bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)


app.layout = dbc.Container([
    dbc.Row([
         dbc.Col([
            html.H1('Climate Change and Atmospheric CO2', className='text-center text-primary mb-2 mt-2')

         ], width=12)
    ]),

],fluid=True,style={"backgroundColor":'rgb(204,204,204)'}
)

if __name__=="__main__":
    app.run_server(debug=True)
