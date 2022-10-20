import urllib.request,requests
from urllib import error
from socket import timeout
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import alpaca_trade_api as tradeapi
import pandas_market_calendars as mcal

import sys,time,csv,os,os.path,json,re
import pandas_ta as ta
import datetime as dt
import pytz
from alpaca_trade_api.rest import TimeFrame

ohlc_dict = {'open':'first', 'high':'max', 'low':'min', 'close':'last'}
k=0;endstr=''
ACCESS_TOKEN='sAB72PY0qTX2BwvHMtQWIyGptnoP'
API_BASE_URL='https://sandbox.tradier.com/v1/'
api_key='SGXR259QZPZOZQLKZSGHRWDVLHXD4GC5@AMER.OAUTHAP'
redirect_uri='https://127.0.0.1'
api_key = 'PKQ8SM9R5B2RR6J6AY6N'
api_secret = 'q0BeUInFZCrmX717748dDQfx1RHes3VdDkNZoyCj'
base_url = 'https://paper-api.alpaca.markets'

api_key = 'PKDW9HHLEIMRNTO3KS8X'
api_secret = 'GKwPri0yLmdSOlm5KgfzzyhE7POgfDHWu7tGJ2Fr'

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
min2=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
f=open(r'error.csv','w');f.write('');f.close()
f=open(r'error18.csv','w');f.write('');f.close()

def get_two(): # run From Monday 21:00 to Friday 21:00
	tz = pytz.timezone('America/New_York')
	US_today = datetime.now(tz).strftime("%Y-%m-%d")
	US_last=(datetime.now(tz)-timedelta(days=7)).strftime('%Y-%m-%d')

	nyse = mcal.get_calendar('NYSE')
	early = nyse.schedule(start_date=US_last, end_date=US_today)
	US_before=str(early.index[-3]).split(' ')[0]
	US_last=str(early.index[-2]).split(' ')[0]
	US_today=str(early.index[-1]).split(' ')[0]
	US_15=(datetime.now()-timedelta(hours=12,minutes=16)).strftime('%Y-%m-%d %H:%M:%S')
	print(US_15)
	
	return(US_before, US_last, US_15)
def def_txt2(mystr):
	UTC = pytz.timezone('America/New_York')
	time_now = dt.datetime.now(tz=UTC)
	time_15_min_ago = time_now - dt.timedelta(days=3,minutes=15)
	print(time_15_min_ago,time_now)
	min2=str(time_15_min_ago)
	inputstr='\n'+min2+'\t'+str(mystr)
	f=open(r'error.csv','a+');f.write(inputstr);f.close()
# ('UTC')
UTC = pytz.timezone('America/New_York')


		
def get_bar_min_tdd(symbols, N):
	time_now = dt.datetime.now(tz=UTC)
	time_15_min_ago = time_now - dt.timedelta(minutes=15)
	time_15_min_ago = time_now - dt.timedelta(days=2,minutes=15)
	time_1_hr_ago = time_now - dt.timedelta(hours=N*480)#1440

	today=datetime.today().strftime('%Y-%m-%d')
		
	lastd=(datetime.now()-timedelta(days=N * 7)).strftime('%Y-%m-%d')
	befored,lastd,today = get_two()
	
	symbols = symbols.replace('US.','')
	if len(symbols)>100:
		print('symbols overloaded, return')
	print(symbols)

	N_min = '3Min';	num = 20
		
	N_min = str(N) + 'Min'	
# start = pd.Timestamp('2010-01-01', tz='America/New_York').isoformat()
	try:
	# if True: time_1_hr_ago
		print('\t\t\t\t Minute ',N_min)
		api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
		
		data_df = api.get_bars(symbols, N_min, 
					 start=time_1_hr_ago.isoformat(), 
					 end=time_15_min_ago.isoformat(), 
					 adjustment='raw'
					 ).df
		data_df.index = data_df.index.tz_convert('America/New_York')
		df_api = data_df.copy()
		if len(df_api)==0:
			return None
		print(symbols, N_min, len(df_api), df_api.tail(1))
	except Exception as e:
		print(e)
		return None

	df_all = pd.DataFrame({'open':[],'high':[],'low':[],'close':[],'time_key':[]})
	df_resh = pd.DataFrame({'open':[],'high':[],'low':[],'close':[],'time_key':[]})

	df_all = df_api.copy()
	df_all.dropna(inplace=True)
	df_all['time_key'] = str(df_all.index)[0:19]

	return(df_api)