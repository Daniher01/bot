import numpy as np
import pandas as pd
from binance.exceptions import BinanceAPIException, BinanceOrderException
import conexion
import estrategias
import funciones


class CriptoBot():
    def __init__(self, cripto, time, limite):
        self.cliente = conexion.cliente
        self.cripto = cripto
        self.time = time #temporalidad
        self.limite = limite
        self.data_df = funciones.datos_ticker(self.cripto, self.time, self.limite) #trae los ultimos 80 dias
        """Valores por defecto"""
        self.HMA_L = 80
        self.HMA_C = 50

    def log(self):
        """Resgistro de actividad del bot"""
        pass

    """def parser(self, data_parser):
        data = pd.concat([self.data_df, data_parser])
        print(data)
        return data"""

    def last_data(self):
        """actualizar datos necesarios para la toma de decisiones"""
        self.estrategia()
        return self.data_df

    def estrategia(self):
        """elegir estrategia"""
        cumple = estrategias.cruce_hma(self.data_df, self.HMA_L, self.HMA_C)
        return cumple

    def order(self):
        """venta, comrpra, resumen llamado al metodo log"""
        pass

list = ['BTCUSDT', 'SOULSDT', 'DOTUSDT', 'LUNAUSDT']
for i in list:
    print(i)
    bot = CriptoBot(i,'1d', 80)
    bot.last_data()
    print('')

#d = funciones.datos_ticker('BTCUSDT', '1d',80)
#print(d)