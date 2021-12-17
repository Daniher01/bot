import backtrader as bt
import datetime as dt

import dateparser


class Strategy(bt.Strategy):

    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('', self.dataclose[0].cose)
        if self.dataclose[0] < self.dataclose[-1]:
            if self.dataclose[-1] < self.dataclose[-2]:
                self.log('BUY CREATE', self.dataclose[0])
                self.buy()

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date[0]
        print('{} {}'.format(dt, txt))


cerebro = bt.Cerebro()

cerebro.addstrategy(Strategy)

data = bt.feeds.GenericCSVData(
    name='BTCUSDT',
    dataname='BTCUSDT-1d-data-enero 2021.csv',
    timeFrame = bt.TimeFrame.Days,
    fromdate = dt.datetime(2021, 1, 17),
    todate = dt.datetime(2021, 12, 17),
    nullvalue = 0.0
)
cerebro.adddata(data)
cerebro.broker.setcash(10000.0)
print('Portafolio inicial: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Portafolio final: %.2f' % cerebro.broker.getvalue())

#d = dt.datetime.strptime('2021-01-17', '%Y-%m-%d ')
#print(d)