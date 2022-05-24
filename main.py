import time
from os import path, remove
from datetime import datetime
import os
import pandas as pd
from telegram.ext import Updater, CommandHandler
import conexion
from conexion import binanceConnect
import funciones
from ordenClass import *
#import backtesting
#import criptoClass




class CriptoBot():
    def __init__(self):
        self.cliente = binanceConnect
        self.simbolo = 'BTCBUSD'
        self.time = '1d'
        self.RUN = True
        self.datosTicker = funciones.datos_ticker(self.simbolo, self.time, 2)
        self.precio_actual = self.datosTicker['close'][1]
        self.ordenClass = ordenClass(self.simbolo)
        self.ath_temporal = 0 #guardar el precio al momento de hacer la compra
        self.descripcion = 'Registro_compra' #descripcion para el nombre del csv
        self.csv_cripto = 'Lista_criptos.csv' #nombre del CSV donde esta la lista de las criptos
        """Se le asigna el tiempo del servidor"""
        self.fechaActual = datetime.now().strftime('%Y-%m-%d')
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
                return cripto, round(liquidez,2), bloqueado

    def hayNuevoATH(self):
        print('function::hayNuevoATH')
        #datos = funciones.datos_ticker(self.simbolo, self.time, 2)
        precio_ayer = self.datosTicker['close'][0]
        self. precio_actual = self.datosTicker['close'][1]
        if self.ath_temporal == 0:
            self.ath_temporal = precio_ayer
        if self.precio_actual >= self.ath_temporal:
            self.ath_temporal = self.precio_actual
            datareturn = True #hay nuevo ath temporal
        else:
            datareturn = False #no hay nuevo ath temporal
        print('ath temporal: ',self.ath_temporal)
        print('precio actual: ', self.precio_actual)
        return datareturn

    """convierte la cantidad de USD a BTC"""
    def convertirCantidad(self, fiat):
        cantidad_en_btc = fiat / self.precio_actual
        cantidad_en_btc = round(cantidad_en_btc, 5)
        print('cantidad de compra en btc: ',cantidad_en_btc)
        return cantidad_en_btc

    """retorna el porcentaje de el monto ingresado"""
    def definirPorcentaje(self,monto, porcentaje):
        return monto * porcentaje

    """define el porcentaje por debajo del precio actual para ejecutar la orden de compra"""
    def definirPrecioCompra(self, porcentaje):
        precio_btc = round(self.precio_actual - (self.precio_actual * porcentaje),2)
        print('precio de compra en btc -> ',precio_btc)
        return precio_btc


    def estrategia(self):
        print('function::estrategia')
        """elegir estrategia"""
        cantidad_min, cantidad_max, cantidad_min_dolar = funciones.cantidad_min_max(self.simbolo)
        #SABER EL PRECIO ACTUAL EN RELACION CON EL CIERRE DEL DIA ANTERIOR
        if self.hayNuevoATH() :
            moneda, liquidez, bloqueado = self.buscar_moneda('BTC')
            porcentaje_btc = round(self.definirPorcentaje(liquidez, 0.25),5)
            print('se cancelan las ordenes pendientes y se toman ganancias')
            dataOrden = self.ordenClass.buscarOrdenes_cripto_status('NEW')
            for id in dataOrden:
                idorden, status = funciones.cancelarOrden(self.simbolo, id[0])
                self.ordenClass.updateOrden(idorden, status)

            if porcentaje_btc > cantidad_min:
                print(f'se venden {porcentaje_btc} btc')
                idorden, status = funciones.ejecutarOrden(self.simbolo, 'SELL',porcentaje_btc,self.precio_actual)
                #idorden = None
                print(porcentaje_btc)
                if idorden != None:
                    self.ordenClass.insertarOrden(idorden, porcentaje_btc, self.precio_actual, 'SELL', datetime.today(), status)

        else: #-------------------------------------------CASO PARA EJECUTAR ORDENES DE COMPRA-------------------------------------------------
            moneda, liquidez, bloqueado = self.buscar_moneda('BUSD')
            if bloqueado == 0: #si no tengo ordenes pendientes
                #SABER SI TENGO BALANCE POSITIVO PARA HACER COMPRA
                if liquidez > cantidad_min_dolar:
                    #COMPRAR CON PORCENTAJES DEL PORTAFOLIO
                    porcentaje_liquidez1 = self.definirPorcentaje(liquidez, 0.25)
                    porcentaje_liquidez2 = self.definirPorcentaje(liquidez, 0.30)
                    porcentaje_liquidez3 = self.definirPorcentaje(liquidez, 0.35)
                    if porcentaje_liquidez1 > cantidad_min_dolar: # si el porcentaje del portafolio se puede ejecutar la compra
                        print(f'tienes para comprar con el {0.25*100}% del portafolio, portafolio total:  {liquidez} ')
                        idorden, status = funciones.ejecutarOrden(self.simbolo, 'BUY', self.convertirCantidad(porcentaje_liquidez1), self.definirPrecioCompra(0.05))
                        if idorden != None:
                            self.ordenClass.insertarOrden(idorden, porcentaje_liquidez1, self.precio_actual, 'BUY', datetime.today(), status)

                            #REVISA QUE TENGA PARA HACER LA SEGUNDA COMPRA
                        if porcentaje_liquidez2 > cantidad_min_dolar: # si el porcentaje del portafolio se puede ejecutar la compra
                            print(f'tienes para comprar con el {0.25*100}% del portafolio: {liquidez} ')
                            idorden, status = funciones.ejecutarOrden(self.simbolo, 'BUY', self.convertirCantidad(porcentaje_liquidez2), self.definirPrecioCompra(0.10))
                            if idorden != None:
                                self.ordenClass.insertarOrden(idorden, porcentaje_liquidez2, self.precio_actual, 'BUY', self.fechaActual, status)

                                # REVISA QUE TENGA PARA HACER LA SEGUNDA COMPRA
                                if porcentaje_liquidez3 > cantidad_min_dolar:  # si el porcentaje del portafolio se puede ejecutar la compra
                                    print(f'tienes para comprar con el {0.25 * 100}% del portafolio: {liquidez} ')
                                    idorden, status = funciones.ejecutarOrden(self.simbolo, 'BUY', self.convertirCantidad( porcentaje_liquidez3),  self.definirPrecioCompra(0.15))
                                    if idorden != None:
                                        self.ordenClass.insertarOrden(idorden, porcentaje_liquidez2, self.precio_actual,
                                                                      'BUY', self.fechaActual, status)
                    else: #el porcentaje del portafolio no llega al minimo para la compra
                        print(f'tienes para comprar solo con el {100}% del portafolio: {liquidez}')
                        idorden, status = funciones.ejecutarOrden(self.simbolo, 'BUY', self.convertirCantidad(liquidez), self.definirPrecioCompra(0.10))
                        self.ordenClass.insertarOrden(idorden, liquidez, self.precio_actual, 'BUY',datetime.today(), status)
                else:
                    print('no tienes para comprar')
                    """no hacer nada"""
            else:
                """no hacer nada"""
                print('ya tienes ordenes pendientes')

    """FUNCION QUE SE VA MANTENER EJECUTANDO"""
    def run(self):
        ''
        """
        -- asignar hora del servidor
        -- ejecutar funcion estrategia solo cuando sea 00:05 hora del servidor (tal vez)
        -- imprimir por telegram mensajes de errores *
        -- subir bd a la nube
        """



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
