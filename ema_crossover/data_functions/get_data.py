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


def tickerData(symbol, period = '0', interval = '1d', startdate = datetime.date.today() - relativedelta(days = 7) - relativedelta(years = 10), enddate = datetime.date.today() + relativedelta(days = 1)):

    try:

        print("\n\n\n\nThe Stock in analysis is %s\n\n\n\n" %(symbol))


        ticker1 = yf.Ticker(symbol)
        #startdate = datetime.date.today() - relativedelta(days = 7) - relativedelta(years = 15)
        #enddate = datetime.date.today() + relativedelta(days = 1)

        if(period != '0'):
            data1 = pd.DataFrame( ticker1.history(  period = period , interval = interval) )
            
        else:
            data1 = pd.DataFrame( ticker1.history( start = startdate , end = enddate, interval = interval) )
        
        data1kindex = data1.index.values
        loda = np.array([])
        for i in data1kindex:
            i = pd.to_datetime(i)
            loda = np.append(loda,i)
        data1.index = loda
        data1 = data1.loc[startdate:enddate,:]
        data1size = len(data1.index)
        
        print("Dataset from %s to %s: \n%s\n\n\n" %(startdate , enddate , data1) )

        return data1


    except Exception as exp:
        
        print(exp)
        input()


#### -- Get OHLC -- ####






