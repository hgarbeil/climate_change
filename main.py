
import pandas as pd
import numpy as np
import plotly.express as px
from dash import dash, dcc, html, Output, Input, dash_table
import dash_bootstrap_components as dbc
from process_co2 import *

 
countries_major=['United States','Russia','China','India']

component_map=['population',
            'co2','co2_per_gdp','co2_per_capita','cement_co2','coal_co2','oil_co2','gas_co2',
            'methane']

CONTENT_STYLE = {
    # "margin-left": "2rem",
    # "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Mauna Loa CO2 Measurements
pc = Process_CO2() 
mloa_df = pc.limit_dates(1960,2022)

fig_mloa=px.line(pc.mloa_df,x='Date',y=['CO2','CO2_trend'],title='Global CO2 Concentration',range_y=[300,450]
        )
fig_mloa.update_layout(yaxis={'title':'CO2 PPM'},legend={'title':'Component'},plot_bgcolor='rgb(200,200,0)')

fig_compos=px.pie(names=greenhouse_gases,values=gases_pct,title='Human-Caused Greenhouse Gas Composition')

fig_ts = px.line(pc.df_countries,x='year',y='co2',color='country')

df_temp = pc.df_countries_full[pc.df_countries_full.year==2020]
fig_choro=px.choropleth(df_temp,locations='iso_code',color='co2',
    color_continuous_scale=px.colors.sequential.Plasma, range_color=(0,10000))

tmp_df = pc.df_countries[(pc.df_countries.year == 2018)]
fig_makeup = px.bar(tmp_df, x='country',y=['coal_co2','gas_co2','oil_co2','cement_co2'],
    barmode='group',
    title='CO2 Makeup')

## Define the app and hook in bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

server = app.server



app.layout = dbc.Container([
    dbc.Row([
         dbc.Col([
            html.H1('Climate Change and Atmospheric CO2', className='text-center text-primary mb-2 mt-2')

         ], width=12)

         

    ]),
    dbc.Row([
        dbc.Col([
            html.H5("Global CO2",className='text-center mb-2 mt-2 text-primary'),
            html.H6("Year Range : ",className='text-center mb-2 text-primary'),
            dcc.RangeSlider(1980,2020,1,value=[1960,2020],id='year_rangeslider',
                marks={
                    #1970:'1970',
                    1980:'1980',
                    #1990:'1990',
                    2000:'2000',
                    #2010:'2010',
                    2020:'2020'})
        ],xs=11,sm=9,md=2,className='bg-light text-dark border '),
        dbc.Col([
           
            
            dcc.Graph(id='mloa_graph', figure=fig_mloa),
            html.Div(["Data is from the ",
                html.A("NOAA Global Monitoring Laboratory", 
                   href='https://gml.noaa.gov/ccgg/trends/gl_data.html', target="_blank")
            ]
            )
        ],
            
        xs=12,sm=10,md=5,className='bg-light text-dark border'),
        dbc.Col([
            dcc.Graph(id='ghg_compos', figure=fig_compos),
            html.Div(["Data is from NRDC ",
                html.A("Greenhouse Effect 101 ", 
                   href='https://www.nrdc.org/stories/greenhouse-effect-101#whatis', target="_blank")
            ]
            )
        ],
            
        xs=12,sm=12,md=5,className='bg-light text-dark border')

    ], justify='evenly',className="mb-3"),
    

    dbc.Row([
        dbc.Col([
            html.H5("CO2 Production",className='text-center mb-2 mt-2 text-primary'),
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

        ],xs=11,sm=11,md=2,className='bg-light text-dark border'),
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
        ],xs=12,sm=12,md=5,className='bg-light text-dark border'),
        dbc.Col([

            dcc.Graph(id='co2_makeup', figure=fig_makeup)

        ],xs=12,sm=12,md=5,className='bg-light text-dark border')

    ], justify='evenly',class_name="mb-3"

    ),
    dbc.Row([
        dbc.Col([
            html.H5("Country Analysis",className='text-center mt-2 mb-2 text-primary'),
            html.H6("Year",className='text-center mb-2 text-primary'),
            dcc.Dropdown(np.arange(1980,2022,1), value=2018, id='mapyr_ddown'),
            html.H6("Component",className='text-center mb-2 text-primary'),
            dcc.Dropdown(component_map,'co2',id='mapvar_ddown')

        ],xs=12,sm=12,md=2,className='bg-light text-dark border'),
        dbc.Col([
            dcc.Graph(id='map_co2',figure=fig_choro),
            html.Div(["Data is from the ",
                html.A("Our World in Data", 
                   href='https://github.com/owid/co2-data', target="_blank"), 
                " CO2 Data Github Page."])
        ],xs=12,sm=12,md=5,className='bg-light text-dark border'),
        dbc.Col([
            html.Div(id='table1')
            #dash_table.DataTable(df_temp[['country','year','co2']].to_dict('records'), [{"name": i, "id": i} for i in ['country','year','co2']])
        ],xs=12,sm=12,md=5,className='bg-light text-dark border',style=CONTENT_STYLE)
    ])
],fluid=True,style={"backgroundColor":'rgb(204,204,204)'})


@app.callback(
    [Output('co2_ts_graph','figure'),
     Output('co2_makeup','figure')]
    ,
    [Input('co2_countries_clist','value'),
     Input('year_rangeslider_ts',"value")]
     
)
def update_co2_ts(count_selected,yearrange):
    tmp_df = pc.df_countries[(pc.df_countries['country'].isin(count_selected))&
            (pc.df_countries.year>=yearrange[0])&(pc.df_countries.year<=yearrange[1])]
    tmpyr_df = tmp_df[(tmp_df.country.isin(count_selected)) & (tmp_df.year==2018)]
    tmp_fig = px.line(tmp_df,x='year',y='co2',color='country')
    tmp_fig.update_layout(yaxis={'title':'MTonnes CO2'},legend={'title':'CO2 Production'},plot_bgcolor='rgb(210,210,210)')
    tmp_fig1 = px.bar(tmpyr_df, x='country',y=['coal_co2','gas_co2','oil_co2','cement_co2'],
        barmode='group',title='CO2 Sources')
    tmp_fig1.update_layout(yaxis={'title':'MTonnes CO2'})
    return(tmp_fig, tmp_fig1)

@app.callback(
    Output('mloa_graph','figure')
    ,
    [Input('year_rangeslider','value')]
     
)
def update_mloa(yearrange):
    min_year= yearrange[0]
    max_year= yearrange[1]
    tmp_df = pc.mloa_df[(pc.mloa_df.Yr >= min_year) & (pc.mloa_df.Yr<=max_year)]
    tmp_fig=px.line(tmp_df,x='Date',y=['CO2','CO2_trend'],title='Global CO2 Concentration',range_y=[300,450])
    tmp_fig.update_layout(yaxis={'title':'CO2 PPM'},legend={'title':'Component'},plot_bgcolor='rgb(200,200,200)')
    return(tmp_fig)

@app.callback(
    [
        Output('map_co2','figure'),
        Output('table1','children')
    ],
    [
        Input('mapyr_ddown','value'),
        Input('mapvar_ddown','value')
    ]
)
def update_map(year, comp):
    df_temp = pc.df_countries_full[(pc.df_countries_full.year==year) & (pc.df_countries_full.country!='World')]
    maxval = df_temp[df_temp.country.isin(countries_major)][comp].max()
    fig_choro=px.choropleth(df_temp,locations='iso_code',color=comp,
        color_continuous_scale=px.colors.sequential.Plasma,range_color=[0,maxval],hover_data=['country',comp])
    
    newcols=df_temp[df_temp.iso_code!=0]
    if comp != 'co2' :
        newcols = newcols[['country',comp,'co2']]
    else :
        newcols = newcols[['country',comp,'methane']]
    newcols=newcols.sort_values(comp,ascending=False)[0:15]
    dtable = dash_table.DataTable(newcols.to_dict('records'), [{"name": i, "id": i} for i in newcols.columns],
        style_cell={'textAlign': 'left'},
        style_cell_conditional=[
        {
            'if': {'column_id': 'country'},
            'textAlign': 'left'
        }],
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
        ],
        style_header={
        'backgroundColor': 'rgb(210, 210, 80)',
        'color': 'black',
        'fontWeight': 'bold'
         }
        
    )

    print (newcols.head(10))

    return(fig_choro,dtable)

if __name__=="__main__":
    app.run_server(debug=True)
