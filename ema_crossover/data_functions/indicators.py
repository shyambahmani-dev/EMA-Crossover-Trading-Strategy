import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.widgets as mplw
from matplotlib.backends.backend_pdf import PdfPages, FigureCanvasPdf
import yfinance as yf
import datetime
import csv
import os
import code
import time
from dateutil.relativedelta import relativedelta
from pandas import ExcelWriter
import traceback

import sys


class plot_indicator(object):
    
    def __init__(self, chart, symbol, indicator_type, period = '1d'):

        self.chart = chart
        self.symbol = symbol
        self.indicator_type = indicator_type
        self.period = period
    
        ticker1 = yf.Ticker(self.symbol)

        self.data = ticker1.history(period= period)

        self.lines = {}

        if(self.indicator_type == 'DMA'):
            self.on_chart.plotDMA(self)

        elif(self.indicator_type == 'EMA'):
            self.on_chart.plotEMA()

        elif(self.indicator_type == 'Bollinger Bands'):
            self.on_chart.plotBB()

    class on_chart(object):

        def plotDMA(self):

            dmaIntv = [3, 5, 10, 25, 50, 100, 200, 500]

            data1DMA = pd.DataFrame()

            for it in dmaIntv:

                data1DMA["DMA%d" %(it)] = self.data["Close"].rolling(it).mean()

            data1DMA.rename(columns={'Date':'time'})

            #"""
            for it in dmaIntv:

                print(data1DMA["DMA%d" %(it)])
                self.lines["DMA%d" %(it)] = self.chart.create_line(name='DMA%d' %(it))
                self.lines["DMA%d" %(it)].set(data1DMA)
            #"""


        def plotEMA():
            pass
        
        def plotBB():
            pass


    