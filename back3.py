from datetime import datetime
import backtrader as bt# import backtrader.feeds as btfeeds
import json,os,sys
import requests
import pandas as pd
import yfinance as yf
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# Create a subclass of Strategy to define the indicators and logic
import datetime
import backtrader as bt
import backtrader.feeds as btfeed

class TestStrategy(bt.Strategy):
    params = dict(
        pfast=8,
        pslow=20
    )

    def __init__(self):
        self.bbands = bt.ind.BollingerBands()
        sma0 = bt.ind.SMA(period=1)
        sma1 = bt.ind.SMA(period=3)
        sma2 = bt.ind.SMA(period=8)
        ema0 = bt.ind.EMA(period=1)
        ema1 = bt.ind.EMA(period=3)
        ema2 = bt.ind.EMA(period=8)
        self.crossover = bt.ind.CrossOver(sma0, self.bbands.lines.top)
        
        # self.crossover_down = bt.ind.CrossOver(sma1, sma2)
        self.crossover_down = bt.ind.CrossOver(sma0, self.bbands.lines.bot)
		
    def next(self):
        # if not self.position:
        if True:
            if self.crossover_down < 0:
                self.buy()
            if self.crossover > 0:
                self.close()

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
start_date = '2020-01-01'

symbol = 'TSLA'
df = yf.download(symbol, start = start_date)

feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)
cerebro.addstrategy(TestStrategy)  # Add the trading strategy
cerebro.broker.setcommission(commission = 0.005)
cerebro.addsizer(bt.sizers.PercentSizer, percents=50)
cerebro.addanalyzer(bt.analyzers.AnnualReturn,_name = 'areturn')
teststrat = cerebro.run()  # run it all
# cerebro.plot()

analyzers = teststrat[0].analyzers.areturn.get_analysis()

v = list(analyzers.values())
k = list(analyzers.keys())
s = [symbol] * len(v)

df = pd.DataFrame({'symbol':s,'year':k,'annualreturn':v})
df['annualreturn']=df['annualreturn'].map(lambda x:("%.3f")%x)
print(start_date, '\t', symbol)
print(df)
