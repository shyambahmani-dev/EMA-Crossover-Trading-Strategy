import numpy as np
import pandas as pd
import yfinance as yf
import datetime
import csv
import os
import code
from dateutil.relativedelta import relativedelta
import traceback

import sys
sys.path.append("..")


import Project1.data_functions.get_data as getData
import Project1.data_functions.get_indicators as getIndicators

import Project1.performance_analysis.run_analysis as pa



from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton

from lightweight_charts.widgets import QtChart

class plot(object):

    #"""
    
    def __init__(self, data1, tickerName, periodTested, portfolio, strat_name, daysBought, daysSold, marketPortfolio):

        self.data1 = data1
        self.tickerName = tickerName
        self.periodTested = periodTested
        self.portfolio = portfolio
        self.strat_name = strat_name
        self.daysBought = daysBought
        self.daysSold = daysSold
        self.marketPortfolio = marketPortfolio
        
        app = QApplication([])
        window = QMainWindow()
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        window.resize(800, 500)
        layout.setContentsMargins(0, 0, 0, 0)



        chart = QtChart(widget, toolbox=False, inner_height=0.6)

        portfolioLine = chart.create_line("Value", color= 'darkgreen')
        portfolioLine.set(self.portfolio)


        marketPortfolioLine = chart.create_line("Value", color= 'sienna')
        marketPortfolioLine.set(self.marketPortfolio)

        chart2 = chart.create_subchart(toolbox=True, position='bottom', width=1, height=0.4, sync= True)
        chart2.set(self.data1)




        layout.addWidget(chart.get_webview())
        window.setCentralWidget(widget)

        window.show()

        app.exec_()

        self.portfolio.to_csv("./results/%s-%s.csv" %(tickerName, periodTested))


