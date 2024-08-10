import backtrader as bt
import backtester
from logger import logger
import os

class CommonStrategy(bt.Strategy):
    params = (
        ('slow', 15),
        ('fast', 30),
        ('printlog', True),
    )
    
    myLogger = logger(name='trade', filename='trade.log')

    # Todo: add strategy name into log
    def log(self, txt, level='info', dt=None, doprint=False):       
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            msg = '%s, %s' % (dt.isoformat(), txt)
            match level:
                case 'debug':
                    self.myLogger.logger.debug(msg)
                case 'info':
                    self.myLogger.logger.info(msg)
                case 'warning':
                    self.myLogger.logger.warning(msg)
                case 'error':
                    self.myLogger.logger.error(msg)
                case 'critical':
                    self.myLogger.logger.critical(msg)
                case _:
                    pass
                    
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.slow)
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.fast)
        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25).subplot = True
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0]).plot = False


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' % 
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          ))
                
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' % 
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))     
                       
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Maring/Rejected')

        self.order = None
        
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
        
class FallingThreeStep(CommonStrategy):
    params = (
        ('exitbars', 5),
    )

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if(self.dataclose[0] < self.dataclose[-1] and
                self.dataclose[-1] < self.dataclose[-2]):
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()
        else:
            if len(self) >= (self.bar_executed + self.params.exitbars):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()

class SimpleSMA(CommonStrategy):
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        
        if self.order:
            return
        
        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()
