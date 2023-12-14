import pandas as pd
import datetime



class Process_Temp :
    def __init__(self):
        global_file = 'https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_complete.txt'
        global_df = pd.read_csv(global_file,skiprows=98,sep='\s\s+')
        global_df.columns={'Year','Month','Anomaly','Uncertainty','Annual_Anom','Annual_Unc','5Yr_Annom','5Yr_Unc',
             '10Yr_Annom','10Yr_Unc','20Yr_Annom','20Yr_Unc'}
        self.global_df = global_df
        self.parse_time() 
        

    def parse_time (self):
        date = datetime.date(self.global_df.Year, self.global_df.Month,15)
        self.global_df['Date'] = date



pt = Process_Temp()