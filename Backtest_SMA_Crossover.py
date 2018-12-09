#! /usr/bin/python3
# -*- coding: utf-8 -*-

from pandas_datareader import data as pdr
import fix_yahoo_finance # must pip install first 
import numpy as np
import pandas as pd
import datetime
from matplotlib import pyplot as plt
#from skimage.feature.tests.test_util import plt


start_date = ("2010-01-01")
stock_ticker = "AAPL"
schnell,langsam = 10,50


class QuantitativeStrategy():
    def __init__(self,stock_ticker,start_date,schnell,langsam):
        self.aktie = pdr.get_data_yahoo(stock_ticker,start_date).copy()
        self.schneller_ma = schnell
        self.langsamer_ma = langsam
    def moving_average_cross(self):
        '''Method to create a DataFrame and initialise the signal as no Signal status
        '''
        #schnellen und langsamen MA erstellen
        schnell = self.aktie["Adj Close"].rolling(window = self.schneller_ma).mean()
        langsam = self.aktie["Adj Close"].rolling(window = self.langsamer_ma).mean()
        signals = pd.concat([self.aktie["Adj Close"],schnell,langsam],axis = 1, join_axes = [schnell.index])
        signals.columns = ["Adj Close","schnell","langsam"]
        signals["signal"] = (signals["schnell"] > signals["langsam"])*1
        #Um Forwadlooking Bias zu vermeiden ist es notwendig, die Signale um einen Tag zu verschieben,
        #Wenn heute das Signal entsteht, darf erst morgen eine Position darauf hin eingegangen werden.
        #Wenn dies nicht beachtet wird wird jede Strategie automatisch zum Powerhouse, da die bekannte
        #Zukunft in die Entscheidungen mit einfließt
        #Dazu shiften wir die Signalspalte um eine Periode in die Zukunft - sodass das Signal am Folgetag
        #für die Handelsentscheidung herangezogen wird
        signals["signal"] = signals["signal"].shift(1)
        return signals


class PortfolioBacktest():
    def __init__(self,signal_matrix):
        self.signal_matrix = signal_matrix
    def equity_development(self,initial_account_size = 10000,leverage = 1):
        df = self.signal_matrix
        df.dropna(inplace = True)
        df["return"] = df["Adj Close"].pct_change()
        df["strategy_returns"] = df["signal"]*df["return"]*leverage+1
        df["capital_growth"] = df["strategy_returns"].cumprod()
        df["stock_performance"] = (df["return"]+1).cumprod()
        df["stock_performance"] = df["stock_performance"]*initial_account_size
        df["equity"] = df["capital_growth"]*initial_account_size
        #fig, axes = plt.subplots(nrows=2, ncols=2)
        fig = plt.figure()
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(212)
        df[["equity","stock_performance"]].plot(ax = ax3)
        (df["return"]).plot(ax = ax1,kind = "hist",title = "Histogram of Stock Returns")
        filter_null_returns = (df["strategy_returns"] != 1)
        (df["strategy_returns"][filter_null_returns]-1).plot(ax = ax2,kind = "hist", title = "Histogram of Strategy Returns")
        return(df)



Strategy = QuantitativeStrategy("BAS.DE","2010-01-01",20,80)
Strategy = Strategy.moving_average_cross()
Portfolio = PortfolioBacktest(Strategy)
Results = Portfolio.equity_development()

Strategy = QuantitativeStrategy("BAS.DE","2010-01-01",20,80)
Strategy = Strategy.moving_average_cross()
Portfolio = PortfolioBacktest(Strategy)
Results = Portfolio.equity_development(leverage = 3)

Strategy = QuantitativeStrategy("AAPL","2010-01-01",30,80)
Strategy = Strategy.moving_average_cross()
Portfolio = PortfolioBacktest(Strategy)
Results = Portfolio.equity_development(leverage = 1)
