from datetime import datetime
import backtrader as bt# import backtrader.feeds as btfeeds
import json,os,sys
import requests
import yfinance as yf
import backtrader.feeds as btfeed
import backtrader.indicators as btind
from idc import *
# os.environ["http_proxy"] = "http://127.0.0.1:10809"
# os.environ["https_proxy"] = "http://127.0.0.1:10809"#7890

# Create a subclass of Strategy to define the indicators and logic

class TestStrategy(bt.Strategy):
    params = dict(
        pfast=8,
        pslow=20
    )

    def __init__(self):
        ema12 = btind.EMA(period=12)
        ema169 = btind.EMA(period=169)
        ema144 = btind.EMA(period=144)        # 
        self.ema144 = btind.EMA(period=144)
        ema576 = btind.EMA(period=576)
        self.ema676 = btind.EMA(period=676)
        self.signal1 = btind.CrossOver(self.data.close, ema12)
        self.signal2 = btind.CrossOver(self.data.close, ema144)
    def next(self):
        # if not self.position:
            # if self.signal1 < 0 :
                # self.sell()
        # if self.position:		
            # if self.signal1 > 0 :
                # self.close()
        if not self.position:
            if self.signal1 > 0 and self.data.close < self.ema144:
                self.buy()
        if self.position:		
            if self.signal1 < 0 and self.data.close > self.ema676:
                self.close()

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
start_date = '2021-10-01'
symbol = 'TSLA'
# df = yf.download(symbol, start = start_date)
df = get_bar_min_tdd(symbol, 10)

if df is None:
	print('none')
	sys.exit()
today=datetime.today().strftime('%Y-%m-%d')
print(len(df),df.tail(5))
print(today, '\t', symbol)

feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)
cerebro.addstrategy(TestStrategy)  # Add the trading strategy
cerebro.broker.setcommission(commission = 0.005)
cerebro.addsizer(bt.sizers.PercentSizer, percents=50)
cerebro.addanalyzer(bt.analyzers.AnnualReturn,_name = 'areturn')
teststrat = cerebro.run()  # run it all
print(teststrat[0].analyzers.areturn.get_analysis())
print(df.head(1),'',df.tail(1))
cerebro.plot()  # and plot it with a single command


