import time
from os import path
from datetime import datetime
import pandas as pd
from conexion import binanceConnect
import funciones
from ordenClass import *
from chatTelegramClass import ChatTelegram


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
        try:
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
            ChatTelegram(f'ath temporal: {self.ath_temporal}')
            ChatTelegram(f'precio actual: {self.precio_actual}')
            return datareturn
        except Exception as e:
            ChatTelegram(f'ERROR hayNuevoAth:: {e}')

    """convierte la cantidad de USD a BTC"""
    def convertirCantidad(self, fiat):
        cantidad_en_btc = fiat / self.precio_actual
        cantidad_en_btc = round(cantidad_en_btc, 5)
        print('cantidad de compra en btc: ',cantidad_en_btc)
        return cantidad_en_btc

    """retorna el porcentaje de el monto ingresado"""
    def definirPorcentaje(self,monto, porcentaje):
        return round(monto * porcentaje,2)

    """define el porcentaje por debajo del precio actual para ejecutar la orden de compra"""
    def definirPrecioCompra(self, porcentaje):
        precio_btc = round(self.precio_actual - (self.precio_actual * porcentaje),2)
        print('precio de compra en btc -> ',precio_btc)
        return precio_btc


    def estrategia(self):
        try:
            print('function::estrategia')
            """elegir estrategia"""
            #ChatTelegram(f'ATH temporal actual: {self.ath_temporal}')
            cantidad_min, cantidad_max, cantidad_min_dolar = funciones.cantidad_min_max(self.simbolo)
            #SABER EL PRECIO ACTUAL EN RELACION CON EL CIERRE DEL DIA ANTERIOR
            if self.hayNuevoATH() == True:
                ChatTelegram('El precio de hoy es mayor que el de ayer \n'
                             f'Nuevo ATH temporal: {self.ath_temporal}')
                moneda, liquidez, bloqueado = self.buscar_moneda('BTC')
                porcentaje_btc = round(self.definirPorcentaje(liquidez, 0.20),5)
                print('se deberian cancelar las ordenes pendientes y se tomar ganancias')
                dataOrden = self.ordenClass.buscarOrdenes_cripto_status('NEW')
                if len(dataOrden) > 0:
                    hayOrdenesFILLED = False
                    for id in dataOrden:
                        #SE GUARDAN LAS FUNCIONES EJECUTADAS
                        idorden, status = funciones.getStatusOrden(self.simbolo, id[0])
                        if status == 'FILLED':
                            self.ordenClass.updateOrden(idorden, status)
                            hayOrdenesFILLED = True
                        #SE BORRAN LAS FUNCIONES QUE NO SE EJECUTARON
                        elif status == 'NEW':
                            idorden, status = funciones.cancelarOrden(self.simbolo, id[0])
                            self.ordenClass.updateOrden(idorden, status)
                            hayOrdenesFILLED = False


                    #si ejecuta la orden de venta de btc y se ejecutaron las ordenes de compra
                    if hayOrdenesFILLED == True:
                        ChatTelegram('Las ordenes de compra ya fueron ejecutadas, revisa binance para mas detalles')

                        if porcentaje_btc > cantidad_min :
                            ChatTelegram('Se vende el 20% de BTC')
                            idorden, status = funciones.ejecutarOrden(self.simbolo, 'SELL',porcentaje_btc,self.precio_actual)
                            if idorden != None:
                                self.ordenClass.insertarOrden(idorden, porcentaje_btc, self.precio_actual, 'SELL', datetime.today(), status)
                        else:
                            ChatTelegram('No tienes para vender el 20% de tu capital en btc')
                    else:
                        ChatTelegram('Se cancelan las Ordenes de compra')
                else:
                    ChatTelegram('No hay Ordenes para cancelar' )
            else:
                ChatTelegram('No hay nuevo ATH')
    #-------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------EJECUTA LAS ORDENES DE COMPRA-------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------------------
            moneda, liquidez, bloqueado = self.buscar_moneda('BUSD')
            if bloqueado == 0:  # si no tengo ordenes pendientes
                # SABER SI TENGO BALANCE POSITIVO PARA HACER COMPRA
                if liquidez > cantidad_min_dolar:
                    # COMPRAR CON PORCENTAJES DEL PORTAFOLIO
                    porcentaje_liquidez1 = self.definirPorcentaje(liquidez, 0.25)
                    porcentaje_liquidez2 = self.definirPorcentaje(liquidez, 0.30)
                    porcentaje_liquidez3 = self.definirPorcentaje(liquidez, 0.35)

                    #PRECIO PARA EJECUTAR LAS ORDENES DE COMPRA
                    precio1 = self.definirPrecioCompra(0.05)
                    precio2 = self.definirPrecioCompra(0.10)
                    precio3 = self.definirPrecioCompra(0.15)

                    if porcentaje_liquidez1 > cantidad_min_dolar:  # si el porcentaje del portafolio se puede ejecutar la compra
                        print(f'tienes para comprar con el {0.25 * 100}% del portafolio, portafolio total:  {liquidez}')
                        #verifica que el precio actual este por arriba del precio de orden de compra
                        if self.precio_actual > precio1:

                            idorden, status = funciones.ejecutarOrden(self.simbolo, 'BUY',
                                                                      self.convertirCantidad(porcentaje_liquidez1),
                                                                      precio1)
                            if idorden != None:
                                self.ordenClass.insertarOrden(idorden, porcentaje_liquidez1, precio1, 'BUY',
                                                              datetime.today(), status)

                            # REVISA QUE TENGA PARA HACER LA SEGUNDA COMPRA
                        if porcentaje_liquidez2 > cantidad_min_dolar:  # si el porcentaje del portafolio se puede ejecutar la compra
                            print(f'tienes para comprar con el {0.25 * 100}% del portafolio: {liquidez}')

                            # verifica que el precio actual este por arriba del precio de orden de compra
                            if self.precio_actual > precio2:
                                idorden, status = funciones.ejecutarOrden(self.simbolo, 'BUY',
                                                                          self.convertirCantidad(porcentaje_liquidez2),
                                                                          precio2)
                                if idorden != None:
                                    self.ordenClass.insertarOrden(idorden, porcentaje_liquidez2, precio2, 'BUY',
                                                                  self.fechaActual, status)

                                # REVISA QUE TENGA PARA HACER LA SEGUNDA COMPRA
                                if porcentaje_liquidez3 > cantidad_min_dolar:  # si el porcentaje del portafolio se puede ejecutar la compra
                                    print(f'tienes para comprar con el {0.25 * 100}% del portafolio: {liquidez}')

                                    # verifica que el precio actual este por arriba del precio de orden de compra
                                    if self.precio_actual > precio3:
                                        idorden, status = funciones.ejecutarOrden(self.simbolo, 'BUY',
                                                                                  self.convertirCantidad(porcentaje_liquidez3),
                                                                                  precio3)
                                        if idorden != None:
                                            self.ordenClass.insertarOrden(idorden, porcentaje_liquidez3, precio3,
                                                                          'BUY', self.fechaActual, status)
                                    else:
                                        ChatTelegram('El precio actual es menor al 15% del ATH temporal')
                                        idorden, status = funciones.ejecutarOrden(self.simbolo, 'BUY',
                                                                                  self.convertirCantidad(
                                                                                      porcentaje_liquidez3),
                                                                                  self.precio_actual)
                                        if idorden != None:
                                            self.ordenClass.insertarOrden(idorden, porcentaje_liquidez3,
                                                                          self.precio_actual,
                                                                          'BUY', self.fechaActual, status)

                    else:  # el porcentaje del portafolio no llega al minimo para la compra
                        mensaje = f'tienes para comprar solo con el {100}% del portafolio: {liquidez}'
                        print(mensaje)
                        ChatTelegram(mensaje)
                        if self.precio_actual < precio1 and self.precio_actual < precio2 and self.precio_actual < precio3:
                            ChatTelegram('El precio actual es menor al 15% del ATH temporal')
                            idorden, status = funciones.ejecutarOrden(self.simbolo, 'BUY', self.convertirCantidad(liquidez),
                                                                      self.precio_actual)
                            self.ordenClass.insertarOrden(idorden, liquidez, self.precio_actual, 'BUY', datetime.today(),
                                                          status)
                        else:
                            idorden, status = funciones.ejecutarOrden(self.simbolo, 'BUY', self.convertirCantidad(liquidez),
                                                                      precio3)
                            self.ordenClass.insertarOrden(idorden, liquidez, precio3, 'BUY', datetime.today(),
                                                          status)

                    ChatTelegram('Se abrieron ordenes de compra, revisa binance para mas detalles')
                else:
                    mensaje = 'no tienes liquidez para comprar'
                    print(mensaje)
                    ChatTelegram(mensaje)

            else:
                """no hacer nada
                    MENSAJE POR TELEGRAM
                """
                mensaje = 'ya tienes ordenes pendientes'
                print(mensaje)
                ChatTelegram(mensaje)
        except Exception as e:
            ChatTelegram(f'ERROR estrategia:: {e}')

        #-----------------------------------------------------------------------------------------------




    def tiempo(self):
        print('function::tiempo')
        time_res = funciones.cliente.get_server_time()
        ts = time_res.get('serverTime')
        self.seconds = datetime.utcfromtimestamp(ts / 1000).second
        self.minute = datetime.utcfromtimestamp(ts / 1000).minute
        self.hour = datetime.utcfromtimestamp(ts / 1000).hour
        pass

    """FUNCION QUE SE VA MANTENER EJECUTANDO"""
    def start(self):
        """
            Inicia el bot
        """
        print('espera 1 minuto y revisa telegram')
        time.sleep(59)
        ChatTelegram('Corriendo el bot...')


        while self.RUN == True:
            self.tiempo()
            self.precio_actual = self.datosTicker['close'][1]
            if self.hour == 1 and self.minute < 59:
                self.estrategia()
            else:
                ChatTelegram(f'Aun no es la hora')
                ChatTelegram(f'Precio Actual: {self.precio_actual}')
            time.sleep(1795) #espera media hora





bot = CriptoBot()
bot.start()




