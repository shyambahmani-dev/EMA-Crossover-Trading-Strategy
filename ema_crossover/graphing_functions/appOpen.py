import tkinter as tk
import code

class tickerApp(object):

    def __init__(self, strat_name):
        
        self.root= tk.Tk()
        self.strat_name = strat_name
        self.tickerName = ""
        self.periodTested = ""
        self.intervalTested = ""


        label1 = tk.Label(self.root, text='Backtesting strategy %s' %(self.strat_name))
        label1.config(font=('helvetica', 14))
        label1.pack()

        label2 = tk.Label(self.root, text='Enter tickername from Yahoo Finance:')
        label2.config(font=('helvetica', 10))
        label2.pack()

        entry1 = tk.Entry(self.root)
        entry1.pack()


        label3 = tk.Label(self.root, text='Enter Period to backtest for (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)')
        label3.config(font=('helvetica', 10))
        label3.pack()

        value_inside1 = tk.StringVar(self.root) 
        
        # Set the default value of the variable 
        value_inside1.set("1y") 
        periodList = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        periodOptionMenu = tk.OptionMenu(self.root, *periodList) 
        periodOptionMenu.pack()


        label4 = tk.Label(self.root, text='Enter interval to backtest for (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)')
        label4.config(font=('helvetica', 10))
        label4.pack()

        value_inside2 = tk.StringVar(self.root) 
        
        # Set the default value of the variable 
        value_inside2.set("1d") 
        intervalList = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
        intervalOptionMenu = tk.OptionMenu(self.root, *intervalList) 
        intervalOptionMenu.pack()



        def setTicker():
            self.tickerName = entry1.get()
            self.periodTested = periodOptionMenu.get()
            self.intervalTested = intervalOptionMenu.get()
        
        button1 = tk.Button(text='Backtest now', command=setTicker, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
        button1.pack()

        self.root.mainloop()

app = tickerApp("test_strat")


code.interact(local=locals())