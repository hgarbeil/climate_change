import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import plotly.express as px
import datetime
import panel as pn

countries = ['World','United States','Russia','China','Australia','Japan','Germany','India','United Kingdom', 'France','Indonesia','Iceland']
greenhouse_gases=['CarbonDioxide','Methane','NitrousOxide','FluorinatedGases']
gases_pct=[79.4,11.5,6.2,3.0]
country_component =['country','year','iso_code','population',
            'co2','co2_per_gdp','co2_per_capita','cement_co2','coal_co2','oil_co2','gas_co2',
            'methane']


class Process_CO2 :

    

    def __init__(self) :
        # maunaloa data
        self.mloafile = 'https://scrippsco2.ucsd.edu/assets/data/atmospheric/stations/in_situ_co2/monthly/monthly_in_situ_co2_mlo.csv'
        self.mloa_df = ''
        self.mix_df = ''
        self.create_df()
        # energy mix --- needs pre-processing
        self.energyfile = 'per-capita-energy-stacked.csv'
        self.create_energy_df()
        self.create_co2_mix_df() 
        

    def create_df (self):
        mloa_df = pd.read_csv(self.mloafile,skiprows=80)
        mloa_df=mloa_df.drop(mloa_df.iloc[:,6:],axis=1)
        mloa_df.columns=['Yr','Mn','EDy','Day','CO2','CO2_trend']
        self.mloa_df=mloa_df[mloa_df.Yr > 1960]
        self.mloa_df['Date']=pd.to_datetime(dict(year=mloa_df.Yr,month=mloa_df.Mn,day=15))

    def create_energy_df (self):
        dfmix = pd.read_csv(self.energyfile)
        self.mix_df = dfmix[dfmix.Entity.isin(countries)]
        self.mix_df.columns=['country','code','year','coal','oil','gas','nuclear','hydro','wind','solar','other']
        self.mix_df=self.mix_df.dropna()

    def create_co2_mix_df(self) :
    
        # df = pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv')
        # cache data to improve dashboard performance
        if 'data' not in pn.state.cache.keys():

            df = pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv')

            pn.state.cache['data'] = df.copy()

        else: 

            df = pn.state.cache['data'] 
        # data cleanup
        df=df.fillna(0)
        df_major=df[(df['country'].isin(countries)) & (df['year']>1940)]
        df_countries_full=df[df.iso_code!='0']
        df_countries=df_countries_full[df_countries_full.year==2018]
        self.df_countries = df_major
        self.co2_comp_world=df[df['country']=='World']
        self.df_countries_full=df_countries_full[country_component]
        print(self.co2_comp_world.columns)
        self.co2_comp_df = df
        
    def limit_dates (self, min_year, max_year):
        min = datetime.date (min_year,1,1)
        max = datetime.date (max_year,12,31)   
        newdf = self.mloa_df[(self.mloa_df.Yr >= min_year) & (self.mloa_df.Yr<=max_year)]
        return newdf

# my_co2 = Process_CO2()
# df = my_co2.create_df()
# newdf = my_co2.limit_dates(2000,2020)
# print(df.head(10))
# fig = px.line(newdf,x='Date',y=['CO2','CO2_trend'],range_y=[300,450])
# fig.show()