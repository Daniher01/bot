import numpy as np
import pandas as pd
from binance.exceptions import BinanceAPIException, BinanceOrderException
import conexion
import estrategias
import funciones
import backtesting




class CriptoBot():
    def __init__(self, time, limite):
        self.cliente = conexion.cliente
        self.lista_cripto = ['BTCUSDT', 'SOLUSDT', 'DOTUSDT', 'LUNAUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT']
        self.time = time #temporalidad
        self.limite = limite
        self.data_df = ''
        """Valores por defecto"""
        self.HMA_L = 80
        self.HMA_C = 50

    def log(self):
        """Resgistro de actividad del bot"""
        pass

    def estrategia(self):
        """elegir estrategia"""
        cumple = estrategias.cruce_hma(self.data_df, self.HMA_L, self.HMA_C)
        return cumple

    def cripto(self, cripto):
        self.data_df = funciones.datos_ticker(cripto, self.time, self.limite)
        print(cripto)
        self.estrategia()
        pass

    def avisar(self):
        """venta, comrpra, resumen llamado al metodo log"""
        #avisar mediante telegram
        for i in self.lista_cripto:
            self.data_df = funciones.datos_ticker(i, self.time, self.limite)
            print(i)
            self.estrategia()
            print('')
        pass


#bot = CriptoBot('1d', 80)
#bot.avisar()
