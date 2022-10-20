from datetime import datetime
import backtrader as bt# import backtrader.feeds as btfeeds
import json,os,sys
import requests
import yfinance as yf
import backtrader.feeds as btfeed
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
        self.bbands = bt.ind.BollingerBands()
        sma0 = bt.ind.SMA(period=1)

        # self.crossover = bt.ind.CrossOver(sma0, self.bbands.lines.top)
        # self.crossover_down = bt.ind.CrossOver(sma0, self.bbands.lines.bot)

    def next(self):
        if not self.position:
        # if True:
            if self.data.high < self.bbands.lines.bot :
                self.buy()
        if self.position:		
            if self.data.low > self.bbands.lines.top :
                self.close()

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
start_date = '2021-10-01'
symbol = 'TSLA'
# df = yf.download(symbol, start = start_date)
if len(sys.argv)>2:
	df = get_bar_min_tdd(sys.argv[1], int(sys.argv[2]))
else:
	df = get_bar_min_tdd(symbol, 3)

today=datetime.today().strftime('%Y-%m-%d')
print(today, '\t', symbol)

if df is None:
	print('df is None')
	sys.exit()
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