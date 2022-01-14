from indicadores import *
import funciones

class Cruce_hma():
    def __init__(self, df, periodo_mayor, periodo_menor):
        self.market = 0
        self.df = df
        self.periodo_mayor = periodo_mayor
        self.periodo_menor = periodo_menor
        self.precio_actual = float(self.df['close'][-1:])
        self.vela_anterior = float(self.df['close'][-2:-1])
        self.dos_velas_antes = float(self.df['close'][-3:-2])
        self.hma_mayor = HMA(self.df, periodo_mayor)
        self.hma80 = self.hma_mayor + (self.hma_mayor * 0.022)  # acercar lo mas posible al valor debido a la variacion
        self.hma_menor = HMA(df, periodo_menor)
        self.hma50 = self.hma_menor + (self.hma_menor * 0.0053)
        self.balance = funciones.balance()
        self.lista_precio = []


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
        pass


