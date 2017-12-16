#! /usr/bin/python3
# -*- coding: utf-8 -*-
from pandas_datareader import data as pdr
import quandl
import matplotlib.pyplot as plt
import fix_yahoo_finance # must pip install first 
from blaze.expr.expressions import label
import pandas as pd
from yahoo_finance import Share
from symbol import comparison

class Stock_Analysis:
    #
    def __init__(self, Stock_Ticker,Start_Date):    
        self.ticker = Stock_Ticker
        self.start_date = Start_Date
        self.share = Share(self.ticker)
        self.name = self.share.get_name()
        try:
            self.stock_data = pdr.get_data_yahoo(self.ticker,self.start_date)
        except:
            print("Error with Yahoo - please enter Quandl Tickers")
            try:
                self.quandl_ticker = input()
                self.stock_data = quandl.get(self.quandl_ticker)
            except:
                print("Failled")
    #
    def Print_Data(self):
        print(self.stock_data)
        return self.stock_data
    #
    def Print_Linechart(self):
        plt.plot(self.stock_data["Adj Close"],label = self.name)
        plt.title("Adj. Aktienkurs des Unternehmens %s"%self.name)
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.show()
    #
    def Histogramm_Returns(self):
        stock_returns = ((self.stock_data["Close"]/self.stock_data["Open"])-1)*100
        plt.hist(stock_returns)
        plt.title("Verteilung der Tagesrenditen von %s"%self.name)
        plt.show()
    #
    def Scatter_Plot(self,comparison_ticker):
        ref_stock = pdr.get_data_yahoo(comparison_ticker,self.start_date)
        ref_share = Share(comparison_ticker)
        ref_stock_name = ref_share.get_name()
        stock_returns = pd.DataFrame(((self.stock_data["Close"]/self.stock_data["Open"])-1)*100)
        ref_returns = pd.DataFrame(((ref_stock["Close"]/ref_stock["Open"])-1)*100)
        returns_df = stock_returns.join(ref_returns,lsuffix=("Returns %s"%self.name),rsuffix=("Returns %s"%ref_stock_name))
        print(returns_df)
        ax1 = plt.subplot2grid((1,1),(0,0))
        ax1.grid(True, color = "b", linestyle = "-")
        plt.xlabel(ref_stock_name)
        plt.ylabel(self.name)
        plt.scatter(returns_df[returns_df.columns[1]],returns_df[returns_df.columns[0]])
        plt.title("Scatterplot von %s und %s"%(ref_stock_name,self.name))
        plt.plot()
        

apple = Stock_Analysis("AAPL","2015-01-01")
apple.Print_Data()


#Pasiva as Stack Chart
years = [2012,2013,2014,2015,2016]
apple_short_credit = [38542,43658,63448,80610,79006]
apple_long_credit = [19312,39793,56844,90514,114431]
apple_equity = [118210,123549,111547,119355,128429]
#lines have to be defined fors to allow for labeling ! - Stackplot itself does not provide this functionality
plt.plot([],[],color = "m",label="short_credit", linewidth=5)
plt.plot([],[],color = "r",label="long_credit", linewidth=5)
plt.plot([],[],color = "c",label="equity", linewidth=5)
#Define the Stackplot, years as x and separate y values comma separated after the years
plt.stackplot(years,apple_short_credit,apple_long_credit,apple_equity, colors = ["m","r","c"])
plt.legend()
plt.xlabel("Years")
plt.ylabel("Capital of %s"%"Apple")
plt.show()
