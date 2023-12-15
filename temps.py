import pandas as pd
import numpy as np
import plotly.express as px
from dash import dash, dcc, html, Output, Input, dash_table
import dash_bootstrap_components as dbc
from process_temp import *



temps = Process_Temp()
fig_global = px.line (temps.global_df, x='Date',y='Anomaly')

## Define the app and hook in bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)


app.layout = dbc.Container([
    dbc.Row([
         dbc.Col([
            html.H1('Climate Change and Temperature', className='text-center text-primary mb-2 mt-2')

         ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H5("Global Temperature",className='text-center mb-2 mt-2 text-primary'),
            html.H6("Year Range : ",className='text-center mb-2 text-primary'),
            # dcc.RangeSlider(1860,2023,1,value=[1960,2023],id='year_rangeslider',
            #     marks={
            #         1900:'1900',
            #         1940:'1940',
            #         1980:'1980',
            #         2020:'2020'}),
            html.H6("Start Year",className='text-center mb-2 text-primary'), 
            dcc.Input(id='input_startyear',value=1860, type="number",style={'maxWidth':'90%'}),
            html.H6("End Year",className='text-center mb-2 text-primary'), 
            dcc.Input(id='input_endyear',value=2022, type="number",style={'maxWidth':'90%'})
        ],xs=11,sm=11,md=2,className='bg-light text-dark border '),
        dbc.Col([
            dcc.Graph (id='graph_global',figure=fig_global),
            html.Div(["Data is from Berkeley Earth Global Warming ",
                html.A("High Resolution Time Series Data", 
                   href='https://berkeleyearth.org/data/', target="_blank")
            ])
        ],xs=11,sm=12,md=10)
    ])

],fluid=True,style={"backgroundColor":'rgb(204,204,204)'}
)

# @app.callback(
#     [
#         Output('input_startyear','value'),
#         Output('input_endyear','value')
#     ],
#     [
#         Input('year_rangeslider','value')
#     ]
# )
# def yearslider_cback(limits):
#     return ([limits[0],limits[1]])

@app.callback(
    [
        Output('graph_global','figure')

    ],
    [
        Input('input_startyear','value'),
        Input('input_endyear','value')
    ]
)
def update_globalplot(year0, year1):
    temp_df = pt.df_limit(year0,year1)
    tmp_fig = px.line(temp_df,x='Date',y='Anomaly',title='Global Temperature Anomaly')
    tmp_fig.update_layout(yaxis={'title':'Temp Anomaly (Deg C)'},plot_bgcolor='rgb(200,200,0)')
    return ([tmp_fig])






if __name__=="__main__":
    app.run_server(debug=True)
