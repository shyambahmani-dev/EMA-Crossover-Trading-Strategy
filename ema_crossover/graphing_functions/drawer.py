import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.widgets as mplw
import matplotlib.figure as mplf
import matplotlib.animation as mplani
import yfinance as yf
import datetime
import csv
import os
import code
import scipy as sp
import scipy.stats as stats
import math
from matplotlib.backends.backend_pdf import PdfPages, FigureCanvasPdf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import time
from dateutil.relativedelta import relativedelta
from pandas import ExcelWriter
import glob
import inline
import tkinter as tk
import pickle
import keyboard
import traceback

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score



def ohlcplot(data1, ax, fig):
    

    try:

        data1ohlc = pd.DataFrame()
        data1ohlc["OmC"] = data1["Open"].copy()
        data1ohlc["CmO"] = data1["Close"].copy()
        data1ohlc["HmO"] = data1["High"].copy()
        data1ohlc["LlC"] = data1["Low"].copy()
        data1ohlc["HmC"] = data1["High"].copy()
        data1ohlc["LlO"] = data1["Low"].copy()
        
            
        for i in data1.index:

            if data1["Open"].loc[i] >= data1["Close"].loc[i]:

                data1ohlc["OmC"].loc[i] = data1["Open"].loc[i] - data1["Close"].loc[i]
                data1ohlc["HmO"].loc[i] = data1["High"].loc[i] - data1["Open"].loc[i]
                data1ohlc["LlC"].loc[i] = data1["Close"].loc[i] - data1["Low"].loc[i]
                data1ohlc["CmO"].loc[i] = int(0)
                data1ohlc["HmC"].loc[i] = int(0)
                data1ohlc["LlO"].loc[i] = int(0)
                
            elif data1["Close"].loc[i] >= data1["Open"].loc[i]:

                data1ohlc["CmO"].loc[i] = data1["Close"].loc[i] - data1["Open"].loc[i]
                data1ohlc["HmC"].loc[i] = data1["High"].loc[i] - data1["Close"].loc[i]
                data1ohlc["LlO"].loc[i] = data1["Open"].loc[i] - data1["Low"].loc[i]
                data1ohlc["OmC"].loc[i] = int(0)
                data1ohlc["HmO"].loc[i] = int(0)
                data1ohlc["LlC"].loc[i] = int(0)
    
        ax.bar(data1.index , data1ohlc["OmC"] , bottom = data1["Close"] , color = "red" , width = 0.7)
        ax.bar(data1.index , data1ohlc["CmO"] , bottom = data1["Open"] , color = "green" , width = 0.7)

        ax.bar(data1.index , data1ohlc["HmO"] , bottom = data1["Open"] , color = "red" , width = 0.2)
        ax.bar(data1.index , data1ohlc["HmC"] , bottom = data1["Close"] , color = "green" , width = 0.2)

        ax.bar(data1.index , data1ohlc["LlC"] , bottom = data1["Low"] , color = "red" , width = 0.2)
        ax.bar(data1.index , data1ohlc["LlO"] , bottom = data1["Low"] , color = "green" , width = 0.2)

        marginandstuffOHLC(data1, ax, fig)
        marginandstuffforx(data1, ax, fig)

    except Exception as exp:
        
        print(exp)
        input()



try:

    def marginandstuff(data1, ax, fig):
        
        """
        
        ax.set_xlim( -50 , len(data1.index) + 50 )
        ax.set_xticks(data1.index[::10])
        ax.set_xticklabels(data1["Date"].iloc[::10] , rotation = 60 )
        
        #"""
        
        
        #"""

        startdate = data1.index[0]
        enddate = data1.index[-1]
        
        ax.set_xlim(startdate - datetime.timedelta(days = 50) , enddate + datetime.timedelta(days = 50))

        month = mdates.MonthLocator(interval=1)
        month_format = mdates.DateFormatter('%d-%m-%y')
        
        days = mdates.DayLocator(interval=1)
        day_format = mdates.DateFormatter("%d-%m-%y")

        ax.xaxis.grid(True, which = 'major')

        ax.xaxis.set_major_locator(month)
        ax.xaxis.set_major_formatter(month_format)
        
        ax.xaxis.set_minor_locator(days)
        
        fig.autofmt_xdate()
        
        #"""

        ax.set_ylim( data1.iloc[:,0].min() - (data1.iloc[:,0].mean()/100), data1.iloc[:,0].max() + data1.iloc[:,0].mean()/100)


except Exception as exp:
    
    print(exp)
    input()






try:

    def marginandstuffOHLC(data1, ax, fig):
        
        """
        
        ax.set_xlim( -50 , len(data1.index) + 50 )
        ax.set_xticks(data1.index[::10])
        ax.set_xticklabels(data1["Date"].iloc[::10] , rotation = 60 )
        
        #"""
        
        
        #"""

        startdate = data1.index[0]
        enddate = data1.index[-1]
        
        ax.set_xlim(startdate - datetime.timedelta(days = 50) , enddate + datetime.timedelta(days = 50))

        month = mdates.MonthLocator(interval=1)
        month_format = mdates.DateFormatter('%d-%m-%y')
        
        days = mdates.DayLocator(interval=1)
        day_format = mdates.DateFormatter("%d-%m-%y")

        ax.xaxis.grid(True, which = 'major')

        ax.xaxis.set_major_locator(month)
        ax.xaxis.set_major_formatter(month_format)
        
        ax.xaxis.set_minor_locator(days)
        
        fig.autofmt_xdate()
        
        #"""

        magofdata1 = getMag(data1)

        for i in np.arange( rounddown(data1["Low"].min() - (data1["Close"].mean()/100), data1) , roundup(data1["High"].max() + (data1["Close"].mean()/100), data1) , magofdata1):
            ax.axhline( y = i , linewidth = 0.1 )

        ax.set_ylim( rounddown(data1["Low"].min() - (data1["Close"].mean()/100), data1) , roundup(data1["High"].max() + (data1["Close"].mean()/100), data1) )
        ax.set_yticks( np.arange( rounddown(data1["Low"].min() - (data1["Close"].mean()/100), data1) , roundup(data1["High"].max() + (data1["Close"].mean()/100), data1) , magofdata1) )


except Exception as exp:
    
    print(exp)
    input()



try:
    

    def marginandstuffforx(data1, ax, fig):

        startdate = data1.index[0]
        enddate = data1.index[-1]

        
        ax.set_xlim(startdate - datetime.timedelta(days = 50) , enddate + datetime.timedelta(days = 50))

        month = mdates.MonthLocator(interval=1)

        month_format = mdates.DateFormatter('%d-%m-%y')

        ax.xaxis.grid(True, which = 'major')

        ax.xaxis.set_major_locator(month)
        ax.xaxis.set_major_formatter(month_format)
        
        fig.autofmt_xdate()


except Exception as exp:
    
    print(exp)
    input()



try:

    def getMag(data1):

            lastprice = float(data1["Close"].tail(1))
            magoften = 1 #np.array([1,10,100,1000,10000,100000,1000000,1000000,100000000,1000000000,10000000000,100000000000,1000000000000])
            magofdata1 = 1

            while True:
                    
                if int(lastprice/magoften) == 0:
                    magofdata1 = magoften
                    break
                
                else:
                
                    magoften = magoften*10
            
            magofdata1 = magofdata1/100

            return magofdata1
    
    
except Exception as exp:
    
    print(exp)
    input()

try:

    def roundup(n, data1):
        
        # Smaller multiple
        magofdata1 = getMag(data1)
        a = (n // magofdata1) * magofdata1
        
        # Larger multiple
        b = a + magofdata1
        
        return b
        
    def rounddown(n, data1):
        
        magofdata1 = getMag(data1)
        # Smaller multiple
        a = (n // magofdata1) * magofdata1
        
        # Larger multiple
        b = a + magofdata1
        
        return a


except Exception as exp:
    
    print(exp)
    input()
