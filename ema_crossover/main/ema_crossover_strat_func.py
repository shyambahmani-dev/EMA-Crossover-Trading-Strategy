import numpy as np
import pandas as pd
import yfinance as yf
import datetime
import csv
import os
import code
from dateutil.relativedelta import relativedelta
import traceback
import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("..")



import Project1.data_functions.get_data as getData
import Project1.data_functions.get_indicators as getIndicators
import Project1.performance_analysis.run_analysis as pa
import Project1.graphing_functions.plotPortfolio as plotPortfolio
import Project1.graphing_functions.plotTrades as plotTrades




tickerName = "^NSEI"
periodTested = "10y"
strat_name = "ema_crossover"
intervalTested = '1h'



class parameterRes(object):

    def __init__(self, CAGR, CAGRExcess, AUCRatio, maxUp, maxDown, averageUp):
        
        self.CAGR = CAGR
        self.CAGRExcess = CAGRExcess
        self.AUCRatio = AUCRatio
        self.maxUp = maxUp
        self.maxDown = maxDown
        self.averageUp = averageUp




class run_strat(object):

    def __init__(self, strat_name, tickerName, periodTested, intervalTested):

        self.strat_name = strat_name
        self.tickerName = tickerName
        self.periodTested = periodTested
        self.intervalTested = intervalTested

        print("Stock analysed: %s for a period of %s \n \n" %(tickerName, periodTested))

        if( os.path.isfile( r".\database\%s-%s-%s-%s.csv" %(self.tickerName, self.periodTested, (str)(datetime.datetime.today().date()), self.intervalTested ) ) ):
            self.data1 = pd.read_csv( r".\database\%s-%s-%s-%s.csv" %(self.tickerName, self.periodTested, (str)(datetime.datetime.today().date()), self.intervalTested ), index_col = [0] )
            self.data1.index = pd.to_datetime(self.data1.index)
        else:
            self.data1 = getData.tickerData(symbol= self.tickerName, period= self.periodTested, interval= self.intervalTested)
            self.data1.to_csv( r".\database\%s-%s-%s-%s.csv" %(self.tickerName, self.periodTested, (str)(datetime.datetime.today().date()), self.intervalTested  ) )



        self.dmaIntv = [3, 5, 10, 15, 25, 50, 75, 100, 150, 200, 500]
        self.emaIntv = [3, 5, 10, 15, 25, 50, 75, 100, 150, 200, 500]

        self.data1DMA = getIndicators.getDMA(self.data1, self.dmaIntv)
        self.data1EMA = getIndicators.getEMA(self.data1, self.emaIntv)
        self.data1BB = getIndicators.getBB(self.data1)
        self.data1RSI = getIndicators.getRSI(self.data1)
        self.data1DMAslope = self.data1DMA.diff()
        self.initialCash = 1e6
        self.feesFactor = 0.05



        #"""

    def run(self, emaFastBuy, emaSlowBuy, emaFastSell, emaSlowSell):

        portfolio = pd.DataFrame(columns=['Value','AssetNum','Cash'], index= self.data1["Close"].index)
        currCash = self.initialCash
        currInvested = 0
        assetNum = 0
        
        daysBought = np.array([])
        daysSold = np.array([])
        marketPortfolio = pd.DataFrame(columns=['Value', 'AssetNum'], index= self.data1["Close"].index)
        marketPortfolio.set_index(self.data1.index)
        marketNum = self.initialCash/self.data1["Close"].iloc[0]


        for ind in self.data1.index:


            if(not pd.isna(self.data1EMA["%s" %( max(emaSlowBuy, emaSlowSell) )].loc[ind])):

                buyPrice = self.data1["Close"].loc[ind]
                sellPrice = buyPrice
                buyRatioCash = 1
                sellRatioPort = 1

                if( self.data1EMA["%s" %(emaFastBuy)].loc[ind] > self.data1EMA["%s" %(emaSlowBuy)].loc[ind]): # and data1EMA["10"].loc[ind] > data1EMA["15"].loc[ind] ):
                    
                    numCanBuy = (buyRatioCash*currCash)/( buyPrice )
                    currCash -= (numCanBuy*buyPrice) - min(30, (numCanBuy*(buyPrice)*self.feesFactor))
                    assetNum += numCanBuy
                    
                    daysBought = np.append(daysBought, ind)
                

                
                elif( self.data1EMA["%s" %(emaFastSell)].loc[ind] < self.data1EMA["%s" %(emaSlowSell)].loc[ind]): # and data1EMA["10"].loc[ind] < data1EMA["15"].loc[ind] ):

                    numCanSell = (assetNum)*(sellRatioPort)
                    currCash += (numCanSell*(sellPrice)) - min(30, (numCanSell*(sellPrice))*self.feesFactor)
                    assetNum -= numCanSell
                    
                    daysSold = np.append(daysSold, ind)


            portfolio.loc[ind] = [currCash + assetNum*(self.data1["Close"].loc[ind]), assetNum, currCash]
            marketPortfolio.loc[ind] = [marketNum*(self.data1["Close"].loc[ind]), marketNum]


        #"""




        #plotPortfolio.plot(data1, self.tickerName, self.periodTested, portfolio, self.strat_name, daysBought, daysSold, marketPortfolio)
        #plotTrades.plot(data1, self.tickerName, self.periodTested, portfolio, self.strat_name, daysBought, daysSold, marketPortfolio)


        analysis = pa.analytics(self.data1, self.tickerName, self.periodTested, self.intervalTested, portfolio, marketPortfolio, daysBought, daysSold)
        CAGRportfolio = analysis.CAGR()
        AUC = analysis.AUC_comp()
        marketDev = analysis.market_dev()

        toRet = parameterRes(CAGRportfolio['CAGRPort'], CAGRportfolio['CAGRExcess'], AUC['AUCRatio'], marketDev['maxUp'], marketDev['maxDown'], marketDev['averageUp'])

        return toRet

    




emaList = [3, 5, 10, 15, 25, 50, 75, 100]
#emaList = [3, 5, 10] #, 15, 25, 50, 75, 100]

stratRes = {}
CAGRExcessRes = []
AUCRatioRes = []
maxUpRes = []
maxDownRes = []
averageUpRes = []




if os.path.isdir(r".\results\%s" %(tickerName) ) :
        
    pass

else:

    os.mkdir(r".\results\%s" %(tickerName) )




#"""

idx = 0

strat_object = run_strat(strat_name, tickerName, periodTested, intervalTested)

for bF in emaList:

    for bS in emaList:

        for sF in emaList:

            for sS in emaList:

                if(bF < bS and sF < sS):

                    print("Running strat for %s-%s-%s-%s" %(bF, bS, sF, sS))
                    
                    stratRes["%s-%s-%s-%s" %(bF, bS, sF, sS)] = strat_object.run(bF, bS, sF, sS)
                    
                    CAGRExcessRes.append( [stratRes["%s-%s-%s-%s" %(bF, bS, sF, sS)].CAGRExcess , ("%s-%s-%s-%s" %(bF, bS, sF, sS))] )
                    AUCRatioRes.append( [stratRes["%s-%s-%s-%s" %(bF, bS, sF, sS)].AUCRatio , "%s-%s-%s-%s" %(bF, bS, sF, sS)] )
                    maxUpRes.append( [stratRes["%s-%s-%s-%s" %(bF, bS, sF, sS)].maxUp , "%s-%s-%s-%s" %(bF, bS, sF, sS)] )
                    maxDownRes.append( [stratRes["%s-%s-%s-%s" %(bF, bS, sF, sS)].maxDown , "%s-%s-%s-%s" %(bF, bS, sF, sS)] )
                    averageUpRes.append( [stratRes["%s-%s-%s-%s" %(bF, bS, sF, sS)].averageUp , "%s-%s-%s-%s" %(bF, bS, sF, sS)] )

CAGRExcessRes.sort(reverse=True)
AUCRatioRes.sort(reverse=True)
maxUpRes.sort(reverse=True)
maxDownRes.sort(reverse=True)
averageUpRes.sort(reverse=True)


CAGRExcessResDF = pd.DataFrame(CAGRExcessRes)
CAGRExcessResDF.to_csv( r".\results\%s\CAGRExcessRes_%s-%s-%s.csv" %(tickerName, tickerName, periodTested, strat_name ) )

AUCRatioResDF = pd.DataFrame(AUCRatioRes)
AUCRatioResDF.to_csv( r".\results\%s\AUCRatioRes_%s-%s-%s.csv" %(tickerName, tickerName, periodTested, strat_name ) )

maxUpResDF = pd.DataFrame(maxUpRes)
maxUpResDF.to_csv( r".\results\%s\maxUpRes_%s-%s-%s.csv" %(tickerName, tickerName, periodTested, strat_name ) )

maxDownResDF = pd.DataFrame(maxDownRes)
maxUpResDF.to_csv( r".\results\%s\maxDownRes_%s-%s-%s.csv" %(tickerName, tickerName, periodTested, strat_name ) )

averageUpResDF = pd.DataFrame(averageUpRes)
maxUpResDF.to_csv( r".\results\%s\averageUpRes_%s-%s-%s.csv" %(tickerName, tickerName, periodTested, strat_name ) )

#"""




code.interact(local=locals())