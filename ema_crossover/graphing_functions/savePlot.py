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

print(os.getcwd())

import Project1.data_functions.get_data as getData
import Project1.data_functions.get_indicators as getIndicators
import Project1.graphing_functions.drawer as drawer
import Project1.graphing_functions.plotPortfolio as plotPortfolio


try:

    def save(portfolio, strat_name, fig, tickerName, periodTested = '0'):

        if(periodTested == '0'):
            periodTested = datetime.date.today()

        portfolio.to_csv("results\%s-%s-%s.csv" %(tickerName, strat_name, periodTested) )
        pdf = PdfPages("results\%s-%s-%s.pdf" %(tickerName, strat_name, periodTested))
        pdf.savefig(fig)
        pdf.close()

except Exception as exp:
    print(exp)
    input()
