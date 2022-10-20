class MyStrategy(bt.Strategy):

    def __init__(self):
        self.sma = btind.SimpleMovingAverage(period=15)

    def next(self):
        if self.sma > self.data.close:
            # Do something
            pass

        elif self.sma < self.data.close:
            # Do something else
            pass
			
import backtrader as bt

class MyStrategy(bt.Strategy)
    def __init__(self):
        self.the_highest_high_15 = bt.ind.Highest(self.data.high, period=15)

    def next(self):
        if self.the_highest_high_15 > X:
            print('ABOUT TO DO SOMETHING')

			
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import time
start_time = time.time()
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import pandas as pd
import matplotlib
import os
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pytz
import numpy as np
from pandas import DataFrame
import backtrader as bt
from collections import OrderedDict
import tabulate



# DataImportVar
fromdate = datetime.datetime(2021, 2, 7, 12, 00)
todate = datetime.datetime(2021, 4, 9, 19, 00)
# SessionTimeFilter
Session_begin = datetime.time(12, 0)
Session_end = datetime.time(19, 0)

if os.getcwd()=='/Users/frankie/PycharmProjects/pythonProject3':
    Directory = '/Users/frankie'
else:
    Directory='/Users/francescocerutti_imac_hs/Desktop/FrankieHD27'

class TotalReturns(bt.Analyzer):
    '''This analyzer reports the total pnl for strategy

    Params:

      - timeframe (default: ``None``)
        If ``None`` then the timeframe of the 1st data of the system will be
        used

      - compression (default: ``None``)

        Only used for sub-day timeframes to for example work on an hourly
        timeframe by specifying "TimeFrame.Minutes" and 60 as compression

        If ``None`` then the compression of the 1st data of the system will be
        used

    Methods:

      - get_analysis

        Returns a dictionary with returns as values and the datetime points for
        each return as keys
    '''

    def __init__(self):
        self.total_pnl = 0
        self.unrealized = 0  # Unrealized pnl for all positions all strategies
        self.positions = OrderedDict.fromkeys([d._name or 'Data%d' % i
                                               for i, d in enumerate(self.datas)], 0)  # Current strategy positions

    def start(self):
        tf = min(d._timeframe for d in self.datas)
        self._usedate = tf >= bt.TimeFrame.Minutes

    def notify_order(self, order):

        if order.status in [order.Completed, order.Partial]:
            self.total_pnl += order.executed.pnl - order.executed.comm

            self.positions[order.data._name] += order.executed.size

    def next(self):
        if self._usedate:
            self.rets[self.strategy.datetime.date()] = self.total_pnl
        else:
            self.rets[self.strategy.datetime.datetime()] = self.total_pnl

    def stop(self):

        for dname in self.positions:
            self.unrealized += (self.strategy.dnames[dname].close[0] -
                                self.strategy.positionsbyname[dname].price) * \
                               self.strategy.positionsbyname[dname].size

    def get_analysis(self):
        return self.rets

'''
class BOLLStrat(bt.Strategy):
    
    This is a simple mean reversion bollinger band strategy.

    Entry Criteria:
        - Long:
            - Price closes below the lower band
            - Stop Order entry when price crosses back above the lower band
        - Short:
            - Price closes above the upper band
            - Stop order entry when price crosses back below the upper band
    Exit Critria
        - Long/Short: Price touching the median line
    

    params = (
        ("period", 20),
        ("devfactor", 2),
        ("size", 20),
        ("debug", False)
    )

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        # self.sx = bt.indicators.CrossDown(self.data.close, self.boll.lines.top)
        # self.lx = bt.indicators.CrossUp(self.data.close, self.boll.lines.bot)

    def next(self):

        orders = self.broker.get_orders_open()

        # Cancel open orders so we can track the median line
        if orders:
            for order in orders:
                self.broker.cancel(order)

        if not self.position:

            if self.data.close > self.boll.lines.top:
                self.sell(exectype=bt.Order.Stop, price=self.boll.lines.top[0], size=self.p.size)

            if self.data.close < self.boll.lines.bot:
                self.buy(exectype=bt.Order.Stop, price=self.boll.lines.bot[0], size=self.p.size)


        else:

            if self.position.size > 0:
                self.sell(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)

            else:
                self.buy(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)

        if self.p.debug:
            print('---------------------------- NEXT ----------------------------------')
            print("1: Data Name:                            {}".format(data._name))
            print("2: Bar Num:                              {}".format(len(data)))
            print("3: Current date:                         {}".format(data.datetime.datetime()))
            print('4: Open:                                 {}'.format(data.open[0]))
            print('5: High:                                 {}'.format(data.high[0]))
            print('6: Low:                                  {}'.format(data.low[0]))
            print('7: Close:                                {}'.format(data.close[0]))
            print('8: Volume:                               {}'.format(data.volume[0]))
            print('9: Position Size:                       {}'.format(self.position.size))
            print('--------------------------------------------------------------------')

    def notify_trade(self, trade):
        if trade.isclosed:
            dt = self.data.datetime.date()

            print('---------------------------- TRADE ---------------------------------')
            print("1: Data Name:                            {}".format(trade.data._name))
            print("2: Bar Num:                              {}".format(len(trade.data)))
            print("3: Current date:                         {}".format(dt))
            print('4: Status:                               Trade Complete')
            print('5: Ref:                                  {}'.format(trade.ref))
            print('6: PnL:                                  {}'.format(round(trade.pnl, 2)))
            print('--------------------------------------------------------------------')

'''
# Create a Strategy
class TestStrategy(bt.Strategy):
    params = (
        ("period", 20),
        ("devfactor", 2.0)
    )

    # The first data in the list self.datas[0] is the default data for trading operations and to keep all strategy elements synchronized (it’s the system clock)
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        dt1 = self.data0.datetime.time(0)
        print('%s,%s, %s' % (dt.isoformat(), dt1.isoformat(), txt))

    '''
    This is a simple mean reversion bollinger band strategy.

    Entry Critria:
        - Long:
            - Price closes below the lower band
            - Stop Order entry when price crosses back above the lower band
        - Short:
            - Price closes above the upper band
            - Stop order entry when price crosses back below the upper band
    Exit Critria
        - Long/Short: Price touching the median line
    '''
    def __init__(self):
        init_time = time.time()
        self.startcash = self.broker.getvalue()
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # Keep a reference to the "close" line in the data[0] dataseries
        self.boll = btind.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        # Signal Booleans
        self.sx = btind.CrossDown(self.data.close, self.boll.lines.top)
        self.lx = btind.CrossUp(self.data.close, self.boll.lines.bot)

        # Indicators for the plotting show
        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25,subplot=True)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:

            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Size: %.2f, OpenPrice: %.2f, Closeprice: %.2f, Comm %.2f' %
                    (order.executed.size,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size
            else:  # Sell
                self.log(
                    'SELL EXECUTED, Size: %.2f, OpenPrice: %.2f, Closeprice: %.2f, Comm %.2f' %
                    (order.executed.size,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm))


        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):

        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):

        if self.data.datetime.time() < Session_begin:
            self.close()  # don't operate until x
            return  #
        if self.data.datetime.time() > Session_end:
            self.close()  # don't operate after y
            return  #

        if self.lx == 1:

            # BUY, BUY, BUY!!! (with all possible default parameters)
            self.close()
            self.log('BUY CREATE, %.2f' % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.order = self.buy()


        elif self.sx == 1:

            # SELL, SELL, SELL!!! (with all possible default parameters)
            self.close()
            self.log('SELL CREATE, %.2f' % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.order = self.sell()

    def stop(self):
        pnl = round(self.broker.getvalue() - self.startcash, 3)
        print('SuTR Period: {} SuTR Mult: {}Final PnL: {}'.format(
            self.params.period, self.params.devfactor, pnl))


if __name__ == '__main__':
    # Variable for our starting cash
    startcash = 100000

    # Create a cerebro entity
    cerebro = bt.Cerebro(optreturn=False)

    # Add a strategy
    cerebro.optstrategy(TestStrategy, period=range(10, 41, 1), devfactor=np.linspace(1.0, 4.0, 31))

    data = btfeeds.GenericCSVData(
        dataname='CME_MINI_NQ1!Actual.csv',

        fromdate=fromdate,
        todate=todate,
        sessionstart=datetime.time(13, 00),
        sessionend=datetime.time(18, 00),

        dtformat=('%Y-%m-%d %H:%M:%S'),
        datetime=1,
        high=3,
        low=4,
        open=2,
        close=5,
        volume=6,
        openinterest=-1,

        timeframe=bt.TimeFrame.Minutes,
        compression=1
    )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    cerebro.addanalyzer(TotalReturns, _name='PNLS')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')

    # Set our desired cash start
    cerebro.broker.setcash(startcash)
    # Set the commission
    cerebro.broker.setcommission(commission=0.00014, mult=20)
    # Run over everything
    print('Run Begin')

    #  #  -------------------------------- SET the cpus --------------------------------  #  #
    opt_runs = cerebro.run(maxcpus=20)
    print('Runs completed: ' + str(len(opt_runs)))