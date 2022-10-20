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
        self.high_nine = bt.indicators.Highest(self.data.high, period=9)
        self.low_nine = bt.indicators.Lowest(self.data.low, period=9)
        self.rsv = 100 * bt.DivByZero(
            self.data_close - self.low_nine, self.high_nine - self.low_nine, zero=None
        )
        self.K = bt.indicators.EMA(self.rsv, period=3)
        self.D = bt.indicators.EMA(self.K, period=3)
        self.J = 3 * self.K - 2 * self.D
    def next(self):

        if not self.position:       
            cond1 = self.K[-1] - self.D[-1]
            cond2 = self.K[0] - self.D[0]
            if cond1 < 0 and cond2 > 0 and self.K[0] < 30:
                self.buy()
        else:
            cond1 = self.K[-1] - self.D[-1]
            cond2 = self.K[0] - self.D[0]
            if cond1 > 0 and cond2 < 0 and self.K[0] > 70:
                self.close()


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
start_date = '2021-10-01'
symbol = 'TSLA'
# df = yf.download(symbol, start = start_date)
df = get_bar_min_tdd(symbol, 3)

print(len(df),df.tail(5))

if df is None:
	print('none')
	sys.exit()
today=datetime.today().strftime('%Y-%m-%d')
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


