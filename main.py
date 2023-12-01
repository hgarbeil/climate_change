
import pandas as pd
import panel as pn
import numpy as np
import plotly.express as px
from dash import dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
from process_co2 import *

 

# Mauna Loa CO2 Measurements
pc = Process_CO2() 
mloa_df = pc.limit_dates(1960,2022)
#print (pc.co2_comp_df.columns)

fig_mloa=px.line(pc.mloa_df,x='Date',y=['CO2','CO2_trend'],title='Mauna Loa CO2 Measurements',range_y=[300,450]
        )
fig_mloa.update_layout(yaxis={'title':'CO2 PPM'},legend={'title':'Component'},plot_bgcolor='rgb(200,200,0)')

fig_ts = px.line(pc.df_countries,x='year',y='co2',color='country')

## Define the app and hook in bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)



app.layout = dbc.Container([
    dbc.Row([
         dbc.Col([
            html.H1('Atmospheric CO2', className='text-center text-primary mb-4')
         ], width=12)
         

    ]),
    dbc.Row([
        dbc.Col([
            html.H5("Mauna Loa CO2",className='text-center mb-2 text-primary'),
            html.H6("Year Range : ",className='text-center mb-2 text-primary'),
            dcc.RangeSlider(1960,2020,1,value=[1960,2020],id='year_rangeslider',
                marks={
                    #1970:'1970',
                    1980:'1980',
                    #1990:'1990',
                    2000:'2000',
                    #2010:'2010',
                    2020:'2020'})
        ],xs=11,sm=2,md=2,className='bg-light text-dark border'),
        dbc.Col([
           
            
            dcc.Graph(id='mloa_graph', figure=fig_mloa),
            html.Div(["Data is from the ",
                html.A("Scripps UCSD CO2 Program", 
                   href='https://scrippsco2.ucsd.edu/data/atmospheric_co2/primary_mlo_co2_record.html', target="_blank")
            ]
            )
        ],
            
            xs=12,sm=9,md=9,className='bg-light text-dark border')

    ], justify='evenly',className="mb-3"),
    dbc.Row([
        dbc.Col([
            html.H5("CO2 Production",className='text-center mb-2 text-primary'),
            html.H6("Year Range : ",className='text-center mb-2 text-primary'),
            dcc.RangeSlider(1940,2025,1,value=[1940,2025],id='year_rangeslider_ts',
                marks={
                    1960:'1960',
                    #1970:'1970',
                    1980:'1980',
                    #1990:'1990',
                    2000:'2000',
                    #2010:'2010',
                    2020:'2020'}),
            dcc.Checklist(countries,value=['World','China','United States'],id='co2_countries_clist')

        ],xs=11,sm=2,md=2,className='bg-light text-dark border'),
        dbc.Col([
            dcc.Graph(id='co2_ts_graph',figure=fig_ts),
            html.Div(["Data is from the ",
                html.A("Our World in Data", 
                   href='https://github.com/owid/co2-data', target="_blank"), 
                " CO2 Data Github Page.",
                " ",
                html.A("This project homepage", 
                       href='https://ourworldindata.org/co2-and-greenhouse-gas-emissions',
                       target="_blank"),
                " fully describes their dataset and has a wealth of CO2 information"
            ])
        ],xs=12,sm=9,md=9,className='bg-light text-dark border')
    ], justify='evenly',class_name="mb-3"

    )
],fluid=True)


@app.callback(
    Output('co2_ts_graph','figure')
    ,
    [Input('co2_countries_clist','value'),
     Input('year_rangeslider_ts',"value")]
     
)
def update_co2_ts(count_selected,yearrange):
    tmp_df = pc.df_countries[(pc.df_countries['country'].isin(count_selected))&
            (pc.df_countries.year>=yearrange[0])&(pc.df_countries.year<=yearrange[1])]
    tmp_fig = px.line(tmp_df,x='year',y='co2',color='country')
    tmp_fig.update_layout(yaxis={'title':'MTonnes CO2'},legend={'title':'CO2 Production'},plot_bgcolor='rgb(210,210,210)')
    return(tmp_fig)

@app.callback(
    Output('mloa_graph','figure')
    ,
    [Input('year_rangeslider','value')]
     
)
def update_mloa(yearrange):
    min_year= yearrange[0]
    max_year= yearrange[1]
    tmp_df = pc.mloa_df[(pc.mloa_df.Yr >= min_year) & (pc.mloa_df.Yr<=max_year)]
    tmp_fig=px.line(tmp_df,x='Date',y=['CO2','CO2_trend'],title='Mauna Loa CO2 Measurements',range_y=[300,450])
    tmp_fig.update_layout(yaxis={'title':'CO2 PPM'},legend={'title':'Component'},plot_bgcolor='rgb(200,200,200)')
    return(tmp_fig)

if __name__=="__main__":
    app.run_server(debug=True)
