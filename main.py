import time
from os import path, remove
from datetime import datetime
import os
import pandas as pd
import telebot
import telegram.error
from telegram.ext import Updater, CommandHandler
import conexion
import config
import indicadores
from estrategias import *
import funciones
import csv
#import backtesting

class CriptoBot():
    def __init__(self):
        self.cliente = conexion.cliente
        self.lista_cripto = []
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

    #lee la lista de criptos
    def get_lista_criptos(self):
        lista = []
        if not path.exists(self.csv_cripto):
            self.lista_cripto = ['BTCUSDT', 'SOLUSDT', 'DOTUSDT', 'LUNAUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT']
            print('No existe el CSV con la lista de criptos')
        else:
            with open(self.csv_cripto, newline='') as File:
                reader = csv.reader(File)
                for row in reader:
                    if len(row[0]) > 0:
                        lista.append(row[0])
            self.lista_cripto = lista
        return lista

    #muestra la lista de criptos en telegram
    def mostrar_lista_cripto(self,update, context):
        updater = Updater(config.TOKEN, use_context=True)
        self.get_lista_criptos()
        df_lista_cripto = pd.DataFrame(self.lista_cripto)
        columns = ['Pares de Criptos']
        df_lista_cripto.columns = columns
        df_lista_cripto.set_index('Pares de Criptos')
        updater.bot.send_message(config.CHAT_ID, f'{df_lista_cripto}')
        pass


    #agrega criptos a la lista
    def agregar_criptos(self, update, context):
        try:
            updater = Updater(config.TOKEN, use_context=True)
            argumento = context.args
            cripto = argumento[0]
            lista =[cripto]
            if funciones.existe_par(cripto):
                if path.exists(self.csv_cripto):
                    self.get_lista_criptos()
                    for i in self.lista_cripto:
                        if i == cripto:
                            ya_existe = True
                            break
                        else:
                            ya_existe = False
                    if ya_existe == False:
                        if len(argumento) > 0:
                            df_cripto = pd.DataFrame(lista)
                            df_cripto.to_csv(self.csv_cripto, index=None, mode='a',header=not os.path.isfile(self.csv_cripto))
                            updater.bot.send_message(config.CHAT_ID, f'Se agrego {cripto} a la lista')
                            return True
                        else:
                            updater.bot.send_message(config.CHAT_ID, f'Asegurese de haber ingresado datos')
                            return False
                    else:
                        updater.bot.send_message(config.CHAT_ID, f'Ya existe esta moneda en la lista')
                        return False
            else:
                updater.bot.send_message(config.CHAT_ID, f'No existe el par {cripto} en Binance')
                return False
        except Exception as e:
            updater.bot.send_message(config.CHAT_ID, f'ERROR: \n {e}')
            print('Error: ',e)
            return None

    #elimina criptos de la lista
    def elimina_criptos(self,update, context):
         try:
             updater = Updater(config.TOKEN, use_context=True)
             argumento = context.args
             cripto = argumento[0]
             if path.exists(self.csv_cripto):
                 lista = []
                 self.get_lista_criptos()
                 for i in self.lista_cripto:
                     if i == cripto:
                         ya_existe = True
                     else:
                         ya_existe = False
                 if ya_existe == True:
                     if len(argumento) > 0:
                         with open(self.csv_cripto, newline='') as file:
                             reader = csv.reader(file)
                             for row in reader:
                                 if row[0] != cripto:
                                     lista.append(row[0])
                             datos_df = pd.DataFrame(lista)
                             datos_df.to_csv(self.csv_cripto, index=None,header=not os.path.isfile(self.csv_cripto))
                             updater.bot.send_message(config.CHAT_ID, f'Se elimino {cripto} de la lista')
                             return True
                     else:
                         updater.bot.send_message(config.CHAT_ID, f'Aseguerese de haber ingresado datos')
                         return False
                 else:
                    updater.bot.send_message(config.CHAT_ID, f'{cripto} no esta en la lista')
                    return False
         except Exception as e:
            updater.bot.send_message(config.CHAT_ID, f'ERROR: \n {e}')
            print('ERRORs: ', e)
            return None


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


    def avisar(self, cripto):
        self.data_df = funciones.datos_ticker(cripto, self.time, self.limite)
        self.accion = self.estrategia(cripto)
        if self.accion == 2:
            aviso=f'Cruce medias moviles \n HMA80: {self.valor_hma80} \n HMA50: {self.valor_hma50}'
        elif self.accion == 1:
            aviso='Oportunidad de compra'
            self.log(cripto, self.precio_compra)
        elif self.accion == -2:
            aviso='Cierra 50%'
        elif self.accion == -1:
            aviso='cierra todo'
        else:
            aviso='No hay entradas ni salidas'
        moneda = self.buscar_moneda(cripto)
        if moneda == cripto:
            moneda_tiene='Ya tienes esa moneda'
        else:
            moneda_tiene='No tienes esa moneda'
        self.mensaje = (f'{cripto} \n {aviso} \n {moneda_tiene}')
        return self.mensaje

    def start(self,update, context): #automatizar el solo mostrar la estrategia
        try:
            old, new = funciones.tiempo_server()
            self.tiempo()
            updater = Updater(config.TOKEN, use_context=True)
            updater.bot.send_message(config.CHAT_ID, f'Hora del servidor: \n {new}')
            self.get_lista_criptos()
            if len(self.lista_cripto) < 1:
                self.get_lista_criptos()
            for i in self.lista_cripto:
                existe = funciones.existe_par(i)
                if existe == True:
                    updater.bot.send_message(config.CHAT_ID, self.avisar(i))
                    if self.accion == 1:
                        updater.bot.send_message(config.CHAT_ID, f'Pagina TradingView: \n {self.tradingView_pag}{i}')
                        updater.bot.send_message(config.CHAT_ID, f'Pagina Binance: \n {self.binance_pag}{i}')
                else:
                    updater.bot.send_message(config.CHAT_ID, f'No existe el par {i}')
            if self.hour == 00:
                updater.bot.send_message(config.CHAT_ID, 'Puedes Ejecutar Ordenes...')
            else:
                updater.bot.send_message(config.CHAT_ID,
                                         f'Se recomienda esperar a que sean las 12 hora del servidor... \n {new}')
        except Exception as e:
            updater.bot.send_message(config.CHAT_ID, f'ERROR: \n {e}')
            print('ERROR: ',e)


    def run(self):
        try:
            # ejecuta en telegram
            updater = Updater(config.TOKEN, use_context=True)
            updater.dispatcher.add_handler(CommandHandler('start', self.start))
            updater.dispatcher.add_handler(CommandHandler('lista', self.mostrar_lista_cripto))
            updater.dispatcher.add_handler(CommandHandler('agregar', self.agregar_criptos, pass_args=True))
            updater.dispatcher.add_handler(CommandHandler('eliminar', self.elimina_criptos, pass_args=True))
            print('Conexion con Telegram Exitosa')
            # start
            updater.start_polling()
            updater.bot.send_message(config.CHAT_ID, f'Corriendo bot...')
            print('listo para utilizar')
            # me quedo esperando
            updater.idle()


        except Exception as e:
            updater.bot.send_message(config.CHAT_ID, f'ERROR: \n {e}')
            print('ERROR: ', e)

class bot_tendencia():
    def __init__(self):
        self.cliente = conexion.cliente
        self.lista_cripto = ['BTCUSDT', 'DOTUSDT', 'LUNAUSDT', 'ROSEUSDT']
        self.time = '1d'
        self.limite = 200
        self.data_df = ''
        self.valor_hma80 = 0
        self.valor_hma50 = 0
        self.valor_hma200 = 0
        self.precio = 0
        """VALORES POR DEFECTO"""
        self.HMA_50 = 50
        self.HMA_80 = 80
        self.HMA_200 = 200
        self.RUN = True
        self.mensaje = None
        self.alcista = None
        """Se le asigna el tiempo del servidor"""
        self.seconds = 0
        self.minute = 0
        self.hour = 0

    def tiempo(self):
        time_res = conexion.cliente.get_server_time()
        ts = time_res.get('serverTime')
        self.seconds = datetime.utcfromtimestamp(ts / 1000).second
        self.minute = datetime.utcfromtimestamp(ts / 1000).minute
        self.hour = datetime.utcfromtimestamp(ts / 1000).hour
        pass

    def buscar_moneda(self, cripto):
        balance = funciones.balance()
        for d in range(len(balance)):
            if balance['asset'][d] + 'USDT' == cripto:
                return cripto

    def estrategia(self):
        """elegir estrategia"""
        estrategias = Cruce_hma(self.data_df, self.HMA_200, self.HMA_80, self.HMA_50)
        self.valor_hma50,self.valor_hma80, self.valor_hma200 ,self.precio = estrategias.alcista_bajista() #tendencia
        return estrategias.es_alcista

    def avisar(self,cripto):
        self.data_df = funciones.datos_ticker(cripto, self.time, self.limite)
        self.alcista =  self.estrategia()
        if self.alcista == True:
            aviso = f'Tendencia Alcista\n HMA50: {self.valor_hma50} \n HMA80: {self.valor_hma80} \n HMA200: {self.valor_hma200} \n PRECIO: {self.precio}'
        elif self.alcista == False:
            aviso = f'Tendencia Bajista\n HMA50: {self.valor_hma50} \n HMA80: {self.valor_hma80} \n HMA200: {self.valor_hma200} \n PRECIO: {self.precio}'
        else:
            aviso = f'No hay Tendencia definida \n HMA50: {self.valor_hma50} \n HMA80: {self.valor_hma80} \n HMA200: {self.valor_hma200} \n PRECIO: {self.precio}'

        moneda = self.buscar_moneda(cripto)
        if moneda == cripto:
            moneda_tiene = 'Ya tienes esa moneda'
        else:
            moneda_tiene = 'No tienes esa moneda'

        self.mensaje = (f'{cripto} \n {aviso} \n {moneda_tiene}')
        return self.mensaje

    def start(self, update):
        try:
            old, new = funciones.tiempo_server()
            self.tiempo()
            updater = Updater(config.TOKEN, use_context=True)
            updater.bot.send_message(config.CHAT_ID, f'Hora del servidor: \n {new}')
            for i in self.lista_cripto:
                existe = funciones.existe_par(i)
                if existe == True:
                    updater.bot.send_message(config.CHAT_ID, self.avisar(i))
            updater.bot.send_message(config.CHAT_ID, f'Verifique los valores de las Medias Moviles de Hull')
            print(updater.message)
        except Exception as e:
            updater.bot.send_message(config.CHAT_ID, f'ERROR: \n {e}')
            print('ERROR: ',e)

    def run(self):
        try:
            updater = Updater(config.TOKEN, use_context=True)
            self.tiempo()
            updater.start_polling()
            updater.bot.send_message(config.CHAT_ID, f'Corriendo bot...')
            print('listo para utilizar')
            while self.RUN == True:
                if self.hour == 23 and self.minute == 59:
                    self.start(updater)
                time.sleep(60)
        except Exception as e:
            updater.bot.send_message(config.CHAT_ID, f'ERROR: \n {e}')
            print('ERROR METODO RUN: ', e)


bot = bot_tendencia() #instancia el bot
bot.run()

