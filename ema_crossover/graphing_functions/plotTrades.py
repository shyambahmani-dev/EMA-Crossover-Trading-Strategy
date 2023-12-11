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
import inline
import traceback

import os
import sys

sys.path.append("..")
import code

import Project1.data_functions.get_data as getData
import Project1.data_functions.get_indicators as getIndicators
import Project1.graphing_functions.drawer as drawer
import Project1.graphing_functions.savePlot as savePlot



#"""
def plot(data1, tickerName, periodTested, portfolio, strat_name, daysBought, daysSold, marketPortfolio):

    fig1 = plt.figure(figsize = (12,12))

    fig1.canvas.setWindowTitle("%s-%s-%s" %(tickerName, strat_name, periodTested))

    gs1 = fig1.add_gridspec(8,4)
    ax1 = fig1.add_subplot(gs1[0:4,0:4])
    
    ax1.plot(portfolio.index, portfolio['Value'], label = "Portfolio", color = 'forestgreen')
    ax1.plot(portfolio.index, marketPortfolio['Value'], label = "Market", color = 'sienna')

    ax1.legend()

    for it in daysBought:
        ax1.axvline(it, color = 'green', alpha = 0.1)

    for it in daysSold:
        ax1.axvline(it, color = 'red', alpha = 0.1)

    drawer.marginandstuff(portfolio, ax1, fig1)

    ax2 = fig1.add_subplot(gs1[4:8,0:4], sharex = ax1)
    drawer.ohlcplot(data1, ax2, fig1)

    cursor1 = mplw.MultiCursor(fig1.canvas, [ax1,ax2] , horizOn= True , color = "lightskyblue" , linewidth = 1)

    fig1.tight_layout()

    plt.show()

    savePlot.save(portfolio, strat_name, fig1, tickerName, periodTested)

#"""


"""

class plot(object)::

    def plot(data1, tickerName, periodTested, portfolio, strat_name, daysBought, daysSold, marketPortfolio):

        if __name__ == '__main__':

        chart = Chart(toolbox=True, debug=True, inner_height=0.7)

        symbol = '^NSEI'
        
        chart.legend(True)
        chart.events.search += on_search
        chart.topbar.textbox(symbol)
        chart.topbar[symbol].set(symbol)
        chart.topbar.menu(
            'timeframe',
            ('1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo', '3mo'),
            default='1d',
            func=on_timeframe_selection
        )

        chart.topbar.menu(
            'period',
            ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"),
            default = '1y',
            func=on_period_selection
        )

        chart.topbar.menu(
            'indicators',
            ('DMA', 'EMA', 'RSI', 'Bollinger Bands', 'Fibbonacci Retracement'),
            func= on_indicator_selection
        )



        chart2 = chart.create_subchart(toolbox=True, position='right', width=1, height=0.3)

        chart2.legend(True)
        chart2.events.search += on_search
        chart2.topbar.textbox(symbol)
        chart2.topbar[symbol].set(symbol)
        chart2.topbar.menu(
            'timeframe',
            ('1m', '5m', '15m', '1hr', '1d', '1wk', '1mo'),
            default='1d',
            func=on_timeframe_selection
        )


        chart.show(block=True)

#"""