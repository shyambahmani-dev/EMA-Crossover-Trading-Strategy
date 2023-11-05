import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
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

print(os.getcwd())

import Project1.data_functions.get_data as getData
import Project1.data_functions.get_indicators as getIndicators



data1 = getData.tickerData("^NSEI", period = "5Y")
data1["Typical"] = (data1["Close"] + data1["High"] + data1["Low"])/3

dmaIntv = [10, 25, 50, 100, 200, 500]
emaIntv = [10, 25, 50, 100, 200, 500]

data1DMA = getIndicators.getDMA(data1)
data1EMA = getIndicators.getEMA(data1, emaIntv)
data1BB = getIndicators.getBB(data1)

longProfit = 0
bought = False
maxLongProfit = -1e10
longPortfolio = np.array([])
compltLongProftfolio = 0

firstBuy = 0
firstBought = False

#"""

for ind in data1.index:

    if(data1["Typical"].loc[ind] > data1BB["1STDUP"].loc[ind] and (not bought) ):

        lastPrice = data1["Typical"].loc[ind]
        bought = True

        if(firstBought == False):
            firstBuy = data1["Typical"].loc[ind]
            firstBought = True

    
    elif ( data1["Typical"].loc[ind] < data1BB["1STDUP"].loc[ind] and (bought)) :

        longProfit += data1["Typical"].loc[ind] - lastPrice
        bought = False
        compltLongProftfolio = longProfit

    longPortfolio = np.append(longPortfolio, longProfit)
    maxLongProfit = max(maxLongProfit, longProfit)


print("Final complete longPortfolio = %0.02f" %(compltLongProftfolio) )
plt.plot(longPortfolio)
#plt.show()

#"""

#"""

shortProfit = 0
maxShortProfit = -1e10
shortPortfolio = np.array([])
sold = False
compltShortProftfolio = 0
lastShortPrice = 0

#data1DMA["DMA10"]
#data1["Typical"]


#"""
for ind in data1.index:

    if(data1["Typical"].loc[ind] < data1BB["1STDDN"].loc[ind] and (not sold) ):

        lastShortPrice = data1["Typical"].loc[ind]
        sold = True

    
    elif ( data1["Typical"].loc[ind] > data1BB["1STDDN"].loc[ind] and (sold)) :

        shortProfit += lastShortPrice - data1["Typical"].loc[ind] 
        sold = False
        compltShortProftfolio = shortProfit

    
    shortPortfolio = np.append(shortPortfolio, shortProfit)
    maxShortProfit = max(maxShortProfit, shortProfit)

print("Final complete shortPortfolio = %0.02f" %(compltShortProftfolio) )
plt.plot(shortPortfolio)
plt.show()

#"""


#plt.plot(portfolio)
plt.plot(longPortfolio)
plt.plot(shortPortfolio)

plt.show()



code.interact(local=locals())
