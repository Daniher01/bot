from indicadores import *
import funciones

class Cruce_hma():
    def __init__(self, df, periodo_mayor_mayor,periodo_medio, periodo_menor):
        self.market = 0
        self.df = df
        self.periodo_mayor_mayor = periodo_mayor_mayor
        self.periodo_mayor = periodo_medio
        self.periodo_menor = periodo_menor
        self.precio_actual = float(self.df['close'][-1:])
        self.vela_anterior = float(self.df['close'][-2:-1])
        self.dos_velas_antes = float(self.df['close'][-3:-2])
        self.hma_200 = HMA(df, periodo_mayor_mayor)
        self.hma200 = self.hma_200 + (self.periodo_mayor_mayor * 0.0053)
        self.hma_80 = HMA(self.df, periodo_medio)
        self.hma80 = self.hma_80 + (self.hma_80 * 0.022)  # acercar lo mas posible al valor debido a la variacion
        self.hma_50 = HMA(df, periodo_menor)
        self.hma50 = self.hma_50 + (self.hma_50 * 0.0053)
        self.balance = funciones.balance()
        self.lista_precio = []
        self.es_alcista = False


    def buy(self):
        if self.hma80 > self.hma50 and self.precio_actual > self.hma80:
            self.market = 2
            if self.hma80 > self.hma50 and self.vela_anterior > self.hma80:
                if self.precio_actual > self.dos_velas_antes and self.precio_actual > self.vela_anterior:
                    self.market = 1
        return self.hma80, self.hma50 ,self.precio_actual

    def sell(self, precio_compra):
        if self.hma80 < self.hma50 and self.precio_actual < self.hma50 and self.market == 1 and float(precio_compra) < self.precio_actual:
            self.compra_precio = 0
            self.market = -2
            if self.precio_actual < self.hma80 and self.vela_anterior < self.hma50:
                self.market = -1
                return True
            else:
                return False

    def alcista_bajista(self):
        #ALCISTA
        if self.hma50 > self.hma80 and self.hma_80 > self.hma200:
            if self.es_alcista != True:
                self.es_alcista = True
        #BAJISTA
        elif self.hma80 > self.hma200 and self.hma50 > self.hma200:
                if self.precio_actual < self.vela_anterior and self.dos_velas_antes < self.hma200:
                    if self.es_alcista != False:
                        self.es_alcista = False
        return self.hma50, self.hma80, self.hma200, self.precio_actual


class DCA():
    def __init__(self, df):
        self.df = df
        self.precio_actual = float(self.df['close'][-1:])
        self.ath = 0

    def saberATH(self):
        for precio in self.df['close']:
            if precio > self.ath:
                self.ath = precio
        return self.ath


"""d = funciones.datos_ticker('BTCUSDT', '1d', 200)
dd = DCA(d)
print(dd.saberATH())"""
