import pandas as pd
from binance.exceptions import BinanceAPIException, BinanceOrderException
import conexion
import funciones


class CriptoBot():
    def __init__(self, cripto, time, fecha):
        self.cliente = conexion.cliente
        self.cripto = cripto
        self.time = time #temporalidad
        self.fecha = fecha
        self.data_df = funciones.datos_ticker(self.cripto, self.time, self.fecha)
        """Valores por defecto"""
        self.HMA_L = 80,
        self.HMA_C = 50

    def log(self):
        """Resgistro de actividad del bot"""
        pass

    def parser(self, data):
        data_parser = pd.concat([self.data_df, data])
        print(data_parser)
        return data_parser

    def last_data(self):
        """actualizar datos necesarios para la toma de decisiones"""
        data_update = self.data_df.iloc[[-1]]
        self.data_df = self.parser(data_update)
        pass

    def estrategia(self):
        """elegir estrategia"""
        pass

    def order(self):
        """venta, comrpra, resumen llamado al metodo log"""
        pass


#bot = CriptoBot('BTCUSDT','1d','marzo 2021')
#bot.last_data()

d = funciones.datos_ticker('BTCUSDT', '1d', '81 days ago')
print(d)