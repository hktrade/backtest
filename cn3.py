from datetime import datetime
import backtrader as bt# import backtrader.feeds as btfeeds
import json,os,sys
import requests
import pandas as pd
import yfinance as yf

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
		
	ret_sub, err_message = quote_ctx.subscribe(symbol, [SubType.K_1M,SubType.K_3M,SubType.K_5M,SubType.K_15M], subscribe_push=False)
	print(ret_sub, err_message)
	if K_M != 10:
		ret, data3 = quote_ctx.get_cur_kline(symbol, 500, ST2)
		if ret_sub == -1:
			def_txt(str(err_message)+' in get_bar_min')
			return None
		if ret == -1:
			def_txt(str(data3)+' in get_bar_min')
			return None

		data3.index = pd.to_datetime(data3['time_key'])
		# print(data3.tail(2))
		return data3

	if K_M == 10:
		ret, data3 = quote_ctx.get_cur_kline(symbol, 500, KLType.K_5M)
		df = pd.DataFrame({})

		for i in range(len(data3)):
			if i%2!=0 and i>1:
				df=df.append({'time_key':data3['time_key'].iloc[i],'open':data3['open'].iloc[i-2],
				'high':data3['high'].iloc[i-2:i].max(),'low':data3['low'].iloc[i-2:i].min(),
				'close':data3['close'].iloc[i],'volume':data3['volume'].iloc[i-2:i].sum()},ignore_index=True)
		df.index = pd.to_datetime(df['time_key'])
		print(df.tail(3))
		return df

class TestStrategy(bt.Strategy):
    params = dict(
        pfast=8,
        pslow=20
    )

    def __init__(self):
        self.bbands = bt.ind.BollingerBands()
        sma0 = bt.ind.SMA(period=1)
        # sma1 = bt.ind.SMA(period=3)
        # sma2 = bt.ind.SMA(period=8)
        # ema0 = bt.ind.EMA(period=1)
        # ema1 = bt.ind.EMA(period=3)
        # ema2 = bt.ind.EMA(period=8)
        self.crossover = bt.ind.CrossOver(sma0, self.bbands.lines.top)
        
        # self.crossover_down = bt.ind.CrossOver(sma1, sma2)
        self.crossover_down = bt.ind.CrossOver(sma0, self.bbands.lines.bot)
		
    def next(self):
        if not self.position:
        # if True:
            if self.crossover_down < 0:
                self.buy()
                def_txt(str(self.datas[0].datetime)+' '+str(self.data.close[0])+' buy')
        else:
            if self.crossover > 0:
                self.close()
                def_txt(str(self.datas[0].datetime)+' '+str(self.data.close[0])+' close')

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
start_date = '2020-01-01'

symbol = 'TSLA'
# df = yf.download(symbol, start = start_date)

# no 10 M
symbol = 'SH.510050'
ret_sub, err_message = quote_ctx.subscribe(['HK.00700'], [SubType.K_1M,SubType.K_3M,SubType.K_15M], subscribe_push=False)
print(ret_sub,err_message)

df = get_bar_min(symbol, 10)
if df is None:
	quote_ctx.close()
	sys.exit()
feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)
cerebro.addstrategy(TestStrategy)  # Add the trading strategy
cerebro.broker.setcommission(commission = 0.001)
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
print(start_date, '\t', symbol)
print(df)

quote_ctx.close()
sys.exit()