from indicadores import *
import funciones


"""def cruce_hma(df, periodo_mayor, periodo_menor): #estrategia solo para opciones BUY
    try:
        precio_actual = float(df['close'][-1:])
        vela_anterior = float(df['close'][-2:-1])
        dos_velas_antes = float(df['close'][-3:-2])
        hma80 = HMA(df, periodo_mayor)
        hma80 = hma80 + (hma80*0.022) #acercar lo mas posible al valor debido a la variacion
        hma50 = HMA(df, periodo_menor)
        hma50 = hma50 + (hma50*0.0053)
        #ejecutar opcion de compra
        if hma80 > hma50 and precio_actual > hma80:
            print('Cruce medias moviles')
            print('HMA80: ', hma80)
            print('HMA50: ', hma50)
            Market = None
            if dos_velas_antes > hma80 and vela_anterior < precio_actual and dos_velas_antes < precio_actual:
                print('Oportunidad de compra')
                Market = True
        elif hma50 > hma80 and precio_actual < hma50:
            print('cerrar 50% de operacion')
            Market = None
            if hma50 > hma80 and vela_anterior < hma50 and precio_actual < hma80:
                print('Cerrar Operacion')
                Market = False
        else:
            print('No se esta cumpliendo la estrategia')
            Market = None
    except Exception as e:
        Market = None
        print('ERRORrr: ', e)
    return Market
    #retorna booleano """

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
            if self.hma80 > self.hma50 and self.dos_velas_antes > self.hma80:
                if self.precio_actual > self.dos_velas_antes and self.precio_actual > self.vela_anterior:
                    self.market = 1
        return self.precio_actual

    def sell(self, precio_compra):
        if self.hma80 < self.hma50 and self.precio_actual < self.hma50 and self.market == 1 and float(precio_compra) < self.precio_actual:
            self.compra_precio = 0
            self.market = -2
            if self.precio_actual < self.hma80 and self.vela_anterior < self.hma50:
                self.market = -1


