from datetime import datetime
import backtrader as bt
import json,os,sys,csv,time
import requests
import pandas as pd
import yfinance as yf
import backtrader.feeds as btfeed
os.environ["http_proxy"] = "http://127.0.0.1:10809"
os.environ["https_proxy"] = "http://127.0.0.1:10809"#7890

class TestStrategy(bt.Strategy):
    def __init__(self):
        self.bbands = bt.ind.BollingerBands()
        sma0 = bt.ind.SMA(period=1)
        sma1 = bt.ind.SMA(period=3)
        sma2 = bt.ind.SMA(period=8)
        self.crossover = bt.ind.CrossOver(sma0, self.bbands.lines.top)

        self.crossover_down = bt.ind.CrossOver(sma0, self.bbands.lines.bot)
    def next(self):
        if not self.position:
        # if True:
            if self.crossover_down < 0:
                self.buy()
            if self.crossover > 0:
                self.close()

##########################
def file_name_walk(file_dir):
	files = []
	for root, dirs, files in os.walk(file_dir):
		len(files)
	return files
path_s = 'junxianshuju/'
file_s=file_name_walk(path_s)
for f in file_s:
	if f[0] == '.':
		file_s.remove(f)
		print('remove ',f)
fn = path_s + file_s[-1]
FN_final = fn
if os.path.isfile(FN_final):
	with open(FN_final,'r') as csvfile:
		reader = csv.reader(csvfile)
		rows = [row[0] for row in reader]
	csvfile.close	
	if rows[0].isupper()==False:
		rows.pop(0)
	symbols=rows[0:10]
print(symbols)
#######################
df_all = pd.DataFrame({'symbol':[],'year':[],'annualreturn':[]})
today=datetime.today().strftime('%Y-%m-%d')
start_date = '2020-01-01'
def stock_test(symbol):
	cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
	df = yf.download(symbol, start = start_date)
	# print(df.tail(1))
	feed = bt.feeds.PandasData(dataname=df)
	cerebro.adddata(feed)
	cerebro.addstrategy(TestStrategy)  # Add the trading strategy
	cerebro.broker.setcommission(commission = 0.005)
	cerebro.addsizer(bt.sizers.PercentSizer, percents=50)
	cerebro.addanalyzer(bt.analyzers.AnnualReturn,_name = 'areturn')
	teststrat = cerebro.run()
	# cerebro.plot()

	analyzers = teststrat[0].analyzers.areturn.get_analysis()
	# print(analyzers)
	v = list(analyzers.values())
	k = list(analyzers.keys())
	s = [symbol] * len(v)

	df = pd.DataFrame({'symbol':s,'year':k,'annualreturn':v})
	df['annualreturn']=df['annualreturn'].map(lambda x:("%.3f")%x)
	df['year'] = df['year'].astype(int)
	print(start_date,today, '\t', symbol)
	df = df.drop(index=df[df['year']==2019].index[0])
	df.reset_index(drop=True, inplace=True)
	print(df)
	time.sleep(2)
	return(df)
	
for symbol in symbols:
	df_all = df_all.append(stock_test(symbol))
print(df_all)
