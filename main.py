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
#import criptoClass




class CriptoBot():
    def __init__(self):
        self.cliente = binanceConnect
        self.simbolo = 'BTCUSDT'
        self.time = '1d'
        self.RUN = True
        self.ath_temporal = 0 #guardar el precio al momento de hacer la compra
        self.descripcion = 'Registro_compra' #descripcion para el nombre del csv
        self.csv_cripto = 'Lista_criptos.csv' #nombre del CSV donde esta la lista de las criptos
        """Se le asigna el tiempo del servidor"""
        self.seconds = 0
        self.minute = 0
        self.hour = 0

    def log(self, cripto, precio_compra):
        """Resgistro de actividad del bot"""
        print('function::log ')
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
            if balance['asset'][d] == cripto:
                liquidez = float(balance['free'][d])
                bloqueado = float(balance['locked'][d])
                return cripto, liquidez, bloqueado

    def hayNuevoATH(self):
        print('function::hayNuevoATH')
        datos = funciones.datos_ticker(self.simbolo, self.time, 2)
        precio_ayer = datos['close'][0]
        precio_actual = datos['close'][1]
        self.ath_temporal = precio_ayer
        if precio_actual >= precio_ayer:
            self.ath_temporal = precio_actual
            return True #hay nuevo ath temporal
        else:
            return False #no hay nuevo ath temporal



    def estrategia(self):
        print('function::estrategia')
        """elegir estrategia"""
        #SABER EL PRECIO ACTUAL EN RELACION CON EL CIERRE DEL DIA ANTERIOR
        if self.hayNuevoATH():
            """ --cancela las ordenes de compra pendientes
                --toma ganancias (definir que porcentaje de ganancia) """
            print('se cancelan las ordenes pendientes y se toman ganancias')
        else:
            moneda, liquidez, bloqueado = self.buscar_moneda('USDT')
            cantidad_min, cantidad_max, cantidad_min_dolar =  funciones.cantidad_min_max(self.simbolo)
            if bloqueado == 0: #si no tengo ordenes pendientes
                #SABER SI TENGO BALANCE POSITIVO PARA HACER COMPRA
                if liquidez > cantidad_min_dolar:
                    print('tienes para comprar')
                    """crea ordenes de compra a porcentajes menores del ath temporal
                            saber que porcentaje colocar en cada compra segun la liquidez"""
                    funciones.ejecutarOrden(self.simbolo, 'BUY', 11, self.ath_temporal - 15000)
                else:
                    print('no tienes para comprar')
                    """no hacer nada"""
            else:
                """no hacer nada"""
                print('ya tienes ordenes pendientes')


    def tiempo(self):
        print('function::tiempo')
        time_res = conexion.cliente.get_server_time()
        ts = time_res.get('serverTime')
        self.seconds = datetime.utcfromtimestamp(ts / 1000).second
        self.minute = datetime.utcfromtimestamp(ts / 1000).minute
        self.hour = datetime.utcfromtimestamp(ts / 1000).hour
        pass

d = CriptoBot()
d.estrategia()
