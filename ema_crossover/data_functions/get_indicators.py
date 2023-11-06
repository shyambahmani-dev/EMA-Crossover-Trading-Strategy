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





## -- DMA -- ##


def getDMA(data1, intervals = [10, 25, 50, 100, 200]):

    try:

        data1DMA = pd.DataFrame()

        for it in intervals:

            data1DMA["DMA%d" %(it)] = data1["Close"].rolling(it).mean()

        return data1DMA

    except Exception as exp:
        
        print(exp)
        input()

## -- DMA -- ##








## -- EMA -- ##

def getEMA(data1, intervals = [10, 25, 50, 100, 200]):

    try:

        data1EMA = pd.DataFrame()

        for it in intervals:

            data1EMA["EMA%d" %(it)] = data1["Close"].ewm( span = it ).mean()

        return data1EMA

    except Exception as exp:
        
        print(exp)
        input()


## -- EMA -- ##







## -- RSI -- ##


def getRSI(data1):

    try:

        pd.options.mode.chained_assignment = None
        
        data1RSI = pd.DataFrame() # columns = data1.columns , index = data1.index )
        data1RSI["Change"] = data1["Close"].copy().diff()
        
        data1RSI["Gain"] = [0]*len(data1["Close"].index)
        data1RSI["Loss"] = [0]*len(data1["Close"].index)
        
        
        for i in data1["Close"].diff().index:
        
            if data1["Close"].diff().loc[i] > 0:
                
                data1RSI["Gain"].loc[i] = data1["Close"].copy().diff().loc[i]
            
            elif data1["Close"].diff().loc[i] < 0:
                
                data1RSI["Loss"].loc[i] = abs(data1["Close"].copy().diff().loc[i])
            
            else:
                
                data1RSI["Gain"].loc[i] = float(0)
                data1RSI["Loss"].loc[i] = float(0)
        
        data1RSI["Avg Gain"] = data1RSI["Gain"].rolling(window = 14).mean()
        data1RSI["Avg Loss"] = data1RSI["Loss"].rolling(window = 14).mean()
        data1RSI["RS"] = data1RSI["Avg Gain"]/data1RSI["Avg Loss"]
        
        data1RSI["RSI"] = ( 100 - ( 100/(1 + data1RSI["RS"]) ) )                

        return data1RSI


    except Exception as exp:
        
        print(exp)
        input()



## -- RSI Done -- ##







## -- Bollinger Bands -- ##

def getBB(data1, interval = 10):

    try:

        data1BB = pd.DataFrame()

        data1BB["1STDUP"] = data1["Close"].rolling(window = interval).mean() + data1["Close"].rolling(window = interval).std()
        data1BB["1STDDN"] = data1["Close"].rolling(window = interval).mean() - data1["Close"].rolling(window = interval).std()
        
        data1BB["2STDUP"] = data1["Close"].rolling(window = interval).mean() + 2*(data1["Close"].rolling(window = interval).std())
        data1BB["2STDDN"] = data1["Close"].rolling(window = interval).mean() - 2*(data1["Close"].rolling(window = interval).std())

        data1BB["3STDUP"] = data1["Close"].rolling(window = interval).mean() + 3*(data1["Close"].rolling(window = interval).std())
        data1BB["3STDDN"] = data1["Close"].rolling(window = interval).mean() - 3*(data1["Close"].rolling(window = interval).std())


        return data1BB
    

    except Exception as exp:
        
        print(exp)
        input()



## -- Bollinger Bands Done -- ##

