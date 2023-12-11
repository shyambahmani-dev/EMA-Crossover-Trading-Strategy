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

import sys
sys.path.append("..")

import Project1.data_functions.get_data as getData
import Project1.data_functions.get_indicators as getIndicators
import Project1.graphing_functions.drawer as drawer
import Project1.graphing_functions.plotPortfolio as plotPortfolio


try:

    class analytics(object):

        def __init__(self, data1, tickerName, periodTested, intervalTested, portfolio, marketPortfolio, daysBought, daysSold):

            self.data1 = data1
            self.data1.index = pd.to_datetime(self.data1.index)
            self.tickerName = tickerName
            self.periodTested = periodTested
            self.intervalTested = intervalTested
            self.portfolio = portfolio
            self.marketPortfolio = marketPortfolio
            self.daysBought = daysBought
            self.daysSold = daysSold
            self.initialCash = self.portfolio['Value'].iloc[0]
            self.testStocks = {}

            relDel = relativedelta(self.data1.index[-1],self.data1.index[0])
            self.strat_years = float(relDel.years) + ( (float)(relDel.months)/12.0 ) +  (float)(relDel.days)/(365.25)


            listTestStocks = ["HDFCBANK.NS", "EXIDE.NS", "SBIN.NS", "TATASTEEL.NS","TATAMOTORS.NS"]

        def portfolio_returns(self):

            portfolioReturns = (((float)(self.portfolio['Value'].iloc[-1] - self.initialCash))/(float)(self.initialCash))*100
            benchmarkReturns = (((float)(self.data1["Close"].iloc[-1] - self.data1["Close"].iloc[0]))/((float)(self.data1["Close"].iloc[0])))*100
            
            return {'portfolioReturns':portfolioReturns, 'benchmarkReturns':benchmarkReturns, 'excessReturns':portfolioReturns - benchmarkReturns}
        
        def CAGR(self):
            CAGRPort = (pow( (float)(((float)(self.portfolio['Value'].iloc[-1]))/((float)(self.initialCash))), 1.0/self.strat_years) - 1)*100
            CAGRStock = (pow((((float)(self.data1["Close"].iloc[-1]))/((float)(self.data1["Close"].iloc[0]))), 1.0/self.strat_years) - 1)*100

            return {'CAGRPort':CAGRPort, 'CAGRMarket':CAGRStock, 'CAGRExcess': CAGRPort - CAGRStock}


        def sharpe_ratio(self):

            data1size = (int)(self.data1["Close"].size)

            alphas = np.array([])
            portfolioRet = np.array([])
            benchmarkRet = np.array([])

            currDate = min(100, data1size/10)
            timeInt = min(100, data1size/10)

            while( currDate < self.data1["Close"].size ):

                portfolioRet = np.append( portfolioRet, ((float)( self.portfolio["Value"].iloc[currDate] - self.portfolio["Value"].iloc[currDate - timeInt] )/(float)(self.portfolio["Value"].iloc[currDate - timeInt])) )
                benchmarkRet = np.append( benchmarkRet, ( (float)(self.marketPortfolio["Value"].iloc[currDate] - self.marketPortfolio["Value"].iloc[currDate - timeInt] )/(float)(self.marketPortfolio["Value"].iloc[currDate - timeInt]) ) )

                currDate += timeInt
            
            alphasPortolio = portfolioRet
            alphasBenchmark = benchmarkRet

            meanRetPortfolio = np.mean(alphasPortolio)
            stdRetPortfolio = np.std(alphasPortolio)
            try:
                sharpeRatioPortfolio = (float)(meanRetPortfolio)/(float)(stdRetPortfolio)
            except:
                sharpeRatioPortfolio = 100

            meanRetBenchmark = np.mean(alphasBenchmark)
            stdRetBenchmark = np.std(alphasBenchmark)
            try:
                sharpeRatioBenchmark = (float)(meanRetBenchmark)/(float)(stdRetBenchmark)
            except:
                sharpeRatioBenchmark = 100

            return {'sharpeRatioPortfolio':sharpeRatioPortfolio, 'sharpeRatioBenchmark':sharpeRatioBenchmark}
        
        def market_dev(self):

            averageUp = 0.0
            maxUp = 0
            maxDown = 0

            for ind in self.portfolio.index:
                averageUp += (float)((float)(self.portfolio["Value"].loc[ind] - self.marketPortfolio["Value"].loc[ind])/(float)(self.marketPortfolio["Value"].loc[ind]))
                maxUp = max( maxUp, (float)(self.portfolio["Value"].loc[ind] - self.marketPortfolio["Value"].loc[ind])/(float)(self.marketPortfolio["Value"].loc[ind]) )
                maxDown = min(maxDown, (float)(self.portfolio["Value"].loc[ind] - self.marketPortfolio["Value"].loc[ind])/(float)(self.marketPortfolio["Value"].loc[ind]) )

            averageUp = (float)(averageUp)/(float)(self.portfolio.index.size)
            
            maxUp *= 100
            maxDown *= 100
            averageUp *= 100
            
            return {'maxUp':maxUp, 'maxDown':maxDown, 'averageUp':averageUp}

        def AUC_comp(self):

            portfolioAUC = 0
            marketPortfolioAUC = 0

            for ind in self.portfolio.index:

                portfolioAUC += self.portfolio["Value"].loc[ind]
                marketPortfolioAUC += self.marketPortfolio["Value"].loc[ind]

            return {'portfolioAUC':portfolioAUC, 'marketPortfolioAUC':marketPortfolioAUC, 'AUCRatio':(float)((( float )( portfolioAUC ))/( (float)( marketPortfolioAUC ) ))  }

                                             




except Exception as exp:
    
    print(exp)
    input()

