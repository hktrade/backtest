from datetime import datetime
import backtrader as bt# import backtrader.feeds as btfeeds
import json,os,sys
import requests
import yfinance as yf
import backtrader.feeds as btfeed
from idc import *
# os.environ["http_proxy"] = "http://127.0.0.1:10809"
# os.environ["https_proxy"] = "http://127.0.0.1:10809"#7890

	# df['20sma'] = df['close'].rolling(window=20).mean()
	# df['stddev'] = df['close'].rolling(window=20).std()
	# df['bbl'] = df['20sma'] - (2 * df['stddev'])
	# df['bbh'] = df['20sma'] + (2 * df['stddev'])
        # self.lines.mid = ma = self.p.movav(self.data, period=self.p.period)
        # stddev = self.p.devfactor * StdDev(self.data, ma, period=self.p.period,
                                           # movav=self.p.movav)
        # self.lines.top = ma + stddev
        # self.lines.bot = ma - stddev
class TestStrategy(bt.Strategy):
    params = (
        ("period", 20),
        ("devfactor", 2.8),
        ("size", 20),
        ("debug", False)
    )

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)

    def next(self):
        if not self.position:
        # if True:
            if self.data.low > self.boll.lines.top :
                self.sell()
        if self.position:		
            if self.data.high < self.boll.lines.bot :
                self.close()

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
start_date = '2021-10-01'
symbol = 'TSLA'
# df = yf.download(symbol, start = start_date)
if len(sys.argv)>2:
	df = get_bar_min_tdd(sys.argv[1], int(sys.argv[2]))
	symbol = sys.argv[1]
else:
	df = get_bar_min_tdd(symbol, 3)

today=datetime.today().strftime('%Y-%m-%d')
print(today, '\t', symbol)

if df is None:
	print('df is None')
	sys.exit()
feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)
cerebro.addstrategy(TestStrategy)
cerebro.broker.setcommission(commission = 0.005)
cerebro.addsizer(bt.sizers.PercentSizer, percents=50)
cerebro.addanalyzer(bt.analyzers.AnnualReturn,_name = 'areturn')
teststrat = cerebro.run()
print(teststrat[0].analyzers.areturn.get_analysis())
print(df.head(1),'',df.tail(1))
fn = 'analyzers/' + symbol + '.csv'
f=open(fn,'a+');f.write(str(df.index[0])+' '+symbol+' '+str(teststrat[0].analyzers.areturn.get_analysis())+'\n');f.close()
cerebro.plot()