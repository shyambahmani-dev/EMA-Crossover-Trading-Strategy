import numpy as np
import pandas as pd
import matplotlib as mpl
import yfinance as yf
import datetime
import csv
import os
import code
import time
from dateutil.relativedelta import relativedelta
from pandas import ExcelWriter
import inline
import traceback
import warnings
warnings.filterwarnings("ignore")


"""

try:
    
    data1name = str("^NSEI") #tickername
    ticker1name = data1name
    ticker1 = yf.Ticker(ticker1name)
    startdate = datetime.date.today() - relativedelta(days = 7) - relativedelta(years = 15)
    enddate = datetime.date.today() + relativedelta(days = 1)

    #startdate = datetime.date(2018, 12, 29)
    #enddate = datetime.date(2021 , 1, 7)

except Exception as exp:
    
    print(exp)
    input()

"""



#### -- Get OHLC -- ####


def tickerData(symbol, period = '0', interval = '1d', startdate = datetime.date.today() - relativedelta(days = 57), enddate = datetime.date.today()):

    try:

        #print("\n\n\n\nThe Stock in analysis is %s\n\n\n\n" %(symbol))


        ticker1 = yf.Ticker(symbol)

        #startdate = datetime.date.today() - relativedelta(days = 7) - relativedelta(years = 15)
        #enddate = datetime.date.today() + relativedelta(days = 1)


        if(period == '0'):

            if interval in ('1m', '2m,' '5m', '15m', '30m', '1h'):
                
                if interval == '1m':
                    days = 7 
                elif interval == '1h':
                    days = 720
                else:
                    days = 57
                
                start_date = datetime.datetime.now()-datetime.timedelta(days=days)
                    
                data1 = pd.DataFrame( ticker1.history( period = period, interval = interval, start= start_date, end= datetime.datetime.today() ) )

            else:

                data1 = pd.DataFrame( ticker1.history( period = '1d' , interval = interval ) )
            
        else:

            if interval in ('1m', '2m,' '5m', '15m', '30m', '1h'):
                
                if interval == '1m':
                    days = 7 
                elif interval == '1h':
                    days = 720
                else:
                    days = 57
                
                start_date = datetime.datetime.now()-datetime.timedelta(days=days)
                    
                data1 = pd.DataFrame( ticker1.history( period = period, interval = interval, start= start_date, end= datetime.datetime.today() ) )
            
            else:

                data1 = pd.DataFrame( ticker1.history( interval = interval, period = period) )


        data1 = data1.astype(dtype={'Open':float, 'High':float, 'Low':float, 'Close':float, 'Volume':float})
        
        data1kindex = data1.index.values
        loda = np.array([])
        for i in data1kindex:
            i = pd.to_datetime(i)
            loda = np.append(loda,i)
        data1.index = loda
        
        #print("Dataset of %f values from %s to %s: \n%s\n\n\n" %(data1.size, startdate , enddate , data1) )

        if(data1.size == 0):
            print("Error fetching data, please check if symbol exists")

        return data1


    except Exception as exp:
        
        print(exp)
        input()


#### -- Get OHLC -- ####






