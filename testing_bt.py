import backtrader as bt
import datetime as dt

class Strategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        self.sma50 = bt.indicators.EMA(period=50)
        self.sma80 = bt.indicators.EMA(period=80)
        self.dataclose = self.datas[0].close


    def prenext(self):
        self.log('Close, %.2f' % self.dataclose[0])
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.sma80 > self.sma50 and self.dataclose[0] > self.sma80:
            self.buy()
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
        elif self.sma80 < self.sma50 and self.dataclose[0] < self.sma80:
            self.sell()
            self.log('SELL CREATE, %.2f' % self.dataclose[0])

    def stop(self):
        print(self.position)

class Strategy1(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        self.sma50 = bt.indicators.SMA(period=50)
        self.sma80 = bt.indicators.SMA(period=80)
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def prenext(self):
        self.log('Close, %.2f' % self.dataclose[0])
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        if not self.position:
            if self.sma80 > self.sma50 and self.dataclose[0] > self.sma80:
                self.buy()
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
        else:
            if self.sma80 < self.sma50 and self.dataclose[0] < self.sma80:
                self.sell()
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

    def stop(self):
        print(self.position)

class RSIStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=14)

    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy()
        if self.rsi > 70 and self.position:
            self.close()


"""
COLOCAR EN EL MAIN
"""

"""
cerebro = bt.Cerebro()

data = bt.feeds.GenericCSVData(
    name = 'BTC',
    dataname = 'BTCUSDT-1h-data-enero 2021.csv',
    timeframe = bt.TimeFrame.Days,
    fromdate = dt.datetime(2021, 1, 20),
    todate = dt.datetime(2021, 12, 20),
    nullvalue = 0.0
)

cerebro.adddata(data)
cerebro.addstrategy(testing_bt.Strategy1)
cerebro.broker.setcash(10000)
print('portafolio inicial: %.2f' %cerebro.broker.getvalue())
cerebro.run()
print('portafolio final: %.2f' %cerebro.broker.getvalue())
"""



