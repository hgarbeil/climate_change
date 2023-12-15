import pandas as pd
import datetime



class Process_Temp :
    def __init__(self):
        skiprowval = (2023 - 1850)*12+180
        global_file = 'https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_complete.txt'
        global_df = pd.read_csv(global_file,skiprows=skiprowval,sep='\s\s+')
        global_df.columns=['Year','Month','Anomaly','Uncertainty','Annual_Anom','Annual_Unc','5Yr_Annom','5Yr_Unc',
             '10Yr_Annom','10Yr_Unc','20Yr_Annom','20Yr_Unc']
        print(global_df.head(30))
        global_df['Year']=global_df['Year'].astype(int)
        self.global_df = global_df[global_df.Year>1860]
        # create the date column
        self.parse_time() 
        

    def parse_time (self):
         self.global_df['Date']=pd.to_datetime(dict(year=self.global_df.Year,month=self.global_df.Month,day=15))


    def df_limit(self,startyear, endyear):
        temp_df = self.global_df[(self.global_df.Year>=startyear)&(self.global_df.Year<=endyear)]
        return temp_df

pt = Process_Temp()