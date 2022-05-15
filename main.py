import time
from os import path, remove
from datetime import datetime
import os
import pandas as pd
from telegram.ext import Updater, CommandHandler
import conexion
import config
from conexion import binanceConnect
from estrategias import *
import funciones
import csv
#import backtesting
import criptoClass




class CriptoBot():
    def __init__(self):
        self.cliente = conexion.cliente
        self.lista_cripto = 'BTCUSDT'
        self.time = '1d'
        self.limite = 80
        self.data_df = ''
        self.valor_hma80 = ''
        self.valor_hma50 = ''
        """Valores por defecto"""
        self.HMA_L = 80
        self.HMA_C = 50
        self.RUN = True
        self.accion = 0 #1 esta en compra, -1 esta en venta
        self.precio_compra = 0 #guardar el precio al momento de hacer la compra
        self.descripcion = 'Registro_compra' #descripcion para el nombre del csv
        self.csv_cripto = 'Lista_criptos.csv' #nombre del CSV donde esta la lista de las criptos
        self.mensaje = None
        self.tradingView_pag = 'https://WWW.tradingview.com/chart/UBCV9gCj/?symbol='
        self.binance_pag = 'https://www.binance.com/es/trade/'
        """Se le asigna el tiempo del servidor"""
        self.seconds = 0
        self.minute = 0
        self.hour = 0

    def log(self, cripto, precio_compra):
        """Resgistro de actividad del bot"""
        old, new = funciones.tiempo_server()
        lista_registro = [[cripto], [precio_compra], [new]]
        registro_df = pd.DataFrame(lista_registro)
        if not path.exists('%s-%s-data.csv' % (cripto, self.descripcion)):
            funciones.get_csv(registro_df, cripto, self.descripcion)
        else:
            pass
        pass

    def buscar_moneda(self, cripto):
        balance = funciones.balance()
        for d in range(len(balance)):
            if balance['asset'][d] + 'USDT' == cripto:
                return cripto

    def estrategia(self, cripto):
        """elegir estrategia"""
        estrategias = Cruce_hma(self.data_df, self.HMA_L, self.HMA_C)
        self.valor_hma80,self.valor_hma50 ,self.precio_compra = estrategias.buy() #precion de compra
        if path.exists('%s-%s-data.csv' % (cripto, self.descripcion)): #para la venta
            print('Leyendo el precio de compra')
            registros_df = funciones.leer_csv(cripto, self.descripcion) #se lee el precio de compra
            precio_compra = registros_df[1][2]
            vender = estrategias.sell(precio_compra)
            if vender == True:
                remove('%s-%s-data.csv' % (cripto, self.descripcion)) #se lee el precio y elimina el archivo
        cumple = estrategias.market
        return cumple

    def tiempo(self):
        time_res = conexion.cliente.get_server_time()
        ts = time_res.get('serverTime')
        self.seconds = datetime.utcfromtimestamp(ts / 1000).second
        self.minute = datetime.utcfromtimestamp(ts / 1000).minute
        self.hour = datetime.utcfromtimestamp(ts / 1000).hour
        pass



