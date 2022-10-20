from datetime import datetime
import backtrader as bt# import backtrader.feeds as btfeeds
import json,os,sys
import requests
import yfinance as yf
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# Create a subclass of Strategy to define the indicators and logic
import datetime
import backtrader as bt
import backtrader.feeds as btfeed

# crumb = None
# sess = requests.Session()
# sess.headers['User-Agent'] = 'backtrader'

class SmaCross(bt.Strategy):
    params = dict(
        pfast=8,
        pslow=20
    )

    def __init__(self):
        ema1 = bt.ind.EMA(period=self.p.pfast)
        ema2 = bt.ind.EMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(ema1, ema2)

        sma1 = bt.ind.SMA(period=3)
        sma2 = bt.ind.SMA(period=8)
        self.crossover_down = bt.ind.CrossOver(sma1, sma2)
		
    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()

        elif self.crossover_down < 0:
            self.close()


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
df = yf.download('TSLA', start = '2022-01-01')

feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)
cerebro.addstrategy(SmaCross)  # Add the trading strategy
cerebro.broker.setcommission(commission = 0.005)
cerebro.addsizer(bt.sizers.PercentSizer, percents=50)
cerebro.addanalyzer(bt.analyzers.AnnualReturn,_name = 'areturn')
teststrat = cerebro.run()  # run it all
cerebro.plot()  # and plot it with a single command
print(teststrat[0].analyzers.areturn.get_analysis())

