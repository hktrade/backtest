from datetime import datetime
import backtrader as bt
import json,os,sys
import requests
import pandas as pd

import datetime
import backtrader as bt
import backtrader.feeds as btfeed

from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
def def_txt(mystr):
	min2 = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	inputstr='\n'+str(mystr)
	if os.stat(r'error.csv').st_size == 0:
		f=open(r'error.csv','w',encoding='utf-8');f.write(inputstr);f.close()
	else:
		f=open(r'error.csv','a+',encoding='utf-8');f.write(inputstr);f.close()
def get_bar_min(symbol,K_M):
	NUM = 100
	if K_M == 3:
		ST=SubType.K_3M;
		ST2= KLType.K_3M;
	elif K_M == 15:
		ST=SubType.K_15M;
		ST2= KLType.K_15M;
	elif K_M == 1:
		ST=SubType.K_1M;
		ST2= KLType.K_1M;
	elif K_M == 5:
		ST=SubType.K_5M;
		ST2= KLType.K_5M;
	elif K_M == 30:
		ST=SubType.K_30M;
		ST2= KLType.K_30M;
	ret_sub, err_message = quote_ctx.subscribe(symbol, [SubType.K_30M,SubType.K_1M,SubType.K_5M,SubType.K_15M], subscribe_push=False)

	ret, data3 = quote_ctx.get_cur_kline(symbol, 500, ST2)
	if ret_sub == -1:
		def_txt(str(err_message)+' in get_bar_min')
		return None
	if ret == -1:
		def_txt(str(data3)+' in get_bar_min')
		return None

	data3.index = pd.to_datetime(data3['time_key'])

	return data3


class TestStrategy(bt.Strategy):
    params = dict(
        pfast=8,
        pslow=20
    )

    def __init__(self):
        self.bbands = bt.ind.BollingerBands()

        self.crossover = bt.ind.CrossOver(self.data.close, self.bbands.lines.top)

        self.crossover_down = bt.ind.CrossOver(self.data.close, self.bbands.lines.bot)
		
    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.sell()
                def_txt(str(self.datas[0].datetime)+' '+str(self.data.close[0])+' close')
        else:
            if self.crossover_down > 0:
                self.close()
                def_txt(str(self.datas[0].datetime)+' '+str(self.data.close[0])+' buy')

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

symbol = 'HK.00700'
ret_sub, err_message = quote_ctx.subscribe(['HK.00700'], [SubType.K_1M,SubType.K_3M,SubType.K_15M], subscribe_push=False)
# print(ret_sub,err_message)

df = get_bar_min(symbol, 5)
if df is None:
	quote_ctx.close()
	sys.exit()
feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)
cerebro.addstrategy(TestStrategy)  # Add the trading strategy
cerebro.broker.setcommission(commission = 0.005)
cerebro.addsizer(bt.sizers.PercentSizer, percents=50)
cerebro.addanalyzer(bt.analyzers.AnnualReturn,_name = 'areturn')
teststrat = cerebro.run()  # run it all
cerebro.plot()

analyzers = teststrat[0].analyzers.areturn.get_analysis()

v = list(analyzers.values())
k = list(analyzers.keys())
s = [symbol] * len(v)

df = pd.DataFrame({'symbol':s,'year':k,'annualreturn':v})
df['annualreturn']=df['annualreturn'].map(lambda x:("%.3f")%x)

print(df)

quote_ctx.close()
sys.exit()